"""
Ed25519 Cryptographically Signed Offline QR Code Engine
SIH26035: Automated OIML R-76 Guided Testing & Traceable Reporting System
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Conforms to:
- RFC 8032: Edwards-Curve Digital Signature Algorithm (Ed25519)
- WELMEC Guide 7.2 (Software Guide) Cryptographic Sealing & Traceability
- OIML-CS Scheme A Type Approval Certification & Inspection Standards
- Offline-First Architecture (100% local cryptographic verification without network connectivity)
"""

import os
import io
import json
import base64
import hashlib
import hmac
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple, Union, List

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

import qrcode
import qrcode.image.svg
from PIL import Image, ImageDraw

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
except ImportError:
    pyzbar_decode = None

from core.welmec_sealer import WelmecSoftwareSealer


DEFAULT_KEY_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "keys"
DEFAULT_ISSUER = "RRSL-Faridabad / Ministry of Consumer Affairs, Govt. of India"
MAX_PAYLOAD_SIZE = 65536  # 64 KB limit to protect against DoS memory exhaustion & ReDoS

ECL_MAP = {
    "L": qrcode.constants.ERROR_CORRECT_L,  # ~7% error recovery
    "M": qrcode.constants.ERROR_CORRECT_M,  # ~15% error recovery (Standard)
    "Q": qrcode.constants.ERROR_CORRECT_Q,  # ~25% error recovery (High)
    "H": qrcode.constants.ERROR_CORRECT_H,  # ~30% error recovery (Industrial/Field Harsh)
}


class KeyRecord:
    """Metadata record for a registered public key within the offline TrustStore."""

    def __init__(
        self,
        public_key: ed25519.Ed25519PublicKey,
        authority_name: str,
        kid: Optional[str] = None,
        valid_from: Optional[datetime] = None,
        valid_until: Optional[datetime] = None,
        is_revoked: bool = False,
        revocation_reason: str = ""
    ):
        self.public_key = public_key
        self.authority_name = authority_name
        raw_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        self.raw_bytes = raw_bytes
        self.hex = raw_bytes.hex()
        self.fingerprint = f"SHA256:{hashlib.sha256(raw_bytes).hexdigest()}"
        self.kid = kid or self.fingerprint[:23]
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.is_revoked = is_revoked
        self.revocation_reason = revocation_reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authority_name": self.authority_name,
            "kid": self.kid,
            "fingerprint": self.fingerprint,
            "pubkey_hex": self.hex,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "is_revoked": self.is_revoked,
            "revocation_reason": self.revocation_reason
        }


class TrustStore:
    """
    Offline public key trust store and Certificate Revocation List (CRL) for Legal Metrology.
    Enables multi-authority verification (e.g. regional RRSL labs across India)
    and enforces key validity windows and instant offline key revocation.
    """

    def __init__(self):
        self._keys_by_fingerprint: Dict[str, KeyRecord] = {}
        self._keys_by_hex: Dict[str, KeyRecord] = {}
        self._keys_by_kid: Dict[str, KeyRecord] = {}
        self._revoked_identifiers: Dict[str, str] = {}  # fingerprint/hex/kid -> reason

    def register_key(
        self,
        pubkey_input: Union[ed25519.Ed25519PublicKey, bytes, str],
        authority_name: str,
        kid: Optional[str] = None,
        valid_from: Optional[datetime] = None,
        valid_until: Optional[datetime] = None
    ) -> KeyRecord:
        resolved = Ed25519ReportSigner.resolve_public_key(pubkey_input)
        record = KeyRecord(
            public_key=resolved,
            authority_name=authority_name,
            kid=kid,
            valid_from=valid_from,
            valid_until=valid_until
        )
        self._keys_by_fingerprint[record.fingerprint] = record
        self._keys_by_hex[record.hex] = record
        self._keys_by_kid[record.kid] = record
        return record

    def revoke_key(self, identifier: str, reason: str = "Key revoked by regulatory authority") -> bool:
        """Revokes a key by fingerprint, kid, or hex string in the CRL."""
        clean = identifier.strip()
        self._revoked_identifiers[clean] = reason
        found = False
        for rec in list(self._keys_by_fingerprint.values()):
            if (rec.fingerprint == clean or rec.hex == clean or rec.kid == clean or 
                rec.fingerprint.startswith(clean) or clean.startswith(rec.kid)):
                rec.is_revoked = True
                rec.revocation_reason = reason
                self._revoked_identifiers[rec.fingerprint] = reason
                self._revoked_identifiers[rec.hex] = reason
                self._revoked_identifiers[rec.kid] = reason
                found = True
        return found

    def is_revoked(self, identifier: str) -> Tuple[bool, str]:
        """Checks whether the key or fingerprint is present in the CRL."""
        clean = identifier.strip()
        if clean in self._revoked_identifiers:
            return True, self._revoked_identifiers[clean]
        for k, reason in self._revoked_identifiers.items():
            if clean.startswith(k) or k.startswith(clean):
                return True, reason
        return False, ""

    def find_record(self, identifier: str) -> Optional[KeyRecord]:
        """Looks up a registered key record by fingerprint, hex, or kid."""
        clean = identifier.strip()
        if clean in self._keys_by_fingerprint:
            return self._keys_by_fingerprint[clean]
        if clean in self._keys_by_hex:
            return self._keys_by_hex[clean]
        if clean in self._keys_by_kid:
            return self._keys_by_kid[clean]
        for rec in self._keys_by_fingerprint.values():
            if rec.fingerprint.startswith(clean) or clean.startswith(rec.kid):
                return rec
        return None

    def check_validity(self, identifier: str, check_time: Optional[datetime] = None) -> Tuple[bool, str]:
        """Validates key revocation and timestamp bounds against validity window."""
        is_rev, reason = self.is_revoked(identifier)
        if is_rev:
            return False, f"Key revoked: {reason}"
        rec = self.find_record(identifier)
        if not rec:
            return True, "Key not in trust store registry (unmanaged)"
        t = check_time or datetime.now(timezone.utc)
        if rec.valid_from and t < rec.valid_from:
            return False, f"Key not yet valid (valid from {rec.valid_from.isoformat()})"
        if rec.valid_until and t > rec.valid_until:
            return False, f"Key expired on {rec.valid_until.isoformat()}"
        return True, "Key is valid and active"


class Ed25519ReportSigner:
    """
    Manages asymmetric cryptographic signing and verification for OIML R 76-2 certificates.
    Uses Ed25519 (EdDSA over Curve25519) for deterministic, fast, 128-bit post-classical security.
    """

    def __init__(
        self,
        key_dir: Optional[Path] = None,
        private_key: Optional[ed25519.Ed25519PrivateKey] = None,
        public_key: Optional[ed25519.Ed25519PublicKey] = None,
    ):
        self.key_dir = key_dir or DEFAULT_KEY_DIR
        self.private_key = private_key
        self.public_key = public_key

        if self.private_key is None and self.public_key is None:
            self._load_or_generate_keys()
        elif self.private_key is not None and self.public_key is None:
            self.public_key = self.private_key.public_key()

    def _load_or_generate_keys(self) -> None:
        """Loads existing keypair from key_dir or generates a persistent new one."""
        self.key_dir.mkdir(parents=True, exist_ok=True)
        priv_file = self.key_dir / "ed25519_private.pem"
        pub_file = self.key_dir / "ed25519_public.pem"

        if priv_file.exists():
            try:
                pem_data = priv_file.read_bytes()
                self.private_key = serialization.load_pem_private_key(pem_data, password=None)
                if not isinstance(self.private_key, ed25519.Ed25519PrivateKey):
                    raise TypeError("Stored private key is not an Ed25519 key")
                self.public_key = self.private_key.public_key()
                # Ensure public file exists
                if not pub_file.exists():
                    self._save_public_pem(pub_file)
                return
            except Exception:
                # Key corruption fallback: regenerate
                pass

        # Generate new Ed25519 keypair
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        # Save private key (PKCS#8 PEM)
        priv_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        priv_file.write_bytes(priv_pem)
        try:
            os.chmod(priv_file, 0o600)
        except OSError:
            pass

        self._save_public_pem(pub_file)

    def _save_public_pem(self, pub_file: Path) -> None:
        """Writes public key to SubjectPublicKeyInfo PEM format."""
        if self.public_key:
            pub_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            pub_file.write_bytes(pub_pem)

    # ==========================================
    # Key Serialization & Fingerprint Helpers
    # ==========================================

    def get_public_key_raw(self) -> bytes:
        """Returns 32-byte raw Ed25519 public key."""
        if not self.public_key:
            raise ValueError("Public key not available")
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def get_public_key_hex(self) -> str:
        """Returns 64-char hex string of raw 32-byte public key."""
        return self.get_public_key_raw().hex()

    @property
    def public_key_hex(self) -> str:
        """Property returning 64-char hex string of raw 32-byte public key."""
        return self.get_public_key_hex()

    def get_public_key_pem(self) -> str:
        """Returns OpenSSL SubjectPublicKeyInfo PEM string."""
        if not self.public_key:
            raise ValueError("Public key not available")
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

    def get_public_key_fingerprint(self) -> str:
        """Returns SHA-256 fingerprint of the raw public key bytes."""
        raw = self.get_public_key_raw()
        digest = hashlib.sha256(raw).hexdigest()
        return f"SHA256:{digest}"

    # ==========================================
    # Canonical Serialization & Hashing
    # ==========================================

    @staticmethod
    def canonicalize(data: Dict[str, Any]) -> bytes:
        """
        Produces strict, deterministic canonical UTF-8 JSON bytes.
        - Lexicographically sorts all dictionary keys.
        - Strips superfluous whitespace (separators=(',', ':')).
        - Preserves unicode without ASCII escaping.
        """
        return json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False
        ).encode("utf-8")

    @classmethod
    def compute_report_hash(cls, report_data: Dict[str, Any]) -> str:
        """Calculates SHA-256 hex digest of the canonical report data."""
        canonical_bytes = cls.canonicalize(report_data)
        return hashlib.sha256(canonical_bytes).hexdigest()

    # ==========================================
    # Signing & Verification Workflows
    # ==========================================

    def create_claims(
        self,
        session_id: str,
        revision: int,
        spec_model: str,
        spec_serial: str,
        accuracy_class: str,
        verdict: str,
        report_sha256: str,
        issuer: str = DEFAULT_ISSUER,
        reviewer_id: str = "RRSL-Inspector",
        timestamp_iso: Optional[str] = None
    ) -> Dict[str, Any]:
        """Constructs standardized OIML R 76 certificate claims dictionary."""
        sealer_info = WelmecSoftwareSealer.calculate_lrs_fingerprint()
        lrs_sha = sealer_info.get("sha256", "UNKNOWN")

        ts = timestamp_iso or datetime.now(timezone.utc).isoformat()
        fingerprint = self.get_public_key_fingerprint()

        claims = {
            "iss": issuer,
            "cert_id": f"OIML-RRSL-{session_id}-R{revision}",
            "sess_id": session_id,
            "rev": int(revision),
            "model": str(spec_model),
            "serial": str(spec_serial),
            "acc_class": str(accuracy_class),
            "verdict": str(verdict).upper(),
            "rep_sha256": str(report_sha256),
            "lrs_sha256": str(lrs_sha),
            "reviewer": str(reviewer_id),
            "ts": str(ts),
            "pubkey_id": fingerprint[:23]  # "SHA256:" + 16 hex chars
        }
        return claims

    def sign_claims(self, claims: Dict[str, Any]) -> Dict[str, Any]:
        """
        Signs canonical claims with Ed25519 private key.
        Returns a complete signed envelope ready for QR encoding:
        {
            "claims": { ... },
            "sig": "<base64url_signature>",
            "pubkey_hex": "<64_hex_chars>"
        }
        """
        if not self.private_key:
            raise ValueError("Private key not available for signing")

        canonical_bytes = self.canonicalize(claims)
        signature_bytes = self.private_key.sign(canonical_bytes)
        # RFC 7515 URL-safe Base64 without '=' padding
        sig_b64 = base64.urlsafe_b64encode(signature_bytes).decode("ascii").rstrip("=")

        return {
            "claims": claims,
            "sig": sig_b64,
            "pubkey_hex": self.get_public_key_hex()
        }

    @classmethod
    def resolve_public_key(
        cls,
        pubkey_input: Union[ed25519.Ed25519PublicKey, bytes, str]
    ) -> ed25519.Ed25519PublicKey:
        """Resolves various public key representations into an Ed25519PublicKey instance."""
        if isinstance(pubkey_input, ed25519.Ed25519PublicKey):
            return pubkey_input

        if isinstance(pubkey_input, str):
            clean_str = pubkey_input.strip()
            # Check if PEM
            if "BEGIN PUBLIC KEY" in clean_str:
                loaded = serialization.load_pem_public_key(clean_str.encode("utf-8"))
                if not isinstance(loaded, ed25519.Ed25519PublicKey):
                    raise ValueError("PEM does not contain an Ed25519 public key")
                return loaded
            # Check if 64-char Hex
            if len(clean_str) == 64:
                try:
                    raw_bytes = bytes.fromhex(clean_str)
                    return ed25519.Ed25519PublicKey.from_public_bytes(raw_bytes)
                except ValueError as e:
                    raise ValueError(f"Invalid hex public key: {e}")
            # Check if Base64 / Base64URL
            try:
                # Add padding if necessary
                padded = clean_str + "=" * ((4 - len(clean_str) % 4) % 4)
                raw_bytes = base64.urlsafe_b64decode(padded)
                if len(raw_bytes) == 32:
                    return ed25519.Ed25519PublicKey.from_public_bytes(raw_bytes)
            except Exception:
                pass
            raise ValueError("Unrecognized public key format (expected PEM, 64-char hex, or 32-byte b64)")

        if isinstance(pubkey_input, (bytes, bytearray)):
            if len(pubkey_input) == 32:
                return ed25519.Ed25519PublicKey.from_public_bytes(bytes(pubkey_input))
            elif b"BEGIN PUBLIC KEY" in pubkey_input:
                loaded = serialization.load_pem_public_key(pubkey_input)
                if not isinstance(loaded, ed25519.Ed25519PublicKey):
                    raise ValueError("PEM does not contain an Ed25519 public key")
                return loaded
            raise ValueError(f"Invalid public key byte length ({len(pubkey_input)} bytes, expected 32)")

        raise TypeError(f"Unsupported public key type: {type(pubkey_input)}")

    @classmethod
    def verify_envelope(
        cls,
        envelope_data: Union[Dict[str, Any], str],
        trusted_public_key: Optional[Union[ed25519.Ed25519PublicKey, bytes, str, TrustStore]] = None,
        trust_store: Optional[TrustStore] = None,
        strict_trust_store: bool = False
    ) -> Dict[str, Any]:
        """
        Cryptographically verifies an offline QR code envelope.
        Supports trusted public keys, TrustStore with Certificate Revocation Lists (CRL),
        strict schema validation, DoS input bounds, and constant-time execution.
        """
        try:
            # 1. DoS Protection: verify payload size bounds before parsing
            if isinstance(envelope_data, str):
                raw_bytes_len = len(envelope_data.encode("utf-8"))
                if raw_bytes_len > MAX_PAYLOAD_SIZE:
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": f"Payload size ({raw_bytes_len} bytes) exceeds maximum allowable limit ({MAX_PAYLOAD_SIZE} bytes)",
                        "claims": None
                    }
                try:
                    envelope = json.loads(envelope_data)
                except Exception as ex:
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": f"Malformed JSON envelope: {str(ex)}",
                        "claims": None
                    }
            elif isinstance(envelope_data, dict):
                envelope = envelope_data
            else:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": f"Invalid envelope type: {type(envelope_data)}",
                    "claims": None
                }

            # 2. Check required top-level fields
            if not isinstance(envelope, dict) or "claims" not in envelope or "sig" not in envelope:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": "Envelope missing mandatory 'claims' or 'sig' fields",
                    "claims": envelope.get("claims") if isinstance(envelope, dict) else None
                }

            # Field tampering defense: reject unexpected top-level envelope properties
            allowed_envelope_keys = {"claims", "sig", "pubkey_hex"}
            unexpected_fields = set(envelope.keys()) - allowed_envelope_keys
            if unexpected_fields:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": f"Envelope contains unexpected or tampered fields: {sorted(list(unexpected_fields))}",
                    "claims": envelope.get("claims")
                }

            claims = envelope["claims"]
            if not isinstance(claims, dict):
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": "'claims' field must be a dictionary",
                    "claims": None
                }

            # 3. Type confusion & schema defensive validation
            if "rev" in claims:
                try:
                    rev_int = int(claims["rev"])
                    if rev_int < 0:
                        return {
                            "is_valid": False,
                            "status": "FORGED_OR_INVALID",
                            "error": "Claim 'rev' must be a non-negative integer",
                            "claims": claims
                        }
                except (ValueError, TypeError):
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": "Claim 'rev' type confusion: expected integer",
                        "claims": claims
                    }

            if "ts" in claims:
                ts_val = claims["ts"]
                if not isinstance(ts_val, str):
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": "Claim 'ts' must be an ISO-8601 formatted string",
                        "claims": claims
                    }
                try:
                    datetime.fromisoformat(ts_val.replace("Z", "+00:00"))
                except Exception as ts_err:
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": f"Claim 'ts' invalid ISO format: {str(ts_err)}",
                        "claims": claims
                    }

            # 4. Decode signature
            sig_str = envelope["sig"]
            if not isinstance(sig_str, str):
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": "Signature field must be a string",
                    "claims": claims
                }

            try:
                # Re-pad base64url if needed
                padded_sig = sig_str + "=" * ((4 - len(sig_str) % 4) % 4)
                trans_sig = padded_sig.replace("-", "+").replace("_", "/")
                sig_bytes = base64.b64decode(trans_sig, validate=True)
            except Exception as b64_ex:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": f"Invalid base64url signature encoding: {str(b64_ex)}",
                    "claims": claims
                }

            if len(sig_bytes) != 64:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": f"Invalid Ed25519 signature length: {len(sig_bytes)} bytes (must be exactly 64 bytes)",
                    "claims": claims
                }

            # 5. Handle TrustStore parameter if passed as trusted_public_key
            effective_trust_store = trust_store
            effective_trusted_key = trusted_public_key
            if isinstance(trusted_public_key, TrustStore):
                effective_trust_store = trusted_public_key
                effective_trusted_key = None

            # 6. Resolve verification public key
            resolved_key: ed25519.Ed25519PublicKey
            if effective_trusted_key is not None:
                try:
                    resolved_key = cls.resolve_public_key(effective_trusted_key)
                except Exception as pk_ex:
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": f"Could not resolve trusted public key: {str(pk_ex)}",
                        "claims": claims
                    }
            elif "pubkey_hex" in envelope:
                try:
                    resolved_key = cls.resolve_public_key(envelope["pubkey_hex"])
                except Exception as pk_ex:
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": f"Invalid envelope public key hex: {str(pk_ex)}",
                        "claims": claims
                    }
            elif effective_trust_store is not None:
                # Attempt to resolve via kid / pubkey_id from claims
                kid = claims.get("pubkey_id") or claims.get("kid")
                if kid:
                    rec = effective_trust_store.find_record(kid)
                    if rec:
                        resolved_key = rec.public_key
                    else:
                        return {
                            "is_valid": False,
                            "status": "UNTRUSTED_KEY",
                            "error": f"Key identifier '{kid}' not found in trust store",
                            "claims": claims
                        }
                else:
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": "No public key provided and claims lack key identifier",
                        "claims": claims
                    }
            else:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": "No public key provided and envelope does not contain 'pubkey_hex'",
                    "claims": claims
                }

            raw_pub = resolved_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            key_fingerprint = f"SHA256:{hashlib.sha256(raw_pub).hexdigest()}"
            pubkey_hex = raw_pub.hex()

            # Enforce envelope pubkey_hex consistency if trusted key was provided
            if effective_trusted_key is not None and "pubkey_hex" in envelope:
                env_hex = envelope["pubkey_hex"]
                if not isinstance(env_hex, str) or not hmac.compare_digest(env_hex.lower(), pubkey_hex.lower()):
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": "Public key declared in envelope ('pubkey_hex') does not match trusted public key",
                        "claims": claims
                    }

            # 7. Check TrustStore (CRL Revocation and Validity Windows)
            if effective_trust_store is not None:
                is_rev, rev_reason = effective_trust_store.is_revoked(key_fingerprint)
                if not is_rev:
                    is_rev, rev_reason = effective_trust_store.is_revoked(pubkey_hex)
                if is_rev:
                    return {
                        "is_valid": False,
                        "status": "REVOKED_KEY",
                        "error": f"Public key has been revoked by authority: {rev_reason}",
                        "claims": claims,
                        "public_key_fingerprint": key_fingerprint
                    }

                claim_dt = None
                if "ts" in claims:
                    try:
                        claim_dt = datetime.fromisoformat(claims["ts"].replace("Z", "+00:00"))
                    except Exception:
                        pass
                val_ok, val_msg = effective_trust_store.check_validity(key_fingerprint, check_time=claim_dt)
                if not val_ok:
                    return {
                        "is_valid": False,
                        "status": "EXPIRED_KEY",
                        "error": f"Key validity window check failed: {val_msg}",
                        "claims": claims,
                        "public_key_fingerprint": key_fingerprint
                    }

                if strict_trust_store and effective_trust_store.find_record(key_fingerprint) is None:
                    return {
                        "is_valid": False,
                        "status": "UNTRUSTED_KEY",
                        "error": f"Public key {key_fingerprint} is not registered in trust store",
                        "claims": claims,
                        "public_key_fingerprint": key_fingerprint
                    }

            # 8. Canonicalize claims
            canonical_bytes = cls.canonicalize(claims)

            # 9. Cryptographic verification
            try:
                resolved_key.verify(sig_bytes, canonical_bytes)
            except InvalidSignature:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": "Cryptographic signature verification failed: payload has been tampered with or key does not match",
                    "claims": claims
                }
            except Exception as v_ex:
                return {
                    "is_valid": False,
                    "status": "FORGED_OR_INVALID",
                    "error": f"Verification error: {str(v_ex)}",
                    "claims": claims
                }

            # 10. Constant-time fingerprint match verification
            declared_pubkey_id = claims.get("pubkey_id", "")
            if declared_pubkey_id:
                expected_prefix = key_fingerprint[:len(declared_pubkey_id)]
                if not hmac.compare_digest(declared_pubkey_id, expected_prefix):
                    return {
                        "is_valid": False,
                        "status": "FORGED_OR_INVALID",
                        "error": f"Public key fingerprint mismatch: claims declared {declared_pubkey_id}, but verified against {key_fingerprint[:23]}",
                        "claims": claims
                    }

            return {
                "is_valid": True,
                "status": "AUTHENTIC",
                "message": "Ed25519 digital signature verified. Document is authentic and unaltered.",
                "claims": claims,
                "certificate_id": claims.get("cert_id"),
                "revision": claims.get("rev"),
                "verdict": claims.get("verdict"),
                "issuer": claims.get("iss"),
                "public_key_fingerprint": key_fingerprint,
                "verified_offline": True,
                "timestamp": claims.get("ts")
            }

        except Exception as unhandled:
            return {
                "is_valid": False,
                "status": "FORGED_OR_INVALID",
                "error": f"Unexpected verification failure: {str(unhandled)}",
                "claims": None
            }

    # ==========================================
    # QR Code Rendering (SVG, PNG & Optical)
    # ==========================================

    @classmethod
    def generate_qr_svg(
        cls,
        payload: Union[Dict[str, Any], str],
        box_size: int = 10,
        border: int = 2,
        ecl: str = "M"
    ) -> str:
        """
        Generates a clean, crisp, self-contained SVG XML string of the QR code.
        Directly embeddable in HTML, PDF, or interactive workbench.
        Supports selectable Error Correction Levels: 'L' (7%), 'M' (15%), 'Q' (25%), 'H' (30%).
        """
        payload_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False) if isinstance(payload, dict) else str(payload)
        ec_level = ECL_MAP.get(ecl.upper(), qrcode.constants.ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec_level,
            box_size=box_size,
            border=border,
            image_factory=qrcode.image.svg.SvgPathImage
        )
        qr.add_data(payload_str)
        qr.make(fit=True)

        img = qr.make_image()
        buf = io.BytesIO()
        img.save(buf)
        svg_content = buf.getvalue().decode("utf-8")

        # Ensure SVG is responsive and strictly bounded by parent containers in HTML/PDF
        svg_content = re.sub(r'width="[^"]+"', 'width="100%"', svg_content, count=1)
        svg_content = re.sub(r'height="[^"]+"', 'height="100%"', svg_content, count=1)
        if 'style="' not in svg_content[:200]:
            svg_content = svg_content.replace('<svg ', '<svg style="width: 100%; height: 100%; display: block;" ', 1)
        return svg_content

    @classmethod
    def generate_qr_data_uri(
        cls,
        payload: Union[Dict[str, Any], str],
        ecl: str = "M"
    ) -> str:
        """Generates an SVG Data URI (data:image/svg+xml;base64,...) for direct HTML <img> embedding."""
        svg_xml = cls.generate_qr_svg(payload, ecl=ecl)
        encoded_svg = base64.b64encode(svg_xml.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded_svg}"

    @classmethod
    def generate_qr_png_bytes(
        cls,
        payload: Union[Dict[str, Any], str],
        box_size: int = 10,
        border: int = 4,
        ecl: str = "M"
    ) -> bytes:
        """Generates high-resolution raster PNG bytes with crisp quiet zones."""
        payload_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False) if isinstance(payload, dict) else str(payload)
        ec_level = ECL_MAP.get(ecl.upper(), qrcode.constants.ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec_level,
            box_size=box_size,
            border=border
        )
        qr.add_data(payload_str)
        qr.make(fit=True)

        pil_img = qr.make_image(fill_color="black", back_color="white").get_image()
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        return buf.getvalue()

    @classmethod
    def generate_qr_png_data_uri(
        cls,
        payload: Union[Dict[str, Any], str],
        box_size: int = 10,
        border: int = 4,
        ecl: str = "M"
    ) -> str:
        """Generates PNG Data URI (data:image/png;base64,...) for image preview."""
        png_bytes = cls.generate_qr_png_bytes(payload, box_size=box_size, border=border, ecl=ecl)
        b64 = base64.b64encode(png_bytes).decode("ascii")
        return f"data:image/png;base64,{b64}"

    @classmethod
    def simulate_qr_damage(
        cls,
        img: Image.Image,
        occlusion_ratio: float = 0.15,
        mode: str = "center_box"
    ) -> Image.Image:
        """
        Simulates physical damage (smudges, tears, coffee stains) on a QR code image
        to stress-test Reed-Solomon error correction boundaries.
        """
        damaged = img.copy()
        draw = ImageDraw.Draw(damaged)
        w, h = damaged.size

        if mode == "center_box":
            box_w = int(w * (occlusion_ratio ** 0.5))
            box_h = int(h * (occlusion_ratio ** 0.5))
            cx, cy = w // 2, h // 2
            x0 = max(0, cx - box_w // 2)
            y0 = max(0, cy - box_h // 2)
            x1 = min(w, cx + box_w // 2)
            y1 = min(h, cy + box_h // 2)
            draw.rectangle([x0, y0, x1, y1], fill="black")
        elif mode == "scratch":
            line_thickness = max(2, int(w * 0.05))
            draw.line([(0, h // 2), (w, h // 2)], fill="black", width=line_thickness)
            draw.line([(w // 4, 0), (3 * w // 4, h)], fill="black", width=line_thickness)

        return damaged

    @classmethod
    def decode_qr_image(cls, img_input: Union[Image.Image, bytes]) -> Optional[str]:
        """
        Decodes a QR code directly from a PIL Image or PNG bytes using pyzbar.
        Returns decoded string content, or None if damaged beyond recovery.
        """
        if pyzbar_decode is None:
            raise RuntimeError("pyzbar is not installed for optical decoding")

        if isinstance(img_input, bytes):
            img = Image.open(io.BytesIO(img_input))
        elif isinstance(img_input, Image.Image):
            img = img_input
        else:
            raise TypeError("img_input must be PIL.Image.Image or bytes")

        results = pyzbar_decode(img)
        if not results:
            return None
        return results[0].data.decode("utf-8")

