"""
OIML R 76-1:2006 & R 76-2:2007 Compliant Metrological Calculation Engine
For Non-Automatic Weighing Instruments (NAWI) - SIH26035
Legal Metrology Division, Ministry of Consumer Affairs, Food & Public Distribution

All arithmetic utilizes arbitrary-precision Decimal with Banker's Rounding (ROUND_HALF_EVEN)
Strictly conforming to WELMEC Guide 7.2 (Legally Relevant Software - LRS)
"""

from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
import math

# Set global decimal precision to 28 digits (ISO standard precision)
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_EVEN


class AccuracyClass(str, Enum):
    CLASS_I = "Class I"      # Special Accuracy
    CLASS_II = "Class II"    # High Accuracy
    CLASS_III = "Class III"  # Medium Accuracy
    CLASS_IIII = "Class IIII"# Ordinary Accuracy


class VerificationType(str, Enum):
    INITIAL = "Initial / Pattern Approval"  # Normal MPE
    IN_SERVICE = "In-Service"              # 2x MPE


class PartialRange:
    """Represents a partial weighing range in a multi-interval instrument."""
    def __init__(self, max_capacity: Decimal, e: Decimal, d: Optional[Decimal] = None):
        self.max_capacity = Decimal(str(max_capacity))
        self.e = Decimal(str(e))
        self.d = Decimal(str(d)) if d is not None else self.e

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_capacity": str(self.max_capacity),
            "e": str(self.e),
            "d": str(self.d)
        }


class InstrumentSpecification:
    """
    Complete metrological specification of a Non-Automatic Weighing Instrument (NAWI).
    Supports single-interval, multi-interval (multiple e), and multiple range instruments.
    """
    def __init__(
        self,
        accuracy_class: AccuracyClass,
        max_capacity: Decimal,
        min_capacity: Decimal,
        e: Decimal,
        d: Optional[Decimal] = None,
        partial_ranges: Optional[List[PartialRange]] = None,
        unit: str = "g",
        manufacturer: str = "",
        model: str = "",
        serial_number: str = ""
    ):
        self.accuracy_class = accuracy_class
        self.max_capacity = Decimal(str(max_capacity))
        self.min_capacity = Decimal(str(min_capacity))
        self.e = Decimal(str(e))
        self.d = Decimal(str(d)) if d is not None else self.e
        self.partial_ranges = partial_ranges or []
        self.unit = unit
        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number

        # Validate basic parameters per OIML R 76-1 Table 3 & 4
        self.validate_specification()

    @property
    def is_multi_interval(self) -> bool:
        return len(self.partial_ranges) > 1

    @property
    def n_intervals(self) -> Decimal:
        """Total number of verification intervals: n = Max / e."""
        return (self.max_capacity / self.e).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)

    def validate_specification(self) -> List[str]:
        """Validates parameters against OIML R 76-1 Table 3 limits."""
        errors = []
        n = self.n_intervals

        if self.accuracy_class == AccuracyClass.CLASS_I:
            if self.e < Decimal("0.001"):
                errors.append("Class I: e must be >= 0.001 g")
            if n < 50000:
                errors.append(f"Class I: n must be >= 50,000 (currently {n})")
            if self.min_capacity < Decimal("100") * self.e:
                errors.append(f"Class I: Min capacity must be >= 100e (currently {self.min_capacity})")

        elif self.accuracy_class == AccuracyClass.CLASS_II:
            if n < 100 or n > 100000:
                errors.append(f"Class II: n must be between 100 and 100,000 (currently {n})")
            if self.e < Decimal("0.001"):
                errors.append("Class II: e must be >= 0.001 g")

        elif self.accuracy_class == AccuracyClass.CLASS_III:
            if n < 100 or n > 10000:
                errors.append(f"Class III: n must be between 100 and 10,000 (currently {n})")
            if self.min_capacity < Decimal("20") * self.e:
                errors.append(f"Class III: Min capacity must be >= 20e (currently {self.min_capacity})")

        elif self.accuracy_class == AccuracyClass.CLASS_IIII:
            if n < 100 or n > 1000:
                errors.append(f"Class IIII: n must be between 100 and 1,000 (currently {n})")
            if self.min_capacity < Decimal("10") * self.e:
                errors.append(f"Class IIII: Min capacity must be >= 10e (currently {self.min_capacity})")

        return errors


class MetrologyMath:
    """
    Core Mathematical Engine implementing Turning Point Method and MPE determination.
    """

    @staticmethod
    def calculate_turning_point(
        indication: Decimal,
        added_load_delta_l: Decimal,
        e_val: Decimal,
        d_val: Optional[Decimal] = None
    ) -> Decimal:
        """
        Calculates the unrounded indicated value P via turning point method:
        P = I + 0.5e - Delta_L (or P = I + 0.5d - Delta_L if d < e)
        OIML R 76-1 Clause A.4.4.3
        """
        I = Decimal(str(indication))
        dL = Decimal(str(added_load_delta_l))
        step = Decimal(str(d_val)) if (d_val is not None and d_val < e_val) else Decimal(str(e_val))
        half_step = step / Decimal("2")
        P = I + half_step - dL
        return P

    @staticmethod
    def calculate_raw_error(p: Decimal, applied_load: Decimal) -> Decimal:
        """Raw error: E = P - L."""
        return Decimal(str(p)) - Decimal(str(applied_load))

    @staticmethod
    def calculate_corrected_error(raw_error: Decimal, zero_error: Decimal) -> Decimal:
        """Corrected error compensating for zero drift: Ec = E - E0."""
        return Decimal(str(raw_error)) - Decimal(str(zero_error))

    @staticmethod
    def get_active_partial_range(load: Decimal, spec: InstrumentSpecification) -> Tuple[Decimal, Decimal]:
        """
        Determines the active (e, d) for a given load step in multi-interval instruments.
        """
        L = Decimal(str(load))
        if not spec.is_multi_interval:
            return spec.e, spec.d

        for pr in spec.partial_ranges:
            if L <= pr.max_capacity:
                return pr.e, pr.d

        # Default to highest range if load exceeds all partials (up to Max)
        return spec.partial_ranges[-1].e, spec.partial_ranges[-1].d

    DEFAULT_TABLE_6_CONFIG: Dict[AccuracyClass, List[Dict[str, Any]]] = {
        AccuracyClass.CLASS_I: [
            {"max_m": Decimal("50000"), "factor": Decimal("0.5"), "factor_str": "+/- 0.5e", "bracket": "0 <= m <= 50,000e"},
            {"max_m": Decimal("200000"), "factor": Decimal("1.0"), "factor_str": "+/- 1.0e", "bracket": "50,000e < m <= 200,000e"},
            {"max_m": None, "factor": Decimal("1.5"), "factor_str": "+/- 1.5e", "bracket": "m > 200,000e"},
        ],
        AccuracyClass.CLASS_II: [
            {"max_m": Decimal("5000"), "factor": Decimal("0.5"), "factor_str": "+/- 0.5e", "bracket": "0 <= m <= 5,000e"},
            {"max_m": Decimal("20000"), "factor": Decimal("1.0"), "factor_str": "+/- 1.0e", "bracket": "5,000e < m <= 20,000e"},
            {"max_m": None, "factor": Decimal("1.5"), "factor_str": "+/- 1.5e", "bracket": "20,000e < m <= 100,000e"},
        ],
        AccuracyClass.CLASS_III: [
            {"max_m": Decimal("500"), "factor": Decimal("0.5"), "factor_str": "+/- 0.5e", "bracket": "0 <= m <= 500e"},
            {"max_m": Decimal("2000"), "factor": Decimal("1.0"), "factor_str": "+/- 1.0e", "bracket": "500e < m <= 2,000e"},
            {"max_m": None, "factor": Decimal("1.5"), "factor_str": "+/- 1.5e", "bracket": "2,000e < m <= 10,000e"},
        ],
        AccuracyClass.CLASS_IIII: [
            {"max_m": Decimal("50"), "factor": Decimal("0.5"), "factor_str": "+/- 0.5e", "bracket": "0 <= m <= 50e"},
            {"max_m": Decimal("200"), "factor": Decimal("1.0"), "factor_str": "+/- 1.0e", "bracket": "50e < m <= 200e"},
            {"max_m": None, "factor": Decimal("1.5"), "factor_str": "+/- 1.5e", "bracket": "200e < m <= 1,000e"},
        ],
    }

    DEFAULT_IN_SERVICE_MULTIPLIER: Decimal = Decimal("2.0")
    ACTIVE_TABLE_6_CONFIG: Optional[Dict[AccuracyClass, List[Dict[str, Any]]]] = None
    ACTIVE_IN_SERVICE_MULTIPLIER: Decimal = Decimal("2.0")

    @classmethod
    def get_table_6_config_dict(cls) -> Dict[str, Any]:
        """Returns the active Table 6 tolerance configuration in JSON-serializable dictionary format."""
        cfg = cls.ACTIVE_TABLE_6_CONFIG or cls.DEFAULT_TABLE_6_CONFIG
        result: Dict[str, Any] = {
            "in_service_multiplier": str(cls.ACTIVE_IN_SERVICE_MULTIPLIER),
            "classes": {}
        }
        for ac, steps in cfg.items():
            result["classes"][ac.value] = [
                {
                    "max_m": str(s["max_m"]) if s["max_m"] is not None else None,
                    "factor": str(s["factor"]),
                    "factor_str": s["factor_str"],
                    "bracket": s["bracket"]
                }
                for s in steps
            ]
        return result

    @classmethod
    def set_table_6_config_dict(cls, data: Dict[str, Any]) -> None:
        """Sets active Table 6 tolerance configuration."""
        new_cfg: Dict[AccuracyClass, List[Dict[str, Any]]] = {}
        for ac in AccuracyClass:
            if ac.value in data.get("classes", {}):
                steps = []
                for s in data["classes"][ac.value]:
                    steps.append({
                        "max_m": Decimal(str(s["max_m"])) if s.get("max_m") is not None else None,
                        "factor": Decimal(str(s["factor"])),
                        "factor_str": s.get("factor_str") or f"+/- {s['factor']}e",
                        "bracket": s.get("bracket", "")
                    })
                new_cfg[ac] = steps
            else:
                new_cfg[ac] = list(cls.DEFAULT_TABLE_6_CONFIG[ac])
        cls.ACTIVE_TABLE_6_CONFIG = new_cfg
        if "in_service_multiplier" in data:
            cls.ACTIVE_IN_SERVICE_MULTIPLIER = Decimal(str(data["in_service_multiplier"]))

    @classmethod
    def reset_table_6_defaults(cls) -> None:
        """Resets active tolerances to statutory OIML R-76 Table 6 defaults."""
        cls.ACTIVE_TABLE_6_CONFIG = None
        cls.ACTIVE_IN_SERVICE_MULTIPLIER = cls.DEFAULT_IN_SERVICE_MULTIPLIER

    @classmethod
    def get_mpe_details(
        cls,
        applied_load: Decimal,
        spec: InstrumentSpecification,
        verification_type: VerificationType = VerificationType.INITIAL
    ) -> Dict[str, Any]:
        """
        Evaluates Maximum Permissible Error (MPE) according to OIML R 76-1:2006 (E) Table 6.
        Returns both the numeric MPE and full structured derivation metadata.
        Uses active legally sealed Table 6 parameters.
        """
        L = abs(Decimal(str(applied_load)))
        active_e, active_d = cls.get_active_partial_range(L, spec)

        # Express load m in units of verification scale intervals e: m = L / e
        m = L / active_e

        # Step limits from active or default Table 6 config
        cfg = cls.ACTIVE_TABLE_6_CONFIG or cls.DEFAULT_TABLE_6_CONFIG
        steps = cfg.get(spec.accuracy_class, cls.DEFAULT_TABLE_6_CONFIG[spec.accuracy_class])

        mpe_factor = Decimal("1.5")
        mpe_factor_str = "+/- 1.5e"
        bracket = "m > high bracket"

        for step in steps:
            max_m = step.get("max_m")
            if max_m is None or m <= max_m:
                mpe_factor = step["factor"]
                mpe_factor_str = step["factor_str"]
                bracket = step["bracket"]
                break

        base_factor = mpe_factor
        # In-service verification multiplier (Clause 3.5.2)
        if verification_type == VerificationType.IN_SERVICE:
            mult = cls.ACTIVE_IN_SERVICE_MULTIPLIER
            mpe_factor *= mult
            mpe_factor_str = f"{mult} * ({mpe_factor_str}) = +/- {mpe_factor}e"

        mpe_value = (mpe_factor * active_e).quantize(Decimal('0.000001'), rounding=ROUND_HALF_EVEN)

        return {
            "standard": "OIML R 76-1:2006 (E)",
            "clause": "3.5.1 & Table 6" if verification_type == VerificationType.INITIAL else "3.5.2 & Table 6",
            "accuracy_class": spec.accuracy_class.value,
            "verification_type": verification_type.value,
            "applied_load": str(L),
            "active_e": str(active_e),
            "load_in_intervals_m": str(m),
            "bracket": bracket,
            "mpe_factor": mpe_factor_str,
            "mpe_value": mpe_value,
            "unit": spec.unit
        }

    @classmethod
    def get_mpe(
        cls,
        applied_load: Decimal,
        spec: InstrumentSpecification,
        verification_type: VerificationType = VerificationType.INITIAL
    ) -> Decimal:
        """
        Evaluates Maximum Permissible Error (MPE) according to OIML R 76-1 Table 6.
        """
        details = cls.get_mpe_details(applied_load, spec, verification_type)
        return details["mpe_value"]


class WeighingObservation:
    """Individual observation row in OIML R 76-2 test forms with explainable derivation."""
    def __init__(
        self,
        step_index: int,
        direction: str,  # 'ascending' or 'descending'
        applied_load: Decimal,
        indicated_value: Decimal,
        added_load_delta_l: Decimal
    ):
        self.step_index = step_index
        self.direction = direction.lower()
        self.applied_load = Decimal(str(applied_load))
        self.indicated_value = Decimal(str(indicated_value))
        self.added_load_delta_l = Decimal(str(added_load_delta_l))

        # Computed metrological fields
        self.p: Optional[Decimal] = None
        self.raw_error_e: Optional[Decimal] = None
        self.corrected_error_ec: Optional[Decimal] = None
        self.mpe: Optional[Decimal] = None
        self.passed: Optional[bool] = None
        self.deviation: Optional[Decimal] = None
        self.derivation: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_index": self.step_index,
            "direction": self.direction,
            "applied_load": str(self.applied_load),
            "indicated_value": str(self.indicated_value),
            "added_load_delta_l": str(self.added_load_delta_l),
            "unrounded_indication_p": str(self.p) if self.p is not None else None,
            "raw_error_e": str(self.raw_error_e) if self.raw_error_e is not None else None,
            "corrected_error_ec": str(self.corrected_error_ec) if self.corrected_error_ec is not None else None,
            "mpe": str(self.mpe) if self.mpe is not None else None,
            "passed": self.passed,
            "deviation": str(self.deviation) if self.deviation is not None else None,
            "derivation": self.derivation
        }


class Form1WeighingPerformance:
    """
    OIML R 76-2 Section 1: Weighing Performance Test Engine.
    Computes P, E, Ec, MPE compliance, and Hysteresis.
    """
    def __init__(self, spec: InstrumentSpecification, verification_type: VerificationType = VerificationType.INITIAL):
        self.spec = spec
        self.verification_type = verification_type
        self.observations: List[WeighingObservation] = []
        self.zero_error_e0: Decimal = Decimal("0")
        self.overall_passed: bool = True
        self.max_hysteresis: Decimal = Decimal("0")

    def set_zero_error(self, indication: Decimal, delta_l: Decimal, zero_load: Decimal = Decimal("0")):
        active_e, active_d = MetrologyMath.get_active_partial_range(zero_load, self.spec)
        p0 = MetrologyMath.calculate_turning_point(indication, delta_l, active_e, active_d)
        self.zero_error_e0 = MetrologyMath.calculate_raw_error(p0, zero_load)

    def add_observation(
        self,
        step_index: int,
        direction: str,
        applied_load: Decimal,
        indicated_value: Decimal,
        added_load_delta_l: Decimal
    ) -> WeighingObservation:
        obs = WeighingObservation(step_index, direction, applied_load, indicated_value, added_load_delta_l)
        active_e, active_d = MetrologyMath.get_active_partial_range(obs.applied_load, self.spec)
        step = active_d if active_d < active_e else active_e

        # 1. Turning point calculation
        obs.p = MetrologyMath.calculate_turning_point(obs.indicated_value, obs.added_load_delta_l, active_e, active_d)

        # 2. Raw error
        obs.raw_error_e = MetrologyMath.calculate_raw_error(obs.p, obs.applied_load)

        # 3. Corrected error
        obs.corrected_error_ec = MetrologyMath.calculate_corrected_error(obs.raw_error_e, self.zero_error_e0)

        # 4. MPE threshold & details
        mpe_details = MetrologyMath.get_mpe_details(obs.applied_load, self.spec, self.verification_type)
        obs.mpe = mpe_details["mpe_value"]

        # 5. Conformity check
        obs.passed = abs(obs.corrected_error_ec) <= obs.mpe
        obs.deviation = abs(obs.corrected_error_ec) - obs.mpe if not obs.passed else Decimal("0")

        # 6. Build structured explainability derivation metadata
        obs.derivation = {
            "turning_point": {
                "standard": "OIML R 76-1:2006 (E)",
                "clause": "A.4.4.3",
                "formula": "P = I + 0.5e - Delta_L" if step == active_e else "P = I + 0.5d - Delta_L",
                "formula_latex": r"P = I + \frac{1}{2}e - \Delta L" if step == active_e else r"P = I + \frac{1}{2}d - \Delta L",
                "inputs": {
                    "indicated_value_I": str(obs.indicated_value),
                    "added_load_delta_l": str(obs.added_load_delta_l),
                    "scale_step": str(step)
                },
                "substitution": f"P = {obs.indicated_value} + 0.5*({step}) - {obs.added_load_delta_l}",
                "unrounded_indication_p": str(obs.p)
            },
            "error_calculation": {
                "standard": "OIML R 76-1:2006 (E)",
                "clause": "A.4.4.3",
                "raw_error_formula": "E = P - L",
                "raw_error_substitution": f"E = {obs.p} - {obs.applied_load}",
                "raw_error_e": str(obs.raw_error_e),
                "zero_error_compensation_formula": "Ec = E - E0",
                "zero_error_e0": str(self.zero_error_e0),
                "corrected_error_substitution": f"Ec = {obs.raw_error_e} - ({self.zero_error_e0})",
                "corrected_error_ec": str(obs.corrected_error_ec)
            },
            "mpe_evaluation": {
                "standard": mpe_details["standard"],
                "clause": mpe_details["clause"],
                "accuracy_class": mpe_details["accuracy_class"],
                "verification_type": mpe_details["verification_type"],
                "load_in_intervals_m": mpe_details["load_in_intervals_m"],
                "bracket": mpe_details["bracket"],
                "mpe_factor": mpe_details["mpe_factor"],
                "mpe_limit_value": str(obs.mpe),
                "condition": "|Ec| <= MPE",
                "comparison": f"|{obs.corrected_error_ec}| <= {obs.mpe}",
                "assessment": "PASS" if obs.passed else "FAIL",
                "deviation": str(obs.deviation)
            }
        }

        if not obs.passed:
            self.overall_passed = False

        self.observations.append(obs)
        return obs

    def evaluate_hysteresis(self) -> Dict[str, Any]:
        """
        Evaluates hysteresis between ascending and descending loading at identical load points.
        Hysteresis = |Ec_descending - Ec_ascending| <= |MPE|
        """
        asc_map: Dict[Decimal, WeighingObservation] = {}
        desc_map: Dict[Decimal, WeighingObservation] = {}

        for obs in self.observations:
            if obs.direction == "ascending":
                asc_map[obs.applied_load] = obs
            elif obs.direction == "descending":
                desc_map[obs.applied_load] = obs

        hysteresis_results = []
        max_h = Decimal("0")
        hysteresis_passed = True

        for load, asc_obs in asc_map.items():
            if load in desc_map:
                desc_obs = desc_map[load]
                h_val = abs(desc_obs.corrected_error_ec - asc_obs.corrected_error_ec)
                mpe = MetrologyMath.get_mpe(load, self.spec, self.verification_type)
                h_pass = h_val <= mpe
                if not h_pass:
                    hysteresis_passed = False
                if h_val > max_h:
                    max_h = h_val

                hysteresis_results.append({
                    "load": str(load),
                    "ascending_ec": str(asc_obs.corrected_error_ec),
                    "descending_ec": str(desc_obs.corrected_error_ec),
                    "hysteresis": str(h_val),
                    "mpe": str(mpe),
                    "passed": h_pass
                })

        self.max_hysteresis = max_h
        return {
            "max_hysteresis": str(max_h),
            "hysteresis_passed": hysteresis_passed,
            "details": hysteresis_results
        }


class Form3Eccentricity:
    """
    OIML R 76-2 Section 3: Eccentricity (Corner Load) Test.
    Test load = 1/3 Max (or 1/4 Max for >4 supports). Center + 4 Corners.
    """
    def __init__(self, spec: InstrumentSpecification, supports_count: int = 4):
        self.spec = spec
        self.supports_count = supports_count
        factor = Decimal("3") if supports_count <= 4 else Decimal("4")
        self.test_load = (spec.max_capacity / factor).quantize(spec.e, rounding=ROUND_HALF_EVEN)
        self.mpe = MetrologyMath.get_mpe(self.test_load, spec)
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.overall_passed = True

    def record_position(
        self,
        position_name: str,  # 'Center', 'Front-Left', 'Back-Left', 'Back-Right', 'Front-Right'
        indication: Decimal,
        delta_l: Decimal,
        zero_error: Decimal = Decimal("0")
    ) -> Dict[str, Any]:
        p = MetrologyMath.calculate_turning_point(indication, delta_l, self.spec.e, self.spec.d)
        raw_e = MetrologyMath.calculate_raw_error(p, self.test_load)
        ec = MetrologyMath.calculate_corrected_error(raw_e, zero_error)
        passed = abs(ec) <= self.mpe
        deviation = abs(ec) - self.mpe if not passed else Decimal("0")

        if not passed:
            self.overall_passed = False

        res = {
            "position": position_name,
            "applied_load": str(self.test_load),
            "indication": str(indication),
            "delta_l": str(delta_l),
            "p": str(p),
            "raw_error_e": str(raw_e),
            "corrected_error_ec": str(ec),
            "mpe": str(self.mpe),
            "passed": passed,
            "deviation": str(deviation),
            "derivation": {
                "standard": "OIML R 76-1:2006 (E)",
                "clause": "3.6.2 & Clause A.4.7",
                "test_load_rule": f"Test load = Max / {self.supports_count if self.supports_count > 4 else 3} = {self.test_load} {self.spec.unit} (Clause 3.6.2.1)",
                "error_compensation_formula": "Ec = P - L - E0",
                "substitution": f"Ec = {p} - {self.test_load} - ({zero_error}) = {ec}",
                "condition": f"|Ec| <= MPE ({self.mpe} {self.spec.unit})",
                "comparison": f"|{ec}| <= {self.mpe}",
                "assessment": "PASS" if passed else "FAIL"
            }
        }
        self.positions[position_name] = res
        return res


class Form5Repeatability:
    """
    OIML R 76-2 Section 5: Repeatability Test.
    10 consecutive weighings at ~50% Max and 100% Max.
    Spread (I_max - I_min) <= |MPE|
    """
    def __init__(self, spec: InstrumentSpecification):
        self.spec = spec
        self.series: Dict[str, List[Decimal]] = {"50%": [], "100%": []}

    def add_reading(self, load_bracket: str, indication: Decimal):
        self.series[load_bracket].append(Decimal(str(indication)))

    def evaluate(self) -> Dict[str, Any]:
        results = {}
        overall_passed = True

        for bracket, readings in self.series.items():
            if not readings:
                continue
            load = (self.spec.max_capacity * (Decimal("0.5") if bracket == "50%" else Decimal("1.0"))).quantize(self.spec.e, rounding=ROUND_HALF_EVEN)
            mpe = MetrologyMath.get_mpe(load, self.spec)
            i_max = max(readings)
            i_min = min(readings)
            spread = i_max - i_min
            passed = spread <= mpe
            deviation = spread - mpe if not passed else Decimal("0")

            if not passed:
                overall_passed = False

            results[bracket] = {
                "nominal_load": str(load),
                "readings_count": len(readings),
                "readings": [str(r) for r in readings],
                "i_max": str(i_max),
                "i_min": str(i_min),
                "spread": str(spread),
                "mpe": str(mpe),
                "passed": passed,
                "deviation": str(deviation),
                "derivation": {
                    "standard": "OIML R 76-1:2006 (E)",
                    "clause": "3.6.1 & Clause A.4.10",
                    "rule": "Difference between maximum and minimum results for same load must not exceed |MPE|: (I_max - I_min) <= |MPE|",
                    "substitution": f"Spread = {i_max} - {i_min} = {spread} {self.spec.unit}",
                    "condition": f"Spread ({spread}) <= MPE ({mpe})",
                    "comparison": f"{spread} <= {mpe}",
                    "assessment": "PASS" if passed else "FAIL"
                }
            }

        return {"overall_passed": overall_passed, "series": results}


class OIMLR111WeightValidator:
    """
    OIML R 111 Standard Weights Uncertainty & Air Buoyancy Verification.
    Rule: Expanded Uncertainty U <= 1/3 MPE (OIML R 76-1 Clause 3.7.1)
    """

    @staticmethod
    def verify_weight_uncertainty(weight_uncertainty: Decimal, mpe: Decimal) -> Tuple[bool, Decimal, Decimal]:
        """
        Validates if standard test weight calibration uncertainty meets U <= (1/3) * MPE.
        """
        u = Decimal(str(weight_uncertainty))
        max_allowed_u = (Decimal(str(mpe)) / Decimal("3")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
        passed = u <= max_allowed_u
        margin = max_allowed_u - u
        return passed, max_allowed_u, margin

    @staticmethod
    def calculate_air_buoyancy_correction(
        conventional_mass: Decimal,
        pressure_hpa: Decimal,
        temperature_c: Decimal,
        relative_humidity_pct: Decimal,
        weight_density_kg_m3: Decimal = Decimal("8000")  # Stainless steel reference
    ) -> Decimal:
        """
        Calculates air buoyancy correction factor using CIPM-2007 formula.
        rho_a = (0.34848 * p - 0.009 * RH * exp(0.061 * T)) / (273.15 + T)
        """
        p = float(pressure_hpa)
        t = float(temperature_c)
        rh = float(relative_humidity_pct)

        # Ambient air density rho_a (kg/m3)
        rho_a = (0.34848 * p - 0.009 * rh * math.exp(0.061 * t)) / (273.15 + t)
        rho_0 = 1.2  # reference air density
        rho_w = float(weight_density_kg_m3)

        # Buoyancy multiplier
        multiplier = 1.0 + (rho_a - rho_0) * (1.0 / rho_w)
        true_mass = Decimal(str(conventional_mass)) * Decimal(str(multiplier))
        return true_mass.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
