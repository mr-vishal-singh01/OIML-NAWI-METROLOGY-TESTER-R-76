"""
Exhaustive Verification Suite for OIML R 76-1:2006 Metrological Engine
SIH26035: Non-Automatic Weighing Instruments Automated Test System
Dual-compatible with unittest and pytest
"""

import unittest
from decimal import Decimal
import sys
from pathlib import Path

# Add src to python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.nawi_engine import (
    AccuracyClass,
    VerificationType,
    PartialRange,
    InstrumentSpecification,
    MetrologyMath,
    Form1WeighingPerformance,
    Form3Eccentricity,
    Form5Repeatability,
    OIMLR111WeightValidator
)
from core.welmec_sealer import WelmecSoftwareSealer


class TestNawiEngine(unittest.TestCase):

    def test_turning_point_calculation(self):
        """Verify unrounded indication P = I + 0.5e - Delta_L."""
        I = Decimal("100.0")
        delta_l = Decimal("0.3")
        e = Decimal("1.0")

        p = MetrologyMath.calculate_turning_point(I, delta_l, e)
        # P = 100.0 + 0.5 - 0.3 = 100.2
        self.assertEqual(p, Decimal("100.2"))

        applied_load = Decimal("100.0")
        e_raw = MetrologyMath.calculate_raw_error(p, applied_load)
        self.assertEqual(e_raw, Decimal("0.2"))

        zero_error = Decimal("0.1")
        ec = MetrologyMath.calculate_corrected_error(e_raw, zero_error)
        self.assertEqual(ec, Decimal("0.1"))

    def test_class_iii_single_interval_mpe(self):
        """
        Test Class III MPE limits:
        0 <= m <= 500e       -> MPE = +/- 0.5e
        500e < m <= 2000e    -> MPE = +/- 1.0e
        2000e < m <= 10000e  -> MPE = +/- 1.5e
        """
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("15000"),  # 15 kg
            min_capacity=Decimal("100"),     # 100 g (20e)
            e=Decimal("5"),                 # 5 g
            d=Decimal("5"),
            unit="g"
        )

        # 1. Load = 500 * 5g = 2500g -> boundary of 0.5e
        mpe_low = MetrologyMath.get_mpe(Decimal("2500"), spec)
        self.assertEqual(mpe_low, Decimal("2.5"))  # 0.5 * 5g = 2.5g

        # 2. Load = 501 * 5g = 2505g -> drops into 1.0e bracket
        mpe_mid = MetrologyMath.get_mpe(Decimal("2505"), spec)
        self.assertEqual(mpe_mid, Decimal("5.0"))  # 1.0 * 5g = 5.0g

        # 3. Load = 2001 * 5g = 10005g -> drops into 1.5e bracket
        mpe_high = MetrologyMath.get_mpe(Decimal("10005"), spec)
        self.assertEqual(mpe_high, Decimal("7.5"))  # 1.5 * 5g = 7.5g

    def test_multi_interval_dynamic_mpe(self):
        """
        Verify dynamic MPE calculation on a dual-interval Class III retail scale:
        Range 1: 0 - 3000g, e1 = 1g
        Range 2: 3000 - 6000g, e2 = 2g
        """
        pr1 = PartialRange(max_capacity=Decimal("3000"), e=Decimal("1"), d=Decimal("1"))
        pr2 = PartialRange(max_capacity=Decimal("6000"), e=Decimal("2"), d=Decimal("2"))

        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("6000"),
            min_capacity=Decimal("20"),
            e=Decimal("1"),
            partial_ranges=[pr1, pr2],
            unit="g"
        )

        self.assertTrue(spec.is_multi_interval)

        # At 200g (in Range 1, e1 = 1g, m = 200 <= 500e) -> MPE = 0.5 * 1g = 0.5g
        mpe_r1 = MetrologyMath.get_mpe(Decimal("200"), spec)
        self.assertEqual(mpe_r1, Decimal("0.5"))

        # At 4000g (in Range 2, e2 = 2g, m = 4000 / 2 = 2000 <= 2000e) -> MPE = 1.0 * 2g = 2.0g
        mpe_r2 = MetrologyMath.get_mpe(Decimal("4000"), spec)
        self.assertEqual(mpe_r2, Decimal("2.0"))

    def test_form1_weighing_performance_and_hysteresis(self):
        """Test full ascending/descending weighing sequence with hysteresis."""
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("3000"),
            min_capacity=Decimal("20"),
            e=Decimal("1"),
            d=Decimal("1"),
            unit="g"
        )

        test_engine = Form1WeighingPerformance(spec)
        # Zero load: I0 = 0.0, dL = 0.5 -> P0 = 0 + 0.5 - 0.5 = 0.0 -> E0 = 0.0
        test_engine.set_zero_error(indication=Decimal("0.0"), delta_l=Decimal("0.5"))
        self.assertEqual(test_engine.zero_error_e0, Decimal("0.0"))

        # Ascending steps
        obs_asc = test_engine.add_observation(
            step_index=1,
            direction="ascending",
            applied_load=Decimal("500"),
            indicated_value=Decimal("500"),
            added_load_delta_l=Decimal("0.5")
        )
        self.assertTrue(obs_asc.passed)
        self.assertEqual(obs_asc.corrected_error_ec, Decimal("0.0"))

        # Descending step at 500g: I = 500, dL = 0.4 -> P = 500.1, Ec = +0.1
        obs_desc = test_engine.add_observation(
            step_index=2,
            direction="descending",
            applied_load=Decimal("500"),
            indicated_value=Decimal("500"),
            added_load_delta_l=Decimal("0.4")
        )
        self.assertTrue(obs_desc.passed)
        self.assertEqual(obs_desc.corrected_error_ec, Decimal("0.1"))

        # Evaluate hysteresis at 500g: |0.1 - 0.0| = 0.1 <= MPE(500g)=0.5g -> PASS
        h_res = test_engine.evaluate_hysteresis()
        self.assertTrue(h_res["hysteresis_passed"])
        self.assertEqual(Decimal(h_res["max_hysteresis"]), Decimal("0.1"))
        self.assertTrue(test_engine.overall_passed)

    def test_form3_corner_eccentricity(self):
        """Verify Corner Eccentricity test with 5 positions at 1/3 Max."""
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("15000"),
            min_capacity=Decimal("100"),
            e=Decimal("5"),
            d=Decimal("5")
        )

        corner_test = Form3Eccentricity(spec, supports_count=4)
        # Test load = 15000 / 3 = 5000g
        self.assertEqual(corner_test.test_load, Decimal("5000"))

        positions = ["Center", "Front-Left", "Back-Left", "Back-Right", "Front-Right"]
        for pos in positions:
            res = corner_test.record_position(
                position_name=pos,
                indication=Decimal("5000"),
                delta_l=Decimal("2.5"),
                zero_error=Decimal("0")
            )
            self.assertTrue(res["passed"])

        self.assertTrue(corner_test.overall_passed)

    def test_repeatability_evaluation(self):
        """Verify Repeatability evaluation spread (I_max - I_min) <= MPE."""
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("10000"),
            min_capacity=Decimal("100"),
            e=Decimal("5"),
            d=Decimal("5")
        )

        rep_test = Form5Repeatability(spec)
        for reading in [10000, 10000, 10005, 10000, 10000, 10000, 10005, 10000, 10000, 10000]:
            rep_test.add_reading("100%", Decimal(str(reading)))

        res = rep_test.evaluate()
        self.assertTrue(res["overall_passed"])
        self.assertEqual(res["series"]["100%"]["spread"], "5")

    def test_oiml_r111_standard_weight_validator(self):
        """Verify standard weight expanded uncertainty rule U <= 1/3 MPE."""
        mpe = Decimal("1.5")
        valid, max_u, margin = OIMLR111WeightValidator.verify_weight_uncertainty(Decimal("0.2"), mpe)
        self.assertTrue(valid)
        self.assertEqual(max_u, Decimal("0.5"))
        self.assertEqual(margin, Decimal("0.3"))

        invalid, _, _ = OIMLR111WeightValidator.verify_weight_uncertainty(Decimal("0.8"), mpe)
        self.assertFalse(invalid)

    def test_welmec_software_sealer(self):
        """Verify WELMEC 7.2 cryptographic sealing of LRS kernel."""
        fp = WelmecSoftwareSealer.calculate_lrs_fingerprint()
        self.assertEqual(fp["lrs_module"], "nawi_engine.py")
        self.assertEqual(len(fp["sha256"]), 64)
        self.assertEqual(len(fp["crc32"]), 8)
        self.assertEqual(fp["status"], "SEALED_VALID")


    def test_form15_software_examination(self):
        """Verify OIML R 76-2 Form 15 Software-Controlled Instruments Examination."""
        from core.software_examination import (
            Form15SoftwareExamination,
            SoftwareArchitectureType,
            WelmecRiskClass
        )
        exam = Form15SoftwareExamination(
            architecture_type=SoftwareArchitectureType.TYPE_P,
            risk_class=WelmecRiskClass.CLASS_C
        )
        # All pass
        exam.add_standard_checks(
            software_id_verified=True,
            checksum_verified=True,
            checksum_value="SHA256:4FA...CRC32:9912",
            software_separation_verified=True,
            parameter_protection_verified=True,
            audit_trail_counter_working=True,
            event_counter_value=5,
            power_failure_protection_verified=True
        )
        self.assertTrue(exam.overall_passed)
        self.assertEqual(len(exam.checks), 6)

        # One fails -> overall fails
        exam.checks[2].passed = False  # software separation failed
        self.assertFalse(exam.overall_passed)

    def test_explainable_derivation_metadata_structure(self):
        """Verify that observations generate fully structured, explainable OIML derivation metadata."""
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("15000"),
            min_capacity=Decimal("100"),
            e=Decimal("5"),
            d=Decimal("5"),
            unit="g"
        )
        engine = Form1WeighingPerformance(spec)
        engine.set_zero_error(indication=Decimal("0.0"), delta_l=Decimal("2.5"))

        # Add observation at 2500g (500e -> bracket boundary)
        obs = engine.add_observation(
            step_index=1,
            direction="ascending",
            applied_load=Decimal("2500"),
            indicated_value=Decimal("2500"),
            added_load_delta_l=Decimal("2.5")
        )
        self.assertTrue(obs.passed)
        self.assertIn("turning_point", obs.derivation)
        self.assertIn("error_calculation", obs.derivation)
        self.assertIn("mpe_evaluation", obs.derivation)

        tp = obs.derivation["turning_point"]
        self.assertEqual(tp["standard"], "OIML R 76-1:2006 (E)")
        self.assertEqual(tp["clause"], "A.4.4.3")
        self.assertEqual(tp["unrounded_indication_p"], "2500.0")

        err = obs.derivation["error_calculation"]
        self.assertEqual(err["corrected_error_ec"], "0.0")

        mpe = obs.derivation["mpe_evaluation"]
        self.assertEqual(mpe["clause"], "3.5.1 & Table 6")
        self.assertEqual(mpe["bracket"], "0 <= m <= 500e")
        self.assertEqual(mpe["mpe_factor"], "+/- 0.5e")
        self.assertEqual(mpe["mpe_limit_value"], "2.500000")
        self.assertEqual(mpe["assessment"], "PASS")

    def test_failing_observation_and_deviation(self):
        """Verify that an out-of-tolerance reading fails and records non-zero deviation."""
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("15000"),
            min_capacity=Decimal("100"),
            e=Decimal("5"),
            d=Decimal("5")
        )
        engine = Form1WeighingPerformance(spec)
        engine.set_zero_error(indication=Decimal("0.0"), delta_l=Decimal("2.5"))

        # Indication 2510 with delta_l=2.5 -> P = 2510.0 -> Ec = +10.0 -> MPE = 2.5 -> FAIL
        obs = engine.add_observation(
            step_index=1,
            direction="ascending",
            applied_load=Decimal("2500"),
            indicated_value=Decimal("2510"),
            added_load_delta_l=Decimal("2.5")
        )
        self.assertFalse(obs.passed)
        self.assertFalse(engine.overall_passed)
        self.assertEqual(obs.corrected_error_ec, Decimal("10.0"))
        # Deviation = |10.0| - 2.5 = 7.5
        self.assertEqual(obs.deviation, Decimal("7.500000"))
        self.assertEqual(obs.derivation["mpe_evaluation"]["assessment"], "FAIL")

    def test_eccentricity_and_repeatability_derivations(self):
        """Verify Form 3 Eccentricity and Form 5 Repeatability explainability metadata."""
        spec = InstrumentSpecification(
            accuracy_class=AccuracyClass.CLASS_III,
            max_capacity=Decimal("15000"),
            min_capacity=Decimal("100"),
            e=Decimal("5"),
            d=Decimal("5")
        )
        # Form 3
        ecc = Form3Eccentricity(spec)
        pos = ecc.record_position("Center", Decimal("5000"), Decimal("2.5"))
        self.assertIn("derivation", pos)
        self.assertEqual(pos["derivation"]["clause"], "3.6.2 & Clause A.4.7")
        self.assertEqual(pos["derivation"]["assessment"], "PASS")

        # Form 5
        rep = Form5Repeatability(spec)
        for val in [5000, 5000, 5005, 5000, 5000, 5000, 5000, 5000, 5005, 5000]:
            rep.add_reading("50%", Decimal(str(val)))
        rep_res = rep.evaluate()
        self.assertIn("derivation", rep_res["series"]["50%"])
        self.assertEqual(rep_res["series"]["50%"]["derivation"]["clause"], "3.6.1 & Clause A.4.10")
        self.assertEqual(rep_res["series"]["50%"]["derivation"]["assessment"], "PASS")


if __name__ == "__main__":
    unittest.main()
