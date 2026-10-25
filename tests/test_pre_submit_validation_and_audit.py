"""
Comprehensive Test Suite for Statutory Compliance, Pre-Submit Validation, and Immutable Audit Trails
Smart India Hackathon SIH26035 — Non-Automatic Weighing Instruments (NAWI)

Validates:
1. Distinct Gateways on Login Page (Officer Authentication Gate vs Public Verification Portal)
2. Security Feedback Indicators (Verified R-76 Credentials, live cryptographic signature statuses, Legal Metrology Act 2009)
3. Pre-Submit Validation Routing Middleware: Rigid Table 6 tolerance enforcement across Classes I, II, III, and IIII
   - Blocking certificate signing and report saving on Table 6 tolerance violations
   - Permitting compliant instruments
4. Immutable Audit Trails: Strict append-only event logging and cryptographic hash chaining for Admin and Inspector actions
"""

import io
import json
import unittest
from decimal import Decimal
from pathlib import Path
import sys

# Ensure backend and src are in python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient
from api.main import (
    app,
    session,
    repo,
    DEFAULT_SPEC,
    SCALE_PRESETS,
    TestSessionWorkflow,
    InstrumentAssessment,
    _persist_session_state,
    check_table_6_tolerances_for_session
)
import api.main as main_mod
from core.nawi_engine import AccuracyClass, InstrumentSpecification


class TestPreSubmitValidationAndAudit(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        main_mod.session = TestSessionWorkflow(session_id="SESS-2026-001", spec=DEFAULT_SPEC)
        _persist_session_state()

    # =========================================================================
    # 1. UI/UX: Distinct Gateways (Login Page Separation)
    # =========================================================================

    def test_distinct_gateways_rendered_on_login_page(self):
        """Verify login page visually separates Officer Authentication Gate from Public Verification Portal."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Must contain the Distinct Gateways selector
        self.assertIn("Select Verification Gateway", html)
        self.assertIn("Public Verification Portal", html)
        self.assertIn("Officer Authentication Gate", html)

        # 2. Must distinguish access types: Citizen (Zero Auth) vs Officer (Level 2/3 Auth)
        self.assertIn("CITIZEN & TRADER ACCESS", html)
        self.assertIn("Zero Authentication", html)
        self.assertIn("STATUTORY ENFORCEMENT ONLY", html)
        self.assertIn("Level 2/3 High Security", html)

        # 3. Must link to the public portal switch
        self.assertIn("switchPortal('public')", html)

        # 4. In Public Portal, must provide return link to Officer Gate
        self.assertIn("Officer Authentication Gate &rarr;", html)

    # =========================================================================
    # 2. UI/UX & API: Security Feedback Indicators
    # =========================================================================

    def test_security_status_endpoint_and_indicators(self):
        """Verify statutory security feedback endpoint returns verified R-76 credentials and live signature status."""
        res = self.client.get("/api/inspector/security-status")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Statutory Act validation
        self.assertEqual(data["statutory_act"], "The Legal Metrology Act, 2009")
        self.assertIn("Section 15", data["statutory_section"])

        # Verified R-76 Credentials
        self.assertEqual(data["r76_credentials"]["status"], "VERIFIED")
        self.assertEqual(data["r76_credentials"]["badge"], "VERIFIED R-76 CREDENTIALS")
        self.assertIn("GOV-IN", data["r76_credentials"]["officer_id"])

        # Live Cryptographic Signature Status
        self.assertEqual(data["cryptographic_signature"]["status"], "OPERATIONAL")
        self.assertTrue(data["cryptographic_signature"]["live_signature_active"])
        self.assertIn("Ed25519", data["cryptographic_signature"]["algorithm"])
        self.assertTrue(len(data["cryptographic_signature"]["public_key_hex"]) == 64)

        # WELMEC 7.2 LRS software sealing
        self.assertIn(data["welmec_software_seal"]["status"], ["SEALED", "VALID"])

        # Table 6 enforcement mode
        self.assertEqual(data["metrology_engine"]["table_6_enforcement"], "RIGID_AUTOMATED_PRE_SUBMIT")

    def test_security_feedback_indicators_on_dashboards_html(self):
        """Verify visual security indicators are displayed on inspector dashboard and live testing views."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # Check for Verified R-76 Credentials badge
        self.assertIn("VERIFIED R-76 CREDENTIALS", html)
        self.assertIn("Statutory Metrology Compliance Environment", html)
        self.assertIn("The Legal Metrology Act, 2009", html)
        self.assertIn("Ed25519 Signer", html)
        self.assertIn("WELMEC 7.2 LRS", html)
        self.assertIn("Table 6 Engine", html)

    # =========================================================================
    # 3. Pre-Submit Validation: Automated Table 6 Enforcement Across Classes I - IIII
    # =========================================================================

    def test_pre_submit_validation_blocks_class_iii_tolerance_violation(self):
        """Verify Table 6 pre-submit validation blocks report saving and signing when Class III error exceeds MPE."""
        # Switch to Class III preset
        self.client.post("/api/session/select-preset/CLASS_III")
        self.client.post("/api/zero", json={"indication": "0.0", "delta_l": "2.5", "operator_id": "OP_TEST"})

        # Class III (15 kg, e=5 g): Load 5,000 g (1,000e) has MPE = +/- 1.0e = 5 g
        # Record an intentionally failing observation: Indication = 5020 g (error ~ +20 g, exceeds 5 g MPE)
        self.client.post("/api/observation", json={
            "step_index": 1,
            "load": "5000.0",
            "indication": "5020.0",
            "delta_l": "2.5",
            "direction": "ascending",
            "operator_id": "OP_TEST"
        })

        # Pre-Submit Check: must detect failure
        failures = check_table_6_tolerances_for_session(main_mod.session)
        self.assertTrue(len(failures) > 0)
        self.assertIn("Form 1 Step #1", failures[0]["test"])

        # Attempt to sign report -> Must be rejected with HTTP 422
        res_sign = self.client.post("/api/inspector/sign-report", json={
            "officer_id": "GOV-IN-7842",
            "inspector_name": "Inspector R. Verma"
        })
        self.assertEqual(res_sign.status_code, 422)
        err_sign = res_sign.json()
        self.assertIn("Pre-Submit Validation Failure", err_sign["detail"]["error"])

        # Attempt to save report as PASS to repository -> Must be rejected with HTTP 422
        res_save = self.client.post("/api/repository/save", json={
            "report_no": "TR-TEST-FAIL-01",
            "result": "PASS"
        })
        self.assertEqual(res_save.status_code, 422)

    def test_pre_submit_validation_blocks_class_i_tolerance_violation(self):
        """Verify Table 6 pre-submit validation blocks Class I Analytical Balance when error exceeds Table 6 MPE."""
        self.client.post("/api/session/select-preset/CLASS_I")
        self.client.post("/api/zero", json={"indication": "0.0", "delta_l": "0.0005", "operator_id": "OP_TEST"})

        # Class I (220 g, e=0.001 g): Load 100 g (100,000e) has MPE = +/- 1.0e = 0.001 g
        # Record failing observation: Indication = 100.010 g (error ~ 0.010 g, exceeds 0.001 g MPE)
        self.client.post("/api/observation", json={
            "step_index": 1,
            "load": "100.0",
            "indication": "100.010",
            "delta_l": "0.0005",
            "direction": "ascending",
            "operator_id": "OP_TEST"
        })

        # Signing must be blocked with HTTP 422
        res_sign = self.client.post("/api/inspector/sign-report", json={"officer_id": "GOV-IN-7842"})
        self.assertEqual(res_sign.status_code, 422)
        self.assertIn("Pre-Submit Validation Failure", res_sign.json()["detail"]["error"])

    def test_pre_submit_validation_blocks_class_ii_tolerance_violation(self):
        """Verify Table 6 pre-submit validation blocks Class II Precision Balance when error exceeds Table 6 MPE."""
        self.client.post("/api/session/select-preset/CLASS_II")
        self.client.post("/api/zero", json={"indication": "0.0", "delta_l": "0.005", "operator_id": "OP_TEST"})

        # Class II (600 g, e=0.01 g): Load 300 g (30,000e) has MPE = +/- 1.5e = 0.015 g
        # Record failing observation: Indication = 300.050 g (error ~ 0.050 g, exceeds 0.015 g MPE)
        self.client.post("/api/observation", json={
            "step_index": 1,
            "load": "300.0",
            "indication": "300.050",
            "delta_l": "0.005",
            "direction": "ascending",
            "operator_id": "OP_TEST"
        })

        res_sign = self.client.post("/api/inspector/sign-report", json={"officer_id": "GOV-IN-7842"})
        self.assertEqual(res_sign.status_code, 422)

    def test_pre_submit_validation_blocks_class_iiii_tolerance_violation(self):
        """Verify Table 6 pre-submit validation blocks Class IIII Platform Scale when error exceeds Table 6 MPE."""
        self.client.post("/api/session/select-preset/CLASS_IIII")
        self.client.post("/api/zero", json={"indication": "0.0", "delta_l": "10.0", "operator_id": "OP_TEST"})

        # Class IIII (50,000 kg, e=20 kg): Load 10,000 kg (500e) has MPE = +/- 1.5e = 30 kg
        # Record failing observation: Indication = 10100 kg (error ~ 100 kg, exceeds 30 kg MPE)
        self.client.post("/api/observation", json={
            "step_index": 1,
            "load": "10000.0",
            "indication": "10100.0",
            "delta_l": "10.0",
            "direction": "ascending",
            "operator_id": "OP_TEST"
        })

        res_sign = self.client.post("/api/inspector/sign-report", json={"officer_id": "GOV-IN-7842"})
        self.assertEqual(res_sign.status_code, 422)

    def test_pre_submit_validation_allows_compliant_instrument_sign_and_save(self):
        """Verify that a compliant instrument meeting all Table 6 tolerances succeeds and signs successfully."""
        # Load winning pitch data (fully passing Form 1, 3, 5, 15)
        self.client.post("/api/demo/load-full-suite")

        # Table 6 failures must be empty
        failures = check_table_6_tolerances_for_session(main_mod.session)
        self.assertEqual(failures, [])

        # Signing must succeed with HTTP 200
        res_sign = self.client.post("/api/inspector/sign-report", json={
            "officer_id": "GOV-IN-7842",
            "inspector_name": "Inspector R. Verma",
            "trader_name": "Metro Retailers Ltd",
            "trader_location": "APMC Yard 4"
        })
        self.assertEqual(res_sign.status_code, 200)
        sign_data = res_sign.json()
        self.assertEqual(sign_data["status"], "success")
        self.assertIn("TR-2026-", sign_data["certificate_no"])
        self.assertEqual(sign_data["certificate"]["verdict"], "PASS")

        # Saving report to repository must succeed
        res_save = self.client.post("/api/repository/save", json={
            "report_no": sign_data["certificate_no"],
            "result": "PASS",
            "status": "APPROVED"
        })
        self.assertEqual(res_save.status_code, 200)

    # =========================================================================
    # 4. Immutable Audit Trails: Strict Append-Only Logging & Cryptographic Integrity
    # =========================================================================

    def test_immutable_audit_logging_and_chain_verification(self):
        """Verify strict append-only audit logging across Admin and Inspector actions and verify Merkle hash chain."""
        # 1. Perform Inspector Login action
        login_res = self.client.post("/api/inspector/login", json={
            "email": "inspector@metrology.gov.in",
            "password": "PrecisionX#2026",
            "officer_id": "GOV-IN-7842"
        })
        self.assertEqual(login_res.status_code, 200)

        # 2. Perform Admin Login action
        admin_login_res = self.client.post("/api/admin/login", json={
            "username": "DR_SHARMA",
            "password": "PrecisionX@2026"
        })
        self.assertEqual(admin_login_res.status_code, 200)

        # 3. Perform Observation action
        self.client.post("/api/zero", json={"indication": "0.0", "delta_l": "2.5", "operator_id": "OP_VERMA"})

        # 4. Perform Admin Tolerance Reset action
        reset_res = self.client.post("/api/admin/tolerances/reset")
        self.assertEqual(reset_res.status_code, 200)

        # 5. Query Audit Logs endpoint
        logs_res = self.client.get("/api/admin/audit-logs?limit=50")
        self.assertEqual(logs_res.status_code, 200)
        logs = logs_res.json()
        self.assertTrue(len(logs) > 0)

        # Verify presence of logged actions
        actions = [l["action"] for l in logs]
        self.assertTrue(any("INSPECTOR_LOGIN" in a for a in actions))
        self.assertTrue(any("ADMIN_LOGIN" in a for a in actions))

        # 6. Verify Cryptographic Hash Chain Integrity
        verify_res = self.client.get("/api/admin/audit-logs/verify")
        self.assertEqual(verify_res.status_code, 200)
        verify_data = verify_res.json()
        self.assertTrue(verify_data["is_valid"])
        self.assertTrue(verify_data["database_chain_valid"])
        self.assertEqual(verify_data["status"], "ALL_HASHES_VERIFIED_VALID")


if __name__ == "__main__":
    unittest.main()
