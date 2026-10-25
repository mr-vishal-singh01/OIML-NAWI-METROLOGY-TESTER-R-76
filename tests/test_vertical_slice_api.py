"""
Integration Test for NAWI Weighing-Performance Vertical Slice API
Verifies the complete HTTP API and Revision Lifecycle end-to-end:
1. Load nominal sequence -> All 8 pass.
2. Reviewer approves Revision 1 -> State = APPROVED.
3. Operator amends Step 3 (2500g) to 2510.0g with reason.
4. Recalculation executes: Ec = +11.0g > 2.5g -> FAILED.
5. Invalidation: State becomes REQUIRES_RE_REVIEW, Revision advances to 2.
6. Optimistic locking: Approval with expected_revision=1 is rejected (409 Conflict).
7. Legitimate approval of Revision 2 succeeds.
8. Report export reflects the frozen failure snapshot.
"""

import unittest
import sys
from pathlib import Path

# Add src to python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from api.main import app, DEFAULT_SPEC, TestSessionWorkflow, _persist_session_state
import api.main as main_mod


class TestVerticalSliceAPI(unittest.TestCase):

    def setUp(self):
        main_mod.session = TestSessionWorkflow(session_id="SESS-2026-001", spec=DEFAULT_SPEC)
        _persist_session_state()
        self.client = TestClient(app)

    def test_full_api_weighing_slice_lifecycle(self):
        # 1. Check initial session
        res = self.client.get("/api/session")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["review_status"], "DRAFT")

        # 2. Load nominal sequence
        res = self.client.post("/api/demo/load-nominal")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/session")
        data = res.json()
        self.assertEqual(data["instrument_verdict"], "PASSED")
        self.assertEqual(data["current_revision"], 1)
        self.assertEqual(len(data["calculations"]), 8)

        # 3. Reviewer approves Revision 1
        res = self.client.post("/api/review/approve", json={
            "reviewer_id": "SCIENTIST_DR_SHARMA",
            "expected_revision": 1,
            "comments": "Initial nominal pass verified."
        })
        self.assertEqual(res.status_code, 200)
        snap = res.json()["snapshot"]
        self.assertEqual(snap["revision_number"], 1)
        self.assertEqual(snap["instrument_verdict"], "PASSED")

        # Verify session state is now APPROVED
        res = self.client.get("/api/session")
        self.assertEqual(res.json()["review_status"], "APPROVED")

        # 4. Operator amends Step 3 (2500g)
        # Original: I = 2500.0, dL = 1.5 -> Ec = +1.0g (PASS)
        # Amended: I = 2510.0, dL = 1.5 -> P = 2511.0 -> Ec = +11.0g (FAIL, MPE = +/- 2.5g)
        res = self.client.post("/api/amend", json={
            "step_index": 3,
            "new_indication": "2510.0",
            "new_delta_l": "1.5",
            "operator_id": "TECH_VERMA",
            "edit_reason": "Corrected transcription error against bench field book entry"
        })
        self.assertEqual(res.status_code, 200)
        amend_data = res.json()
        self.assertEqual(amend_data["new_revision"], 2)
        self.assertEqual(amend_data["review_status"], "REQUIRES_RE_REVIEW")
        self.assertEqual(amend_data["instrument_verdict"], "FAILED")
        calc = amend_data["calculation"]
        self.assertEqual(calc["corrected_error_ec"], "11.0")
        self.assertFalse(calc["passed"])

        # 5. Concurrency check: Stale approval rejection (HTTP 409)
        res = self.client.post("/api/review/approve", json={
            "reviewer_id": "SCIENTIST_DR_SHARMA",
            "expected_revision": 1,
            "comments": "Attempting to approve old revision"
        })
        self.assertEqual(res.status_code, 409)
        self.assertIn("Concurrency Conflict", res.json()["detail"])

        # 6. Valid approval of Revision 2
        res = self.client.post("/api/review/approve", json={
            "reviewer_id": "SCIENTIST_DR_SHARMA",
            "expected_revision": 2,
            "comments": "Revision 2 approved: verified out-of-tolerance failure."
        })
        self.assertEqual(res.status_code, 200)
        snap2 = res.json()["snapshot"]
        self.assertEqual(snap2["revision_number"], 2)
        self.assertEqual(snap2["instrument_verdict"], "FAILED")

        # 7. Check HTML report contains the failure verdict and comments
        res = self.client.get("/api/report/html")
        self.assertEqual(res.status_code, 200)
        html_body = res.text
        self.assertIn("OVERALL INSTRUMENT VERDICT: FAILED", html_body)
        self.assertIn("Revision #2", html_body)
        # 8. Check DOCX report generation
        res = self.client.get("/api/report/docx")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.assertGreater(len(res.content), 2000)

    def test_scale_presets_and_hardware_simulation(self):
        # 1. Fetch presets
        res = self.client.get("/api/presets")
        self.assertEqual(res.status_code, 200)
        presets = res.json()["presets"]
        self.assertEqual(len(presets), 4)
        preset_ids = [p["id"] for p in presets]
        self.assertIn("CLASS_I", preset_ids)
        self.assertIn("CLASS_II", preset_ids)
        self.assertIn("CLASS_III", preset_ids)
        self.assertIn("CLASS_IIII", preset_ids)

        # 2. Select Class I analytical balance preset
        res = self.client.post("/api/session/select-preset/CLASS_I")
        self.assertEqual(res.status_code, 200)
        p_data = res.json()
        self.assertEqual(p_data["accuracy_class"], "Class I")
        self.assertEqual(p_data["max"], "220")
        self.assertEqual(p_data["e"], "0.001")

        # 3. Simulate hardware acquisition over MT-SICS
        res = self.client.get("/api/hardware/simulate?target_weight=150.0&protocol=mt_sics&unit=g")
        self.assertEqual(res.status_code, 200)
        hw_data = res.json()
        self.assertEqual(hw_data["final_indication"], 150.0)
        self.assertTrue(hw_data["is_stable"])
        self.assertEqual(len(hw_data["frames"]), 6)
        self.assertIn("S S", hw_data["raw_final"])

    def test_evidence_vault_lifecycle(self):
        # 1. Upload mock photo evidence
        fake_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
        res = self.client.post(
            "/api/sessions/SESS-2026-001/attachments",
            data={"document_type": "NAMEPLATE"},
            files={"file": ("test_nameplate.png", fake_bytes, "image/png")}
        )
        self.assertEqual(res.status_code, 200)
        att = res.json()["attachment"]
        att_id = att["attachment_id"]
        self.assertEqual(att["document_type"], "NAMEPLATE")
        self.assertTrue(att["sha256_hash"])

        # 2. Query attachments
        res = self.client.get("/api/sessions/SESS-2026-001/attachments")
        self.assertEqual(res.status_code, 200)
        atts = res.json()["attachments"]
        self.assertTrue(any(a["attachment_id"] == att_id for a in atts))

        # 3. Download file
        res = self.client.get(f"/api/attachments/{att_id}/file")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content, fake_bytes)

        # 4. Delete attachment
        res = self.client.delete(f"/api/attachments/{att_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "deleted")


if __name__ == "__main__":
    unittest.main()

