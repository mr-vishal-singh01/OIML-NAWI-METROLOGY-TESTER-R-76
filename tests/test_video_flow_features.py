"""Tests for Video Demonstration Features (Portal Showcase, Inspector Login, Setup, Guided Testing, and Digital Repository).

Validates the complete workflow demonstrated in the video:
1. Inspector authentication (/api/inspector/login)
2. Instrument & Lab conditions configuration (/api/session/setup)
3. Digital repository queries, status filters, and session archival (/api/repository/*)
4. UI DOM completeness matching reference presentation
"""

import unittest
from fastapi.testclient import TestClient
from backend.api.main import app


class TestVideoFlowFeatures(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_inspector_login_endpoint(self):
        """Test authentication for authorized metrology inspector."""
        # 1. Valid credentials
        res = self.client.post("/api/inspector/login", json={
            "email": "inspector@metrology.gov.in",
            "password": "PrecisionX#2026",
            "officer_id": "GOV-IN-7842"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["officer_id"], "GOV-IN-7842")
        self.assertEqual(data["role"], "LEGAL_METROLOGY_INSPECTOR")
        self.assertIn("token", data)
        token = data["token"]

        # Verify active session query
        res_sess = self.client.get("/api/inspector/session", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res_sess.status_code, 200)
        self.assertTrue(res_sess.json()["authenticated"])
        self.assertEqual(res_sess.json()["officer_id"], "GOV-IN-7842")

        # Test logout session invalidation
        res_logout = self.client.post("/api/inspector/logout", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res_logout.status_code, 200)
        self.assertEqual(res_logout.json()["status"], "logged_out")

        # Session should now be unauthenticated
        res_sess_after = self.client.get("/api/inspector/session", headers={"Authorization": f"Bearer {token}"})
        self.assertFalse(res_sess_after.json()["authenticated"])

        # 2. Invalid credentials
        res_bad = self.client.post("/api/inspector/login", json={
            "email": "intruder@unknown.com",
            "password": "WrongPassword",
            "officer_id": "INVALID-000"
        })
        self.assertEqual(res_bad.status_code, 200)
        data_bad = res_bad.json()
        self.assertFalse(data_bad["authenticated"])

    def test_session_instrument_and_lab_setup(self):
        """Test configuring instrument specifications and laboratory conditions."""
        setup_payload = {
            "manufacturer": "Mettler Toledo / Essae",
            "model": "XP-15K Industrial Bench",
            "accuracy_class": "CLASS_III",
            "serial_number": "SN-2026-IND-8849",
            "max_capacity_kg": 15.0,
            "min_capacity_kg": 0.1,
            "verification_interval_e": 0.005,
            "actual_interval_d": 0.005,
            "temperature_c": 23.4,
            "relative_humidity_pct": 48.5,
            "pressure_hpa": 1013.2,
            "lab_location": "Regional Reference Standards Laboratory (RRSL)"
        }
        res = self.client.post("/api/session/setup", json=setup_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["instrument"]["serial_number"], "SN-2026-IND-8849")
        self.assertEqual(data["laboratory_conditions"]["temperature_c"], 23.4)

        # Verify active session has updated details
        sess = self.client.get("/api/session").json()
        self.assertEqual(sess["instrument_info"]["serial_number"], "SN-2026-IND-8849")
        self.assertEqual(sess["environmental_conditions"]["temperature_c"], 23.4)

    def test_repository_records_and_filtering(self):
        """Test digital repository search, filtering by status, and date matching."""
        # 1. Retrieve all records
        res = self.client.get("/api/repository/records")
        self.assertEqual(res.status_code, 200)
        records = res.json()
        self.assertIsInstance(records, list)
        self.assertGreaterEqual(len(records), 5)

        # Check expected record structure from video
        rec0 = records[0]
        self.assertIn("report_no", rec0)
        self.assertIn("instrument", rec0)
        self.assertIn("status", rec0)
        self.assertIn("result", rec0)

        # 2. Filter by Status: APPROVED
        res_approved = self.client.get("/api/repository/records?status=APPROVED")
        self.assertEqual(res_approved.status_code, 200)
        approved_records = res_approved.json()
        for r in approved_records:
            self.assertEqual(r["status"], "APPROVED")

        # 3. Filter by Status: REJECTED
        res_rejected = self.client.get("/api/repository/records?status=REJECTED")
        self.assertEqual(res_rejected.status_code, 200)
        rejected_records = res_rejected.json()
        for r in rejected_records:
            self.assertEqual(r["status"], "REJECTED")

        # 4. Search query
        res_search = self.client.get("/api/repository/records?q=Essae")
        self.assertEqual(res_search.status_code, 200)
        essae_records = res_search.json()
        self.assertTrue(any("Essae" in r["instrument"] or "Essae" in r.get("manufacturer", "") for r in essae_records))

    def test_repository_session_archive(self):
        """Test archiving the current test session into the digital repository."""
        res = self.client.post("/api/repository/save")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("report_no", data)

        # Ensure the newly saved record appears in repository query
        res_list = self.client.get("/api/repository/records?q=" + data["report_no"])
        self.assertEqual(res_list.status_code, 200)
        matches = res_list.json()
        self.assertTrue(len(matches) >= 1)
        self.assertEqual(matches[0]["report_no"], data["report_no"])

    def test_ui_html_contains_all_video_sections(self):
        """Verify the HTML contains all 5 video presentation views and interaction elements."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Showcase Landing Hero
        self.assertIn('id="tab-showcase"', html)
        self.assertIn("Precision testing", html)
        self.assertIn("without the paperwork", html)
        self.assertIn("OIML R 76 COMPLIANT", html)
        self.assertIn("5,200+", html)
        self.assertIn("99.9%", html)

        # 2. Inspector Authentication
        self.assertIn('id="tab-login"', html)
        self.assertIn('id="inspectorEmail"', html)
        self.assertIn('id="inspectorPassword"', html)
        self.assertIn('id="inspectorOfficerId"', html)

        # 3. Instrument & Lab Setup
        self.assertIn('id="tab-setup"', html)
        self.assertIn('id="setupManufacturer"', html)
        self.assertIn('id="setupModel"', html)
        self.assertIn('id="setupMax"', html)
        self.assertIn('id="setupTemp"', html)
        self.assertIn("Proceed to Testing", html)

        # 4. Guided Testing Suite
        self.assertIn('id="tab-testing"', html)
        self.assertIn('id="subtab-weighing"', html)
        self.assertIn('id="subtab-repeatability"', html)
        self.assertIn('id="subtab-eccentricity"', html)
        self.assertIn('id="subtab-zerotare"', html)
        self.assertIn('id="guidedWeighingTableBody"', html)

        # 5. Digital Repository
        self.assertIn('id="tab-repository"', html)
        self.assertIn('id="repoSearchInput"', html)
        self.assertIn('id="repoStatusFilter"', html)
        self.assertIn('id="repoDateFilter"', html)
        self.assertIn('id="repositoryTableBody"', html)

        # 6. Theme and Pitch Controls
        self.assertIn('id="btnThemeToggle"', html)
        self.assertIn("theme-emerald", html)
        self.assertIn("Pitch Flow", html)


if __name__ == "__main__":
    unittest.main()
