"""
Integration Tests for Step 5: Interactive Workbench UI & Jury Demonstration Orchestration

Tests the 4 pillars of the winning SIH jury pitch:
1. 1-Click Load Winning Pitch Data (Forms 1, 3, 5, 15 complete session).
2. Interactive MPE Trumpet Curve calculations & envelope validation.
3. Revision Anti-Rollback lifecycle, freezing approved snapshots, and invalidation.
4. UI DOM template integrity & toolbar element presence.
"""

import unittest
import sys
from pathlib import Path
from decimal import Decimal

# Add src to python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from api.main import app, DEFAULT_SPEC, TestSessionWorkflow, _persist_session_state
import api.main as main_mod


class TestJuryDemoWorkflow(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        main_mod.session = TestSessionWorkflow(session_id="SESS-2026-001", spec=DEFAULT_SPEC)
        _persist_session_state()

    def test_01_load_winning_pitch_data(self):
        """Test 1-click loading of complete Class III 15kg NAWI test session across all forms."""
        # Call the winning pitch load endpoint (test both aliases)
        res = self.client.post("/api/demo/load_pitch_data")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "full_suite_loaded")
        self.assertGreaterEqual(data["form1_steps"], 12)
        self.assertEqual(data["form3_positions"], 5)
        self.assertEqual(data["form5_series"], 2)
        self.assertEqual(data["form15_checks"], 6)

        # Inspect session state
        res_sess = self.client.get("/api/session")
        self.assertEqual(res_sess.status_code, 200)
        sess = res_sess.json()
        self.assertEqual(sess["instrument_verdict"], "PASSED")
        self.assertEqual(sess["review_status"], "DRAFT")
        self.assertEqual(sess["current_revision"], 1)

        # Verify completeness gating passes 100%
        completeness = sess["completeness"]
        self.assertTrue(completeness["complete"])
        self.assertEqual(completeness["form1_steps_count"], 12)
        self.assertEqual(len(completeness["form3_positions_recorded"]), 5)
        self.assertEqual(completeness["form5_series_counts"]["50%"], 10)
        self.assertEqual(completeness["form5_series_counts"]["100%"], 10)
        self.assertEqual(completeness["software_checks_count"], 6)
        self.assertEqual(len(completeness["missing_requirements"]), 0)

    def test_02_mpe_trumpet_curve_envelope_and_corridor(self):
        """Test statutory MPE trumpet curve data and error corridor adherence (OIML R 76-1)."""
        self.client.post("/api/demo/load-full-suite")
        res = self.client.get("/api/session")
        sess = res.json()
        calcs = sess["calculations"]
        self.assertGreaterEqual(len(calcs), 12)

        # Map step_index to load from observations
        obs_by_step = {obs["step_index"]: Decimal(str(obs["load"])) for obs in sess["observations"]}

        # e = 5g for Class III 15kg scale
        for calc in calcs:
            s_idx = calc.get("step_index")
            if s_idx == 0 or s_idx not in obs_by_step:
                continue
            load = obs_by_step[s_idx]
            ec = Decimal(str(calc["corrected_error_ec"]))
            mpe = Decimal(str(calc["mpe"]))

            # Verify statutory MPE tolerance envelope tier:
            # 0 <= m <= 500e (2500g): +/- 0.5e (+/- 2.5g)
            # 500e < m <= 2000e (10000g): +/- 1.0e (+/- 5.0g)
            # 2000e < m <= 3000e (15000g): +/- 1.5e (+/- 7.5g)
            if load <= Decimal("2500"):
                expected_mpe = Decimal("2.5")
            elif load <= Decimal("10000"):
                expected_mpe = Decimal("5.0")
            else:
                expected_mpe = Decimal("7.5")

            self.assertEqual(mpe, expected_mpe, f"Step {s_idx} load {load}g expected MPE {expected_mpe} but got {mpe}")
            # All nominal errors in pitch data must fall strictly within tolerance envelope
            self.assertLessEqual(abs(ec), mpe, f"Error {ec} exceeds MPE {mpe} at load {load}g")
            self.assertTrue(calc["passed"])

            # Verify positive safety margin
            margin = mpe - abs(ec)
            self.assertGreaterEqual(margin, Decimal("0.0"))

    def test_03_revision_anti_rollback_and_audit_lifecycle(self):
        """Test ISO/IEC 17025 anti-rollback: approved revision freeze, amendment invalidation to REQUIRES_RE_REVIEW, and audit history preservation."""
        # 1. Populate full session
        self.client.post("/api/demo/load-full-suite")

        # 2. Lock & Certify Revision 1 as approved legal metrology report
        res_appr = self.client.post("/api/review/approve", json={
            "reviewer_id": "SCIENTIST_DR_SHARMA",
            "expected_revision": 1,
            "comments": "Certified OIML R 76-1:2006 Scheme A conformance.",
            "enforce_completeness": True
        })
        self.assertEqual(res_appr.status_code, 200)
        appr_data = res_appr.json()
        self.assertEqual(appr_data["status"], "approved")
        self.assertEqual(appr_data["snapshot"]["revision_number"], 1)
        self.assertEqual(appr_data["snapshot"]["instrument_verdict"], "PASSED")

        # Check session is now APPROVED with 1 archived revision
        sess1 = self.client.get("/api/session").json()
        self.assertEqual(sess1["review_status"], "APPROVED")
        self.assertEqual(len(sess1["archived_revisions"]), 1)
        self.assertEqual(sess1["archived_revisions"][0]["revision_number"], 1)
        self.assertEqual(sess1["archived_revisions"][0]["instrument_verdict"], "PASSED")

        # 3. Simulate Operator amendment at Step 3 (2500g): 2500.0g -> 2510.0g (+11.0g error > 2.5g MPE)
        res_amend = self.client.post("/api/amend", json={
            "step_index": 3,
            "new_indication": "2510.0",
            "new_delta_l": "2.5",
            "operator_id": "TECH_VERMA",
            "edit_reason": "Bench re-check indicates calibration error at 500e load point (2500g)"
        })
        self.assertEqual(res_amend.status_code, 200)
        amend_res = res_amend.json()
        self.assertEqual(amend_res["new_revision"], 2)
        self.assertEqual(amend_res["review_status"], "REQUIRES_RE_REVIEW")
        self.assertEqual(amend_res["instrument_verdict"], "FAILED")

        # 4. Anti-Rollback Proof: Verify Revision 1 remains frozen in archived_revisions with original PASSED verdict
        sess2 = self.client.get("/api/session").json()
        self.assertEqual(sess2["current_revision"], 2)
        self.assertEqual(sess2["review_status"], "REQUIRES_RE_REVIEW")
        self.assertEqual(sess2["instrument_verdict"], "FAILED")

        # Archived revision #1 must NOT have been overwritten or mutated
        self.assertEqual(len(sess2["archived_revisions"]), 1)
        self.assertEqual(sess2["archived_revisions"][0]["revision_number"], 1)
        self.assertEqual(sess2["archived_revisions"][0]["instrument_verdict"], "PASSED")
        self.assertEqual(sess2["archived_revisions"][0]["reviewer_id"], "SCIENTIST_DR_SHARMA")

        # Verify observation history contains both initial entry and amended entry with audit reason
        history = sess2.get("observation_history", [])
        self.assertGreater(len(history), 0)
        amended_entries = [h for h in history if h.get("step_index") == 3 and h.get("edit_reason")]
        self.assertTrue(len(amended_entries) >= 1)
        self.assertIn("500e load point", amended_entries[0]["edit_reason"])

    def test_04_ui_dom_and_workbench_elements(self):
        """Verify that the HTML workbench contains all Step 5 jury pitch elements, MPE curve SVG, and revision audit controls."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Pitch Toolbar Button
        self.assertIn("btn-load-pitch-data", html)
        self.assertIn("Load Winning Pitch Data", html)

        # 2. Interactive MPE Trumpet Curve SVG Canvas & KPI Summary Ribbon
        self.assertIn("trumpetChartSvg", html)
        self.assertIn("curveTotalPoints", html)
        self.assertIn("curveMaxError", html)
        self.assertIn("curveMinMargin", html)
        self.assertIn("curveEnvelopeStatus", html)

        # 3. Revision Anti-Rollback Audit Card & Demo Actions
        self.assertIn("revisionAuditCard", html)
        self.assertIn("btn-demo-lock-rev1", html)
        self.assertIn("btn-demo-simulate-amend", html)
        self.assertIn("revisionAlertBanner", html)
        self.assertIn("archivedRevisionsTableBody", html)
        self.assertIn("observationHistoryTableBody", html)


if __name__ == "__main__":
    unittest.main()
