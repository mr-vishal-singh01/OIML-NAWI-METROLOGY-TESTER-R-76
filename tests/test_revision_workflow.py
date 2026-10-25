"""
Exhaustive Verification Suite for NAWI Testing Workflow & Revision Lifecycle
Directly testing:
1. Non-zero E0 compensation (Clause A.4.4.3).
2. Acceptance boundary conditions (+/- MPE vs +/- MPE +/- 0.1g).
3. Both distinct failure scenarios (Delta_L = 1.5g -> Ec = +11.0g vs Delta_L = 2.5g -> Ec = +10.0g).
4. Atomic amendment sequence and optimistic locking.
5. Preserved immutable snapshot ownership.
"""

import unittest
from decimal import Decimal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.nawi_engine import (
    AccuracyClass,
    InstrumentSpecification
)
from api.workflow import (
    TestSessionWorkflow,
    ReportReviewStatus,
    InstrumentAssessment
)


class TestRevisionWorkflowLifecycle(unittest.TestCase):

    def setUp(self):
        # Single-Interval Class III Initial Verification (Max=15000g, Min=100g, e=5g, d=5g)
        self.spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("15000"),
            min_capacity=Decimal("100"),
            e=Decimal("5"),
            d=Decimal("5"),
            unit="g",
            manufacturer="Essae-Teraoka",
            model="DS-852",
            serial_number="SN-2026-IND-001"
        )
        self.workflow = TestSessionWorkflow(session_id="SESS-2026-001", spec=self.spec)

    def test_nonzero_zero_error_compensation(self):
        """
        Verify that non-zero error at zero load (E0 != 0) is correctly compensated per Clause A.4.4.3:
        At zero: I0 = 0.0, dL0 = 2.0 -> P0 = 0 + 2.5 - 2.0 = +0.5g -> E0 = +0.5g.
        At load 100g: I = 100.0, dL = 2.5 -> P = 100.0 -> Raw E = 0.0 -> Ec = E - E0 = 0.0 - (+0.5) = -0.5g.
        """
        self.workflow.set_zero_reading(indication=Decimal("0.0"), delta_l=Decimal("2.0"))
        self.assertEqual(self.workflow.zero_error_e0, Decimal("0.5"))

        c = self.workflow.record_observation(1, Decimal("100"), Decimal("100.0"), Decimal("2.5"))
        self.assertEqual(c.raw_error_e, Decimal("0.0"))
        self.assertEqual(c.corrected_error_ec, Decimal("-0.5"))
        self.assertEqual(c.mpe, Decimal("2.500000"))
        self.assertTrue(c.passed)

    def test_acceptance_boundary_conditions(self):
        """
        Verify exact acceptance boundaries for 0 <= m <= 500e (MPE = +/- 2.5g):
        1. Ec = +2.50g -> PASS
        2. Ec = +2.60g -> FAIL
        3. Ec = -2.50g -> PASS
        4. Ec = -2.60g -> FAIL
        """
        self.workflow.set_zero_reading(indication=Decimal("0.0"), delta_l=Decimal("2.5"))  # E0 = 0.0

        # Boundary Case 1: Ec = +2.5g (L = 2500g, I = 2502.0g, dL = 2.0g -> P = 2502.5 -> Ec = +2.5g)
        b1 = self.workflow.record_observation(1, Decimal("2500"), Decimal("2502.0"), Decimal("2.0"))
        self.assertEqual(b1.corrected_error_ec, Decimal("2.5"))
        self.assertTrue(b1.passed)

        # Boundary Case 2: Ec = +2.6g (L = 2500g, I = 2502.0g, dL = 1.9g -> P = 2502.6 -> Ec = +2.6g)
        b2 = self.workflow.record_observation(2, Decimal("2500"), Decimal("2502.0"), Decimal("1.9"))
        self.assertEqual(b2.corrected_error_ec, Decimal("2.6"))
        self.assertFalse(b2.passed)
        self.assertEqual(b2.deviation, Decimal("0.100000"))

        # Boundary Case 3: Ec = -2.5g (L = 2500g, I = 2497.0g, dL = 2.0g -> P = 2497.5 -> Ec = -2.5g)
        b3 = self.workflow.record_observation(3, Decimal("2500"), Decimal("2497.0"), Decimal("2.0"))
        self.assertEqual(b3.corrected_error_ec, Decimal("-2.5"))
        self.assertTrue(b3.passed)

        # Boundary Case 4: Ec = -2.6g (L = 2500g, I = 2497.0g, dL = 2.1g -> P = 2497.4 -> Ec = -2.6g)
        b4 = self.workflow.record_observation(4, Decimal("2500"), Decimal("2497.0"), Decimal("2.1"))
        self.assertEqual(b4.corrected_error_ec, Decimal("-2.6"))
        self.assertFalse(b4.passed)
        self.assertEqual(b4.deviation, Decimal("0.100000"))

    def test_both_distinct_failure_vectors(self):
        """
        Verifies both distinct failure vectors without numerical conflation:
        Scenario 1: L = 2500, I = 2510, dL = 1.5 -> P = 2511.0 -> Ec = +11.0g > 2.5g -> FAIL
        Scenario 2: L = 2500, I = 2510, dL = 2.5 -> P = 2510.0 -> Ec = +10.0g > 2.5g -> FAIL
        """
        self.workflow.set_zero_reading(indication=Decimal("0.0"), delta_l=Decimal("2.5"))  # E0 = 0

        s1 = self.workflow.record_observation(1, Decimal("2500"), Decimal("2510.0"), Decimal("1.5"))
        self.assertEqual(s1.p, Decimal("2511.0"))
        self.assertEqual(s1.corrected_error_ec, Decimal("11.0"))
        self.assertFalse(s1.passed)

        s2 = self.workflow.record_observation(2, Decimal("2500"), Decimal("2510.0"), Decimal("2.5"))
        self.assertEqual(s2.p, Decimal("2510.0"))
        self.assertEqual(s2.corrected_error_ec, Decimal("10.0"))
        self.assertFalse(s2.passed)

    def test_atomic_amendment_recalculation_and_optimistic_locking(self):
        """
        Proves:
        1. Revision 1 approved with expected_revision=1.
        2. Amendment atomically marks prior calc stale, updates revision to 2,
           recalculates result with failure verdict, and flags session as REQUIRES_RE_REVIEW.
        3. Attempting to approve using stale revision #1 is rejected by optimistic locking.
        4. Revision 2 approved with expected_revision=2.
        5. Historical archive retains immutable Revision 1 (PASSED) alongside Revision 2 (FAILED).
        """
        self.workflow.set_zero_reading(indication=Decimal("0.0"), delta_l=Decimal("2.5"))
        self.workflow.record_observation(1, Decimal("100"), Decimal("100.0"), Decimal("2.5"))
        self.workflow.record_observation(2, Decimal("2500"), Decimal("2500.0"), Decimal("1.5"))  # Ec = +1.0g (PASS)

        # Approve Revision 1
        snap1 = self.workflow.approve_report_revision(reviewer_id="DR_SHARMA", expected_revision=1, comments="Initial review")
        self.assertEqual(self.workflow.review_status, ReportReviewStatus.APPROVED)
        self.assertEqual(snap1.instrument_verdict, InstrumentAssessment.PASSED)

        # Amend Step 2: Change I from 2500 to 2510 (keeping dL = 1.5g)
        # Expected new error: Ec = +11.0g (FAIL)
        calc2 = self.workflow.amend_observation(
            step_index=2,
            new_indication=Decimal("2510.0"),
            new_delta_l=Decimal("1.5"),
            operator_id="TECH_VERMA",
            edit_reason="Corrected transcription error from field sheet"
        )

        # Check atomic state
        self.assertEqual(self.workflow.current_revision, 2)
        self.assertEqual(self.workflow.review_status, ReportReviewStatus.REQUIRES_RE_REVIEW)
        self.assertFalse(calc2.passed)
        self.assertEqual(calc2.corrected_error_ec, Decimal("11.0"))
        self.assertEqual(self.workflow.instrument_verdict, InstrumentAssessment.FAILED)

        # Optimistic locking check: Reviewer tries to approve using stale revision 1
        with self.assertRaises(RuntimeError) as ctx:
            self.workflow.approve_report_revision(reviewer_id="DR_SHARMA", expected_revision=1)
        self.assertIn("Concurrency Conflict", str(ctx.exception))

        # Legitimate approval of Revision 2
        snap2 = self.workflow.approve_report_revision(reviewer_id="DR_SHARMA", expected_revision=2, comments="Reviewed amendment: failed.")
        self.assertEqual(snap2.revision_number, 2)
        self.assertEqual(snap2.instrument_verdict, InstrumentAssessment.FAILED)

        # Archive verification
        self.assertEqual(len(self.workflow.archived_report_revisions), 2)
        self.assertEqual(self.workflow.archived_report_revisions[0].instrument_verdict, InstrumentAssessment.PASSED)
        self.assertEqual(self.workflow.archived_report_revisions[1].instrument_verdict, InstrumentAssessment.FAILED)


if __name__ == "__main__":
    unittest.main()
