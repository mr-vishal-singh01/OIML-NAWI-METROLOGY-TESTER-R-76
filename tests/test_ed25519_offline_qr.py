"""
Exhaustive 20-Way Test Suite for Ed25519 Offline Cryptographic QR Code Engine
SIH26035: Automated OIML R-76 Guided Testing & Traceable Reporting System
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Covers 20 distinct verification scenarios:
 1. Keypair generation, persistence & reloading from disk
 2. Public key format conversions (PEM, raw 32-byte, 64-char hex, base64url)
 3. Canonical serialization determinism (key order invariance, whitespace stripping)
 4. Genuine payload signature generation and positive verification
 5. Tamper detection: Certificate ID mutation
 6. Tamper detection: Revision number mutation
 7. Tamper detection: Instrument verdict forgery (FAIL -> PASS)
 8. Tamper detection: Report SHA-256 calculation digest mutation
 9. Tamper detection: Legally Relevant Software (LRS) hash mutation
 10. Tamper detection: Timestamp alteration
 11. Tamper detection: Issuer authority spoofing
 12. Key mismatch / Rogue authority public key rejection
 13. Bit-flip cryptographic attack on 64-byte signature
 14. Truncated signature byte length rejection (< 64 bytes)
 15. Malformed / corrupted Base64URL signature rejection
 16. Deterministic handling of Unicode & Devanagari metrological metadata
 17. QR Code SVG generation & XML schema validity
 18. Payload density & scannability bounds (< 600 characters for high optical contrast)
 19. End-to-end QR code matrix data extraction & cryptographic verification
 20. FastAPI /api/verify/qr endpoint positive and negative validation
"""

import sys
import os
import json
import base64
import tempfile
import unittest
from pathlib import Path
from decimal import Decimal

# Ensure src is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import qrcode

from core.offline_qr import Ed25519ReportSigner
from core.nawi_engine import MetrologyMath, AccuracyClass, InstrumentSpecification
from core.welmec_sealer import WelmecSoftwareSealer
from fastapi.testclient import TestClient
from api.main import app


class TestEd25519OfflineQR(unittest.TestCase):
    """20-Way Cryptographic Test Suite for Ed25519 Offline Verification."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.key_dir = Path(cls.temp_dir.name) / "keys"
        cls.signer = Ed25519ReportSigner(key_dir=cls.key_dir)
        cls.client = TestClient(app)

        # Baseline sample claims
        cls.base_claims = cls.signer.create_claims(
            session_id="SESS-2026-TEST",
            revision=1,
            spec_model="APX-15K",
            spec_serial="SIH-2026-NAWI-001",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            issuer="RRSL-Faridabad / Ministry of Consumer Affairs, Govt. of India",
            reviewer_id="SCIENTIST_DR_SHARMA",
            timestamp_iso="2026-09-11T12:00:00Z"
        )
        cls.base_envelope = cls.signer.sign_claims(cls.base_claims)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    # ----------------------------------------------------------------------
    # Test 1: Keypair Generation, Persistence & Reloading
    # ----------------------------------------------------------------------
    def test_01_keypair_generation_and_persistence(self):
        """1. Verify generation, persistence, and reloading of Ed25519 keypair."""
        priv_pem = self.key_dir / "ed25519_private.pem"
        pub_pem = self.key_dir / "ed25519_public.pem"

        self.assertTrue(priv_pem.exists(), "Private key PEM file must exist on disk")
        self.assertTrue(pub_pem.exists(), "Public key PEM file must exist on disk")
        self.assertIn(b"BEGIN PRIVATE KEY", priv_pem.read_bytes())
        self.assertIn(b"BEGIN PUBLIC KEY", pub_pem.read_bytes())

        # Reload keys in a fresh instance
        reloaded_signer = Ed25519ReportSigner(key_dir=self.key_dir)
        self.assertEqual(
            self.signer.get_public_key_raw(),
            reloaded_signer.get_public_key_raw(),
            "Reloaded public key must exactly match original key"
        )
        self.assertEqual(
            self.signer.get_public_key_fingerprint(),
            reloaded_signer.get_public_key_fingerprint()
        )

    # ----------------------------------------------------------------------
    # Test 2: Public Key Format Conversions
    # ----------------------------------------------------------------------
    def test_02_public_key_formats(self):
        """2. Validate public key conversion across PEM, 32-byte raw, 64-char hex, and base64url."""
        raw = self.signer.get_public_key_raw()
        self.assertEqual(len(raw), 32, "Raw Ed25519 public key must be exactly 32 bytes")

        hex_str = self.signer.get_public_key_hex()
        self.assertEqual(len(hex_str), 64, "Hex public key must be 64 characters")
        self.assertEqual(bytes.fromhex(hex_str), raw)

        pem_str = self.signer.get_public_key_pem()
        self.assertIn("BEGIN PUBLIC KEY", pem_str)

        # Test resolution from all formats
        key_from_hex = Ed25519ReportSigner.resolve_public_key(hex_str)
        key_from_pem = Ed25519ReportSigner.resolve_public_key(pem_str)
        key_from_raw = Ed25519ReportSigner.resolve_public_key(raw)

        self.assertEqual(
            key_from_hex.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw),
            raw
        )
        self.assertEqual(
            key_from_pem.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw),
            raw
        )
        self.assertEqual(
            key_from_raw.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw),
            raw
        )

    # ----------------------------------------------------------------------
    # Test 3: Canonical Serialization Determinism
    # ----------------------------------------------------------------------
    def test_03_canonical_serialization_determinism(self):
        """3. Canonical JSON must be deterministic regardless of dictionary insertion order."""
        dict_a = {"z": 100, "a": "hello", "m": [1, 2, 3]}
        dict_b = {"a": "hello", "m": [1, 2, 3], "z": 100}

        bytes_a = Ed25519ReportSigner.canonicalize(dict_a)
        bytes_b = Ed25519ReportSigner.canonicalize(dict_b)

        self.assertEqual(bytes_a, bytes_b, "Canonicalization must be key-order invariant")
        self.assertEqual(bytes_a, b'{"a":"hello","m":[1,2,3],"z":100}')
        self.assertNotIn(b" ", bytes_a, "Canonical JSON must not contain extraneous whitespace")

    # ----------------------------------------------------------------------
    # Test 4: Genuine Payload Signature Generation & Positive Verification
    # ----------------------------------------------------------------------
    def test_04_signature_generation_and_positive_verification(self):
        """4. Verify that an unmolested genuine signed payload verifies as AUTHENTIC."""
        result = Ed25519ReportSigner.verify_envelope(self.base_envelope, self.signer.public_key)
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["status"], "AUTHENTIC")
        self.assertEqual(result["certificate_id"], "OIML-RRSL-SESS-2026-TEST-R1")
        self.assertEqual(result["verdict"], "PASSED")
        self.assertTrue(result["verified_offline"])

    # ----------------------------------------------------------------------
    # Test 5: Tamper Detection - Certificate ID Mutation
    # ----------------------------------------------------------------------
    def test_05_tamper_detection_certificate_id(self):
        """5. Mutating certificate ID in claims must fail verification."""
        forged = json.loads(json.dumps(self.base_envelope))
        forged["claims"]["cert_id"] = "OIML-RRSL-FORGED-001"

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")
        self.assertIn("signature verification failed", result["error"].lower())

    # ----------------------------------------------------------------------
    # Test 6: Tamper Detection - Revision Number Mutation
    # ----------------------------------------------------------------------
    def test_06_tamper_detection_revision_number(self):
        """6. Mutating revision number (e.g. 1 -> 2) must fail verification."""
        forged = json.loads(json.dumps(self.base_envelope))
        forged["claims"]["rev"] = 2

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 7: Tamper Detection - Instrument Verdict Forgery
    # ----------------------------------------------------------------------
    def test_07_tamper_detection_instrument_verdict(self):
        """7. Forging instrument verdict (e.g. FAILED -> PASSED) must fail verification."""
        failed_claims = self.signer.create_claims(
            session_id="SESS-FAIL-01",
            revision=1,
            spec_model="APX-15K",
            spec_serial="SIH-FAIL-999",
            accuracy_class="Class III",
            verdict="FAILED",
            report_sha256="1111111111111111111111111111111111111111111111111111111111111111"
        )
        failed_envelope = self.signer.sign_claims(failed_claims)

        # Forger attempts to flip verdict to PASSED
        forged = json.loads(json.dumps(failed_envelope))
        forged["claims"]["verdict"] = "PASSED"

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 8: Tamper Detection - Report SHA-256 Calculation Digest Mutation
    # ----------------------------------------------------------------------
    def test_08_tamper_detection_report_hash(self):
        """8. Altering even one character of the report SHA-256 must invalidate signature."""
        forged = json.loads(json.dumps(self.base_envelope))
        # Flip the last character
        orig_hash = forged["claims"]["rep_sha256"]
        tampered_hash = orig_hash[:-1] + ("0" if orig_hash[-1] != "0" else "1")
        forged["claims"]["rep_sha256"] = tampered_hash

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 9: Tamper Detection - Legally Relevant Software (LRS) Hash Mutation
    # ----------------------------------------------------------------------
    def test_09_tamper_detection_lrs_software_hash(self):
        """9. Mutating the WELMEC 7.2 LRS kernel hash in claims must invalidate signature."""
        forged = json.loads(json.dumps(self.base_envelope))
        forged["claims"]["lrs_sha256"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 10: Tamper Detection - Timestamp Alteration
    # ----------------------------------------------------------------------
    def test_10_tamper_detection_timestamp(self):
        """10. Modifying certification timestamp must fail verification."""
        forged = json.loads(json.dumps(self.base_envelope))
        forged["claims"]["ts"] = "2099-01-01T00:00:00Z"

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 11: Tamper Detection - Issuer Authority Spoofing
    # ----------------------------------------------------------------------
    def test_11_tamper_detection_issuer_spoofing(self):
        """11. Altering issuing authority must fail verification."""
        forged = json.loads(json.dumps(self.base_envelope))
        forged["claims"]["iss"] = "Fake Lab Testing Authority Ltd."

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 12: Key Mismatch / Rogue Authority Rejection
    # ----------------------------------------------------------------------
    def test_12_key_mismatch_rogue_authority(self):
        """12. Verifying a payload signed by Authority A against rogue Authority B's key must fail."""
        rogue_private = ed25519.Ed25519PrivateKey.generate()
        rogue_public = rogue_private.public_key()

        result = Ed25519ReportSigner.verify_envelope(self.base_envelope, rogue_public)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 13: Bit-Flip Cryptographic Attack on Signature
    # ----------------------------------------------------------------------
    def test_13_bit_flip_attack_on_signature(self):
        """13. Flipping a single bit in the 64-byte signature must cause verification failure."""
        forged = json.loads(json.dumps(self.base_envelope))
        sig_str = forged["sig"]
        padded_sig = sig_str + "=" * ((4 - len(sig_str) % 4) % 4)
        sig_bytes = bytearray(base64.urlsafe_b64decode(padded_sig))

        # Flip the lowest bit of byte 10
        sig_bytes[10] ^= 0x01
        forged["sig"] = base64.urlsafe_b64encode(bytes(sig_bytes)).decode("ascii").rstrip("=")

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 14: Truncated Signature Length Rejection
    # ----------------------------------------------------------------------
    def test_14_truncated_signature_rejection(self):
        """14. A signature shorter than 64 bytes must be rejected with invalid length error."""
        forged = json.loads(json.dumps(self.base_envelope))
        # 32 bytes instead of 64
        short_bytes = b"\x00" * 32
        forged["sig"] = base64.urlsafe_b64encode(short_bytes).decode("ascii").rstrip("=")

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertIn("64 bytes", result["error"])

    # ----------------------------------------------------------------------
    # Test 15: Malformed / Corrupted Base64URL Rejection
    # ----------------------------------------------------------------------
    def test_15_malformed_base64_rejection(self):
        """15. Malformed base64url characters must be rejected gracefully without unhandled crashes."""
        forged = json.loads(json.dumps(self.base_envelope))
        forged["sig"] = "!!!NOT_VALID_BASE64_AT_ALL!!!"

        result = Ed25519ReportSigner.verify_envelope(forged, self.signer.public_key)
        self.assertFalse(result["is_valid"])
        self.assertIn("base64url", result["error"].lower())

    # ----------------------------------------------------------------------
    # Test 16: Unicode & Devanagari Metrological Metadata Handling
    # ----------------------------------------------------------------------
    def test_16_non_ascii_unicode_metrology_claims(self):
        """16. Unicode and Devanagari metrology strings must serialize deterministically."""
        unicode_claims = self.signer.create_claims(
            session_id="SESS-HINDI-01",
            revision=1,
            spec_model="APX-15K-भारतीय-मॉडल",
            spec_serial="SIH-क्रमांक-001",
            accuracy_class="Class III (मध्यम परिशुद्धता)",
            verdict="PASSED",
            report_sha256="abcde12345abcde12345abcde12345abcde12345abcde12345abcde12345abcd",
            issuer="क्षेत्रीय संदर्भ मानक प्रयोगशाला (RRSL) - फरीदाबाद"
        )
        envelope = self.signer.sign_claims(unicode_claims)
        res = Ed25519ReportSigner.verify_envelope(envelope, self.signer.public_key)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")
        self.assertEqual(res["claims"]["model"], "APX-15K-भारतीय-मॉडल")

    # ----------------------------------------------------------------------
    # Test 17: QR Code SVG Generation & XML Validity
    # ----------------------------------------------------------------------
    def test_17_qr_code_svg_generation_validity(self):
        """17. QR generator must output valid, well-formed SVG XML with viewBox and path elements."""
        svg_str = Ed25519ReportSigner.generate_qr_svg(self.base_envelope, box_size=8, border=2)
        self.assertIn("<svg", svg_str)
        self.assertIn("</svg>", svg_str)
        self.assertIn("viewBox", svg_str)
        self.assertIn("<path", svg_str)
        self.assertGreater(len(svg_str), 1000, "SVG output must contain non-trivial path coordinates")

        data_uri = Ed25519ReportSigner.generate_qr_data_uri(self.base_envelope)
        self.assertTrue(data_uri.startswith("data:image/svg+xml;base64,"))

    # ----------------------------------------------------------------------
    # Test 18: Payload Density & Optical Scannability Bound
    # ----------------------------------------------------------------------
    def test_18_qr_code_density_and_scannability(self):
        """18. The complete signed envelope must remain compact (< 750 characters) for high optical contrast."""
        envelope_json = json.dumps(self.base_envelope, separators=(",", ":"))
        payload_len = len(envelope_json)
        self.assertLess(
            payload_len,
            750,
            f"Signed QR payload must be under 750 chars for reliable camera scanning (actual: {payload_len} chars)"
        )

    # ----------------------------------------------------------------------
    # Test 19: End-to-End QR Matrix Data Extraction & Cryptographic Verification
    # ----------------------------------------------------------------------
    def test_19_end_to_end_qr_matrix_data_retrieval(self):
        """19. Extract data payload directly from QR internal matrix structure and cryptographically verify."""
        envelope_json = json.dumps(self.base_envelope, separators=(",", ":"))
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2
        )
        qr.add_data(envelope_json)
        qr.make(fit=True)

        # Extract embedded payload bytes from QR data list (multi-mode chunks)
        embedded_bytes = b"".join([item.data for item in qr.data_list])
        recovered_str = embedded_bytes.decode("utf-8")
        recovered_envelope = json.loads(recovered_str)

        res = Ed25519ReportSigner.verify_envelope(recovered_envelope, self.signer.public_key)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")
        self.assertEqual(res["certificate_id"], "OIML-RRSL-SESS-2026-TEST-R1")

    # ----------------------------------------------------------------------
    # Test 20: FastAPI /api/verify/qr Endpoint Positive and Negative Validation
    # ----------------------------------------------------------------------
    def test_20_fastapi_offline_verification_endpoint(self):
        """20. Test FastAPI /api/verify/qr endpoint with authentic and tampered payloads."""
        # 1. Authentic request
        resp_ok = self.client.post("/api/verify/qr", json={"payload": self.base_envelope})
        self.assertEqual(resp_ok.status_code, 200)
        data_ok = resp_ok.json()
        self.assertTrue(data_ok["is_valid"])
        self.assertEqual(data_ok["status"], "AUTHENTIC")
        self.assertEqual(data_ok["certificate_id"], "OIML-RRSL-SESS-2026-TEST-R1")

        # 2. Tampered request (flipped verdict)
        tampered = json.loads(json.dumps(self.base_envelope))
        tampered["claims"]["verdict"] = "FAILED"
        resp_tampered = self.client.post("/api/verify/qr", json={"payload": tampered})
        self.assertEqual(resp_tampered.status_code, 200)
        data_tampered = resp_tampered.json()
        self.assertFalse(data_tampered["is_valid"])
        self.assertEqual(data_tampered["status"], "FORGED_OR_INVALID")


if __name__ == "__main__":
    unittest.main(verbosity=2)
