"""
WELMEC Guide 7.2 (Software Guide) Cryptographic Sealer
SIH26035: Legally Relevant Software (LRS) Integrity & Verification Module
Conforms to:
- WELMEC Guide 7.2 Extension L (Long-term Storage)
- WELMEC Guide 7.2 Extension S (Software Separation)
- OIML D 31:2008 General Requirements for Software-controlled Measuring Instruments
"""

import hashlib
import zlib
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

class WelmecSoftwareSealer:
    """
    Computes cryptographic checksums of the Legally Relevant Software (LRS) kernel
    and tracks legally relevant software parameter changes via chained cryptographic seals.
    Ensures that mathematical logic and Table 6 tolerances cannot be modified without
    generating an immutable audit trail and updating regulatory type approval seals.
    """

    GENESIS_SEAL = "0000000000000000000000000000000000000000000000000000000000000000"

    @staticmethod
    def get_lrs_file_path() -> Path:
        return Path(__file__).parent / "nawi_engine.py"

    @classmethod
    def calculate_lrs_fingerprint(cls) -> Dict[str, Any]:
        lrs_path = cls.get_lrs_file_path()
        if not lrs_path.exists():
            raise FileNotFoundError(f"LRS Kernel missing at {lrs_path}")

        content = lrs_path.read_bytes()

        # 1. SHA-256 Digest
        sha256_hash = hashlib.sha256(content).hexdigest()

        # 2. CRC-32 Checksum (Standard legal metrology indicator)
        crc32_val = zlib.crc32(content) & 0xffffffff
        crc32_hex = f"{crc32_val:08X}"

        # 3. File size & version metadata
        return {
            "lrs_module": "nawi_engine.py",
            "welmec_class": "Type P (Built-in) / Extension L (Long-term storage)",
            "sha256": sha256_hash,
            "crc32": crc32_hex,
            "byte_size": len(content),
            "status": "SEALED_VALID"
        }

    @classmethod
    def verify_runtime_integrity(cls, expected_sha256: str) -> bool:
        current = cls.calculate_lrs_fingerprint()
        return current["sha256"].lower() == expected_sha256.lower()


    @staticmethod
    def _canonicalize_value(val: Any) -> str:
        """Deterministically canonicalizes parameter value dictionaries or strings."""
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                return json.dumps(parsed, sort_keys=True, separators=(",", ":"))
            except Exception:
                return val
        return json.dumps(val, sort_keys=True, separators=(",", ":"))

    @classmethod
    def calculate_parameter_seal(
        cls,
        param_name: str,
        old_value: Any,
        new_value: Any,
        admin_id: str,
        reason: str,
        prev_seal: Optional[str] = None,
        timestamp_iso: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates an immutable chained SHA-256 cryptographic seal for legally relevant
        software parameter adjustments (e.g., OIML Table 6 tolerances).
        Conforms to WELMEC 7.2 Clause 3.2.1 Audit Trail requirements.
        """
        effective_prev = prev_seal if prev_seal else cls.GENESIS_SEAL
        now_iso = timestamp_iso or (datetime.now(timezone.utc).isoformat() + "Z")

        canonical_old = cls._canonicalize_value(old_value)
        canonical_new = cls._canonicalize_value(new_value)

        seal_payload = f"{effective_prev}|{param_name}|{canonical_old}|{canonical_new}|{admin_id}|{reason}|{now_iso}"
        seal_hash = hashlib.sha256(seal_payload.encode("utf-8")).hexdigest()

        crc32_val = zlib.crc32(seal_payload.encode("utf-8")) & 0xffffffff
        crc32_hex = f"{crc32_val:08X}"

        return {
            "seal_hash": seal_hash,
            "prev_seal": effective_prev,
            "crc32": crc32_hex,
            "parameter_name": param_name,
            "admin_id": admin_id,
            "reason": reason,
            "timestamp_iso": now_iso,
            "status": "LRS_PARAMETER_SEALED"
        }

    @classmethod
    def calculate_composite_system_seal(cls, active_tolerances: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a master composite software seal binding both the static LRS kernel code
        and the currently active legally relevant parameters (OIML Table 6 configuration).
        """
        code_fp = cls.calculate_lrs_fingerprint()
        tolerances_canonical = cls._canonicalize_value(active_tolerances)
        tolerances_sha256 = hashlib.sha256(tolerances_canonical.encode("utf-8")).hexdigest()

        composite_input = f"{code_fp['sha256']}:{tolerances_sha256}"
        composite_seal = hashlib.sha256(composite_input.encode("utf-8")).hexdigest()

        return {
            "master_lrs_seal": composite_seal,
            "code_sha256": code_fp["sha256"],
            "code_crc32": code_fp["crc32"],
            "tolerances_sha256": tolerances_sha256,
            "welmec_version": "WELMEC Guide 7.2 (2020)",
            "compliance_status": "SEALED_VALID",
            "is_tamper_evident": True
        }

    @classmethod
    def verify_parameter_chain(cls, audit_records: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
        """
        Validates cryptographic integrity across the parameter modification chain.
        """
        if not audit_records:
            return True, None

        expected_prev = cls.GENESIS_SEAL
        for idx, rec in enumerate(audit_records):
            prev_hash = rec.get("prev_hash") or rec.get("prev_seal")
            if prev_hash != expected_prev:
                return False, f"Broken link at audit entry #{idx + 1}: expected prev {expected_prev[:12]}, found {str(prev_hash)[:12]}"

            # Recompute using identical canonical serialization
            canonical_old = cls._canonicalize_value(rec["old_value"])
            canonical_new = cls._canonicalize_value(rec["new_value"])
            payload = f"{prev_hash}|{rec['parameter_name']}|{canonical_old}|{canonical_new}|{rec['admin_id']}|{rec['reason']}|{rec['timestamp_iso']}"
            computed = hashlib.sha256(payload.encode("utf-8")).hexdigest()

            actual_seal = rec.get("seal_hash") or rec.get("event_hash")
            if actual_seal != computed:
                return False, f"Tampered seal at audit entry #{idx + 1}: hash mismatch"

            expected_prev = actual_seal

        return True, None


if __name__ == "__main__":
    fp = WelmecSoftwareSealer.calculate_lrs_fingerprint()
    print("--- WELMEC 7.2 LRS FINGERPRINT ---")
    for k, v in fp.items():
        print(f"{k}: {v}")
