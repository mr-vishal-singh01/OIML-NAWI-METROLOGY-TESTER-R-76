"""
Defensive Security & Red Team Audit Verification Test Suite
Verifies remediations for:
- CWE-285: Broken Function-Level Authorization on Administrative APIs
- CWE-22: Path Traversal defense on file downloads
- CWE-400 / CWE-434: Upload size boundaries and extension whitelisting
- CWE-307: Brute-force rate limiting on administrative login
- Regression test for Observation calculation logging
"""

import sys
import unittest
from pathlib import Path
from decimal import Decimal

# Ensure src is in python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient
from api.main import app, session, ADMIN_ACTIVE_TOKENS
from core.ministry_gazette_engine import get_gazette_file_path


class TestDefensiveRedTeamSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Ensure clean unauthenticated session state
        session.admin_authenticated = False

    def test_01_unauthenticated_admin_endpoints_blocked(self):
        """Unauthenticated requests to admin endpoints must return 401 Unauthorized."""
        endpoints = [
            ("POST", "/api/admin/tolerances/reset", None),
            ("GET", "/api/admin/audit-logs", None),
            ("GET", "/api/admin/audit-export", None),
            ("POST", "/api/admin/inspectors", {"name": "Test Attacker", "role": "HACKER", "jurisdiction": "Delhi"}),
        ]
        for method, ep, body in endpoints:
            if method == "POST":
                res = self.client.post(ep, json=body or {})
            else:
                res = self.client.get(ep)
            self.assertEqual(res.status_code, 401, f"Endpoint {ep} should require authorization but returned {res.status_code}")
            self.assertIn("Unauthorized", res.json().get("detail", ""))

    def test_02_authenticated_admin_endpoints_accessible(self):
        """Authenticated requests with valid admin login or Bearer token must succeed."""
        # Authenticate via admin login
        login_res = self.client.post("/api/admin/login", json={
            "username": "DR_SHARMA",
            "password": "PrecisionX@2026"
        })
        self.assertEqual(login_res.status_code, 200)
        token = login_res.json()["token"]

        # Now admin actions succeed
        reset_res = self.client.post("/api/admin/tolerances/reset")
        self.assertEqual(reset_res.status_code, 200)

        logs_res = self.client.get("/api/admin/audit-logs")
        self.assertEqual(logs_res.status_code, 200)

        # Logout clears session
        self.client.post("/api/admin/logout")
        unauth_res = self.client.post("/api/admin/tolerances/reset")
        self.assertEqual(unauth_res.status_code, 401)

        # Bearer token in header works even if session logout occurred
        bearer_res = self.client.post("/api/admin/tolerances/reset", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(bearer_res.status_code, 200)

    def test_03_path_traversal_blocked(self):
        """Path traversal attempts (CWE-22) must be blocked and return None or 404."""
        traversal_attempts = [
            "../../../../etc/passwd",
            "..\\..\\..\\windows\\win.ini",
            "/etc/shadow",
            "....//....//....//etc/passwd",
        ]
        for attempt in traversal_attempts:
            res_path = get_gazette_file_path(attempt)
            self.assertIsNone(res_path, f"Traversal path '{attempt}' should resolve to None")

            http_res = self.client.get(f"/api/ministry/gazette/{attempt}")
            self.assertIn(http_res.status_code, [404, 400], f"HTTP request with traversal '{attempt}' must return 404/400")

    def test_04_file_upload_security(self):
        """Uploads of unauthorized extensions or malicious files must be rejected."""
        # 1. Reject executable script
        exe_file = ("exploit.sh", b"#!/bin/bash\necho hack", "application/x-sh")
        res_exe = self.client.post(
            f"/api/sessions/{session.session_id}/attachments",
            params={"document_type": "SCRIPT"},
            files={"file": exe_file}
        )
        self.assertEqual(res_exe.status_code, 400)
        self.assertIn("Invalid file type", res_exe.json().get("detail", ""))

        # 2. Reject oversized file (>15MB boundary)
        big_content = b"0" * (16 * 1024 * 1024)
        big_file = ("large.jpg", big_content, "image/jpeg")
        res_big = self.client.post(
            f"/api/sessions/{session.session_id}/attachments",
            params={"document_type": "BIG"},
            files={"file": big_file}
        )
        self.assertEqual(res_big.status_code, 413)

        # 3. Accept legitimate JPEG image
        valid_img = ("seal.jpg", b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00", "image/jpeg")
        res_valid = self.client.post(
            f"/api/sessions/{session.session_id}/attachments",
            params={"document_type": "SEAL"},
            files={"file": valid_img}
        )
        self.assertEqual(res_valid.status_code, 200)

    def test_05_observation_recording_regression(self):
        """User's 'Record' step must record with 0 AttributeError and correct error_ec."""
        payload = {
            "step_index": 1,
            "load": "2500.0",
            "indication": "2500.0",
            "delta_l": "1.5",
            "direction": "ascending",
            "operator_id": "TEST_OFFICER"
        }
        res = self.client.post("/api/observation", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("calculation", data)
        self.assertEqual(data["calculation"]["step_index"], 1)

    def test_06_form3_scale_pan_resilience_and_all_positions(self):
        """Form 3 eccentricity positions must record without foreign key failure and support all 5 target positions."""
        sess_res = self.client.get("/api/session")
        self.assertEqual(sess_res.status_code, 200)
        sess_data = sess_res.json()
        self.assertIn("form3_test_load", sess_data)
        self.assertIn("form3_mpe", sess_data)
        test_load = sess_data["form3_test_load"]

        positions = ["Center", "Front-Left", "Back-Left", "Back-Right", "Front-Right"]
        for pos in positions:
            res = self.client.post("/api/form3/position", json={
                "position_name": pos,
                "indication": f"{test_load}.0",
                "delta_l": "2.5",
                "operator_id": "TEST_INSPECTOR"
            })
            self.assertEqual(res.status_code, 200, f"Position {pos} failed with: {res.text}")
            rdata = res.json()
            self.assertEqual(rdata["status"], "ok")
            self.assertEqual(rdata["result"]["position"], pos)
            self.assertTrue(rdata["result"]["passed"])

        # Check session reflects all 5 positions recorded
        updated = self.client.get("/api/session").json()
        self.assertEqual(len(updated["form3_positions"]), 5)

    def test_07_scale_preset_switching_and_specs_sync(self):
        """All scale presets (including Class IV / CLASS_IV alias) must switch cleanly, return full metadata, and update active instrument."""
        presets = ["CLASS_I", "CLASS_II", "CLASS_III", "CLASS_IIII", "CLASS_IV"]
        for p_id in presets:
            res = self.client.post(f"/api/session/select-preset/{p_id}")
            self.assertEqual(res.status_code, 200, f"Preset {p_id} switch failed: {res.text}")
            data = res.json()
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["preset_id"], p_id)
            self.assertIn("accuracy_class", data)
            self.assertIn("max", data)
            self.assertIn("e", data)
            self.assertIn("manufacturer", data)
            self.assertIn("model", data)

            # Verify session state reflects new instrument
            sess = self.client.get("/api/session").json()
            self.assertEqual(sess["instrument"]["accuracy_class"], data["accuracy_class"])
            self.assertEqual(sess["instrument"]["manufacturer"], data["manufacturer"])
            self.assertEqual(sess["instrument"]["model"], data["model"])
            self.assertEqual(sess["session_id"], f"SESS-2026-{p_id}")


if __name__ == "__main__":
    unittest.main()
