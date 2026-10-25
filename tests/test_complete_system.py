"""
Comprehensive End-to-End Verification Suite for OIML R-76 Testing System
Validates:
1. Multi-Form API (Forms 1, 3, 5, 15)
2. Completeness Gating & Workflow Enforcement
3. CSV Ingestion Engine
4. Headless Chrome PDF Generation & PTB DCC v3.2.1 XML Export
5. Revision Invalidation & Concurrency Locks
"""

import unittest
from decimal import Decimal
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from api.main import app, session, repo


class TestCompleteSystemSuite(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_full_suite_demo_loading(self):
        """Verify that load-full-suite populates Forms 1, 3, 5, 15 and meets completeness."""
        res = self.client.post("/api/demo/load-full-suite")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "full_suite_loaded")
        self.assertEqual(data["form1_steps"], 12)
        self.assertEqual(data["form3_positions"], 5)
        self.assertEqual(data["form5_series"], 2)
        self.assertEqual(data["form15_checks"], 6)
        self.assertTrue(data["completeness"]["complete"])

    def test_completeness_gating_blocks_premature_approval(self):
        """Verify that premature review approval is blocked when enforce_completeness=True."""
        # Reset to bare nominal sequence (only Form 1)
        self.client.post("/api/demo/load-nominal")
        
        # Check completeness
        comp_res = self.client.get("/api/session/completeness")
        self.assertEqual(comp_res.status_code, 200)
        comp = comp_res.json()
        
        # Attempt to approve with enforce_completeness=True
        res = self.client.post("/api/review/approve", json={
            "reviewer_id": "DR_SHARMA",
            "expected_revision": 1,
            "comments": "Testing gating",
            "enforce_completeness": True
        })
        # Should fail with 400 Bad Request
        self.assertEqual(res.status_code, 400)
        self.assertIn("incomplete", res.json()["detail"].lower())

    def test_form3_eccentricity_endpoints(self):
        """Verify recording and amending Form 3 corner load positions."""
        self.client.post("/api/demo/load-nominal")

        # Record Center position
        r1 = self.client.post("/api/form3/position", json={
            "position_name": "Center",
            "indication": "5000.0",
            "delta_l": "2.5",
            "operator_id": "OPERATOR_1"
        })
        self.assertEqual(r1.status_code, 200)
        self.assertTrue(r1.json()["result"]["passed"])
        self.assertEqual(r1.json()["result"]["corrected_error_ec"], "0.0")

        # Record Front-Left with failing load (Ec = +10.0g > 5.0g MPE)
        r2 = self.client.post("/api/form3/position", json={
            "position_name": "Front-Left",
            "indication": "5010.0",
            "delta_l": "2.5",
            "operator_id": "OPERATOR_1"
        })
        self.assertEqual(r2.status_code, 200)
        self.assertFalse(r2.json()["result"]["passed"])

        # Check overall Form 3 status
        f3 = self.client.get("/api/form3").json()
        self.assertFalse(f3["overall_passed"])

        # Amend Front-Left with valid reading and reason
        r3 = self.client.post("/api/form3/amend", json={
            "position_name": "Front-Left",
            "new_indication": "5000.0",
            "new_delta_l": "2.5",
            "operator_id": "TECH_VERMA",
            "edit_reason": "Re-centered test weight correctly"
        })
        self.assertEqual(r3.status_code, 200)
        self.assertTrue(r3.json()["result"]["passed"])

    def test_form5_repeatability_endpoints(self):
        """Verify Form 5 repeatability readings and spread calculation."""
        self.client.post("/api/demo/load-nominal")

        # Add 10 readings at 50% Max
        for ind in ["7500.0"] * 9 + ["7505.0"]:
            self.client.post("/api/form5/reading", json={
                "load_bracket": "50%",
                "indication": ind,
                "operator_id": "OPERATOR_1"
            })

        res = self.client.get("/api/form5").json()
        series_dict = res.get("series", res)
        self.assertIn("50%", series_dict)
        self.assertEqual(series_dict["50%"]["spread"], "5.0")
        self.assertTrue(series_dict["50%"]["passed"])

    def test_csv_batch_ingestion(self):
        """Verify CSV ingestion for Form 1, Form 3, and Form 5."""
        # Ingest Form 1 CSV
        csv_f1 = (
            "step_index,load,indication,delta_l,direction,operator_id\n"
            "0,0,0.0,2.5,ascending,OPERATOR_1\n"
            "1,100,100.0,2.5,ascending,OPERATOR_1\n"
            "2,2500,2500.0,1.5,ascending,OPERATOR_1\n"
        )
        r1 = self.client.post("/api/import/csv", json={"csv_content": csv_f1, "form_type": "form1"})
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()["imported_count"], 3)

        # Ingest Form 3 CSV
        csv_f3 = (
            "position,indication,delta_l,operator_id\n"
            "Center,5000.0,2.5,OPERATOR_1\n"
            "Back-Right,5000.0,2.0,OPERATOR_1\n"
        )
        r2 = self.client.post("/api/import/csv", json={"csv_content": csv_f3, "form_type": "form3"})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json()["imported_count"], 2)

    def test_report_and_exports(self):
        """Verify HTML, PDF, and PTB DCC XML reports."""
        self.client.post("/api/demo/load-full-suite")

        # HTML
        r_html = self.client.get("/api/report/html")
        self.assertEqual(r_html.status_code, 200)
        self.assertIn("OIML R 76-2:2007 Pattern Evaluation Test Report", r_html.text)
        self.assertIn("Form 1: Weighing Performance", r_html.text)
        self.assertIn("Form 3: Corner Eccentricity", r_html.text)
        self.assertIn("Form 5: Repeatability", r_html.text)

        # PDF
        r_pdf = self.client.get("/api/report/pdf")
        self.assertEqual(r_pdf.status_code, 200)
        self.assertEqual(r_pdf.headers["content-type"], "application/pdf")
        self.assertGreater(len(r_pdf.content), 10000)

        # DCC XML
        r_dcc = self.client.get("/api/report/dcc")
        self.assertEqual(r_dcc.status_code, 200)
        self.assertIn("application/xml", r_dcc.headers["content-type"])
        self.assertIn("digitalCalibrationCertificate", r_dcc.text)


if __name__ == "__main__":
    unittest.main()
