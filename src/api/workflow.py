"""
NAWI Testing Workflow & Revision Lifecycle Engine
Conforming to OIML R 76-1:2006 (E) Initial Verification Class III rules.

Implements the atomic sequence:
Amendment saved -> previous dependent results become stale -> recalculation completes 
for the new revision -> current assessment updated -> renewed review remains required.
"""

import sys
from pathlib import Path
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from enum import Enum
from typing import Dict, Any, List, Optional
import uuid
import copy
from datetime import datetime, timezone

# Ensure backend root is in sys.path
_backend_root = str(Path(__file__).resolve().parent.parent)
if _backend_root not in sys.path:
    sys.path.insert(0, _backend_root)

getcontext().prec = 28
getcontext().rounding = ROUND_HALF_EVEN

from core.nawi_engine import (
    InstrumentSpecification,
    AccuracyClass,
    VerificationType,
    MetrologyMath,
    Form3Eccentricity,
    Form5Repeatability
)
from core.software_examination import (
    Form15SoftwareExamination,
    SoftwareArchitectureType,
    WelmecRiskClass
)
from api.audit_trail import ImmutableAuditTrail

ENGINE_RULE_VERSION = "OIML-R76-1:2006-INITIAL-VERIFICATION-v1.0"


class SessionCompletionStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"


class ReportReviewStatus(str, Enum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REQUIRES_RE_REVIEW = "REQUIRES_RE_REVIEW"
    SUPERSEDED = "SUPERSEDED"


class InstrumentAssessment(str, Enum):
    UNTESTED = "UNTESTED"
    PASSED = "PASSED"
    FAILED = "FAILED"


class ObservationRecord:
    """Represents an immutable observation entry for a specific revision."""
    def __init__(
        self,
        step_index: int,
        load: Decimal,
        indication: Decimal,
        delta_l: Decimal,
        direction: str = "ascending",
        operator_id: str = "OPERATOR_1",
        revision: int = 1,
        edit_reason: Optional[str] = None
    ):
        self.observation_id = str(uuid.uuid4())
        self.step_index = step_index
        self.load = Decimal(str(load))
        self.indication = Decimal(str(indication))
        self.delta_l = Decimal(str(delta_l))
        self.direction = direction.lower()
        self.operator_id = operator_id
        self.revision = revision
        self.edit_reason = edit_reason
        self.timestamp_iso = datetime.now(timezone.utc).isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "step_index": self.step_index,
            "load": str(self.load),
            "indication": str(self.indication),
            "delta_l": str(self.delta_l),
            "direction": self.direction,
            "operator_id": self.operator_id,
            "revision": self.revision,
            "edit_reason": self.edit_reason,
            "timestamp_iso": self.timestamp_iso
        }


class CalculationSnapshot:
    """Authoritative calculation result bound strictly to an observation revision and rule version."""
    def __init__(
        self,
        observation_id: str,
        observation_revision: int,
        instrument_snapshot_id: str,
        engine_version: str,
        step_index: int,
        p: Decimal,
        raw_error_e: Decimal,
        corrected_error_ec: Decimal,
        mpe: Decimal,
        passed: bool,
        deviation: Decimal,
        derivation: Dict[str, Any],
        is_stale: bool = False
    ):
        self.calculation_id = str(uuid.uuid4())
        self.observation_id = observation_id
        self.observation_revision = observation_revision
        self.instrument_snapshot_id = instrument_snapshot_id
        self.engine_version = engine_version
        self.step_index = step_index
        self.p = p
        self.raw_error_e = raw_error_e
        self.corrected_error_ec = corrected_error_ec
        self.mpe = mpe
        self.passed = passed
        self.deviation = deviation
        self.derivation = derivation
        self.is_stale = is_stale
        self.calculated_at_iso = datetime.now(timezone.utc).isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "calculation_id": self.calculation_id,
            "observation_id": self.observation_id,
            "observation_revision": self.observation_revision,
            "instrument_snapshot_id": self.instrument_snapshot_id,
            "engine_version": self.engine_version,
            "step_index": self.step_index,
            "p": str(self.p),
            "raw_error_e": str(self.raw_error_e),
            "corrected_error_ec": str(self.corrected_error_ec),
            "mpe": str(self.mpe),
            "passed": self.passed,
            "deviation": str(self.deviation),
            "is_stale": self.is_stale,
            "derivation": self.derivation,
            "calculated_at_iso": self.calculated_at_iso
        }


class ReportRevisionSnapshot:
    """An immutable snapshot of a reviewed prototype test report revision."""
    def __init__(
        self,
        revision_number: int,
        reviewer_id: str,
        review_status: ReportReviewStatus,
        instrument_verdict: InstrumentAssessment,
        instrument_snapshot: Dict[str, Any],
        engine_version: str,
        observations: List[Dict[str, Any]],
        calculations: List[Dict[str, Any]],
        diagnostics: Dict[str, Any],
        review_comments: str = "",
        eccentricity_results: Optional[Dict[str, Any]] = None,
        repeatability_results: Optional[Dict[str, Any]] = None,
        software_exam_results: Optional[Dict[str, Any]] = None
    ):
        self.snapshot_id = str(uuid.uuid4())
        self.revision_number = revision_number
        self.reviewer_id = reviewer_id
        self.review_status = review_status
        self.instrument_verdict = instrument_verdict
        self.instrument_snapshot = copy.deepcopy(instrument_snapshot)
        self.engine_version = engine_version
        self.observations = copy.deepcopy(observations)
        self.calculations = copy.deepcopy(calculations)
        self.diagnostics = copy.deepcopy(diagnostics)
        self.review_comments = review_comments
        self.eccentricity_results = copy.deepcopy(eccentricity_results) if eccentricity_results else {}
        self.repeatability_results = copy.deepcopy(repeatability_results) if repeatability_results else {}
        self.software_exam_results = copy.deepcopy(software_exam_results) if software_exam_results else {}
        self.created_at_iso = datetime.now(timezone.utc).isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "revision_number": self.revision_number,
            "reviewer_id": self.reviewer_id,
            "review_status": self.review_status.value,
            "instrument_verdict": self.instrument_verdict.value,
            "instrument_snapshot": self.instrument_snapshot,
            "engine_version": self.engine_version,
            "observations_count": len(self.observations),
            "calculations_count": len(self.calculations),
            "diagnostics": self.diagnostics,
            "review_comments": self.review_comments,
            "eccentricity_results": self.eccentricity_results,
            "repeatability_results": self.repeatability_results,
            "software_exam_results": self.software_exam_results,
            "created_at_iso": self.created_at_iso
        }


class TestSessionWorkflow:
    """
    Authoritative test session workflow manager
    """
    __test__ = False
    """ for single-interval Class III weighing performance.
    """
    def __init__(self, session_id: str, spec: InstrumentSpecification):
        self.session_id = session_id
        self.spec = spec
        self.instrument_snapshot_id = str(uuid.uuid4())
        self.instrument_snapshot = {
            "snapshot_id": self.instrument_snapshot_id,
            "manufacturer": spec.manufacturer,
            "model": spec.model,
            "serial_number": spec.serial_number,
            "accuracy_class": spec.accuracy_class.value,
            "max_capacity": str(spec.max_capacity),
            "min_capacity": str(spec.min_capacity),
            "e": str(spec.e),
            "d": str(spec.d),
            "unit": spec.unit,
            "testing_context": "Initial Verification per OIML R 76-1:2006 Clause 3.5.1"
        }
        self.engine_version = ENGINE_RULE_VERSION
        self.current_revision: int = 1
        self.completion_status = SessionCompletionStatus.NOT_STARTED
        self.review_status = ReportReviewStatus.DRAFT
        self.instrument_verdict = InstrumentAssessment.UNTESTED

        self.observations: Dict[int, ObservationRecord] = {}
        self.observation_history: List[ObservationRecord] = []
        self.calculations: Dict[int, CalculationSnapshot] = {}
        self.calculation_history: List[CalculationSnapshot] = []
        self.zero_error_e0: Decimal = Decimal("0")
        self.archived_report_revisions: List[ReportRevisionSnapshot] = []
        self.audit_trail = ImmutableAuditTrail()

        # Multi-Form Metrology Testing Engines
        self.form3 = Form3Eccentricity(self.spec)
        self.form5 = Form5Repeatability(self.spec)
        self.form15 = Form15SoftwareExamination()

    def set_zero_reading(self, indication: Decimal, delta_l: Decimal, operator_id: str = "OPERATOR_1"):
        """
        Establishes error at zero load (E0 = P0 - L0) per Clause A.4.4.3.
        """
        p0 = MetrologyMath.calculate_turning_point(indication, delta_l, self.spec.e, self.spec.d)
        self.zero_error_e0 = MetrologyMath.calculate_raw_error(p0, Decimal("0"))
        
        zero_obs = ObservationRecord(
            step_index=0,
            load=Decimal("0"),
            indication=indication,
            delta_l=delta_l,
            direction="ascending",
            operator_id=operator_id,
            revision=self.current_revision
        )
        self.observations[0] = zero_obs
        self.observation_history.append(zero_obs)

    def record_observation(
        self,
        step_index: int,
        load: Decimal,
        indication: Decimal,
        delta_l: Decimal,
        direction: str = "ascending",
        operator_id: str = "OPERATOR_1"
    ) -> CalculationSnapshot:
        obs = ObservationRecord(
            step_index=step_index,
            load=load,
            indication=indication,
            delta_l=delta_l,
            direction=direction,
            operator_id=operator_id,
            revision=self.current_revision
        )
        self.observations[step_index] = obs
        self.observation_history.append(obs)
        self.completion_status = SessionCompletionStatus.IN_PROGRESS

        calc = self._evaluate_observation(obs)
        self.calculations[step_index] = calc
        self.calculation_history.append(calc)
        self._update_instrument_verdict()
        return calc

    def amend_observation(
        self,
        step_index: int,
        new_indication: Decimal,
        new_delta_l: Decimal,
        operator_id: str,
        edit_reason: str
    ) -> CalculationSnapshot:
        """
        Atomic Amendment Sequence:
        1. Validates presence and reason.
        2. Previous calculation marked STALE and archived.
        3. Revision index advances.
        4. New observation record created.
        5. Recalculation completes with fresh inputs for new revision.
        6. Instrument assessment updated (e.g. FAILED).
        7. Review status shifts to REQUIRES_RE_REVIEW.
        """
        if step_index not in self.observations:
            raise KeyError(f"No observation found for step {step_index}")

        if not edit_reason or not edit_reason.strip():
            raise ValueError("An explicit edit_reason is mandatory when amending observations.")

        old_obs = self.observations[step_index]

        # Step A: Invalidate previous calculation
        if step_index in self.calculations:
            old_calc = self.calculations[step_index]
            old_calc.is_stale = True

        # Step B: Advance revision counter
        self.current_revision += 1

        # Step C: Save new observation record
        new_obs = ObservationRecord(
            step_index=step_index,
            load=old_obs.load,
            indication=new_indication,
            delta_l=new_delta_l,
            direction=old_obs.direction,
            operator_id=operator_id,
            revision=self.current_revision,
            edit_reason=edit_reason.strip()
        )
        self.observations[step_index] = new_obs
        self.observation_history.append(new_obs)

        # Step D: Recalculation executes immediately for new revision
        new_calc = self._evaluate_observation(new_obs)
        new_calc.is_stale = False
        self.calculations[step_index] = new_calc
        self.calculation_history.append(new_calc)

        # Step E: Instrument assessment reflects latest recalculation
        self._update_instrument_verdict()

        # Step F: Renewed review is now required
        if self.review_status in (ReportReviewStatus.APPROVED, ReportReviewStatus.UNDER_REVIEW):
            self.review_status = ReportReviewStatus.REQUIRES_RE_REVIEW

        return new_calc

    def record_eccentricity_position(
        self,
        position_name: str,
        indication: Decimal,
        delta_l: Decimal,
        operator_id: str = "OPERATOR_1"
    ) -> Dict[str, Any]:
        res = self.form3.record_position(position_name, indication, delta_l, self.zero_error_e0)
        res["operator_id"] = operator_id
        res["revision"] = self.current_revision
        self.completion_status = SessionCompletionStatus.IN_PROGRESS
        self._update_instrument_verdict()
        return res

    def amend_eccentricity_position(
        self,
        position_name: str,
        new_indication: Decimal,
        new_delta_l: Decimal,
        operator_id: str,
        edit_reason: str
    ) -> Dict[str, Any]:
        if position_name not in self.form3.positions:
            raise KeyError(f"No eccentricity observation recorded for position {position_name}")
        if not edit_reason or not edit_reason.strip():
            raise ValueError("An explicit edit_reason is mandatory when amending observations.")
        
        self.current_revision += 1
        res = self.form3.record_position(position_name, new_indication, new_delta_l, self.zero_error_e0)
        res["operator_id"] = operator_id
        res["revision"] = self.current_revision
        res["edit_reason"] = edit_reason.strip()

        if self.review_status in (ReportReviewStatus.APPROVED, ReportReviewStatus.UNDER_REVIEW):
            self.review_status = ReportReviewStatus.REQUIRES_RE_REVIEW

        self._update_instrument_verdict()
        return res

    def record_repeatability_reading(
        self,
        load_bracket: str,
        indication: Decimal,
        operator_id: str = "OPERATOR_1"
    ) -> Dict[str, Any]:
        self.form5.add_reading(load_bracket, indication)
        self.completion_status = SessionCompletionStatus.IN_PROGRESS
        res = self.form5.evaluate()
        self._update_instrument_verdict()
        return res

    def evaluate_repeatability(self) -> Dict[str, Any]:
        return self.form5.evaluate()

    def setup_software_examination(
        self,
        software_id_verified: bool = True,
        checksum_verified: bool = True,
        checksum_value: str = "SHA256:4a8c9b2f7d1e84a2",
        software_separation_verified: bool = True,
        parameter_protection_verified: bool = True,
        audit_trail_counter_working: bool = True,
        event_counter_value: int = 1,
        power_failure_protection_verified: bool = True
    ) -> Dict[str, Any]:
        self.form15.add_standard_checks(
            software_id_verified=software_id_verified,
            checksum_verified=checksum_verified,
            checksum_value=checksum_value,
            software_separation_verified=software_separation_verified,
            parameter_protection_verified=parameter_protection_verified,
            audit_trail_counter_working=audit_trail_counter_working,
            event_counter_value=event_counter_value,
            power_failure_protection_verified=power_failure_protection_verified
        )
        self._update_instrument_verdict()
        return self.form15.evaluate()

    def check_completeness(self) -> Dict[str, Any]:
        missing = []
        if 0 not in self.observations:
            missing.append("Zero reference load reading (Step 0 / E0)")
        form1_steps = [s for s in self.observations.keys() if s > 0]
        if len(form1_steps) < 2:
            missing.append("Form 1: Insufficient weighing steps (at least 2 required)")
        
        expected_positions = {"Center", "Front-Left", "Back-Left", "Back-Right", "Front-Right"}
        recorded_positions = set(self.form3.positions.keys())
        if not expected_positions.issubset(recorded_positions):
            missing_pos = sorted(list(expected_positions - recorded_positions))
            missing.append(f"Form 3: Missing corner load positions: {', '.join(missing_pos)}")

        rep_has_readings = any(len(readings) >= 3 for readings in self.form5.series.values())
        if not rep_has_readings:
            missing.append("Form 5: At least one repeatability series with >= 3 readings required")

        is_complete = len(missing) == 0
        if is_complete:
            self.completion_status = SessionCompletionStatus.COMPLETE

        return {
            "complete": is_complete,
            "missing_requirements": missing,
            "form1_steps_count": len(form1_steps),
            "form3_positions_recorded": sorted(list(self.form3.positions.keys())),
            "form5_series_counts": {k: len(v) for k, v in self.form5.series.items()},
            "software_checks_count": len(self.form15.checks)
        }

    def approve_report_revision(
        self,
        reviewer_id: str,
        expected_revision: int,
        comments: str = "",
        enforce_completeness: bool = False
    ) -> ReportRevisionSnapshot:
        """
        Approves the report revision with optimistic locking.
        Rejects if the revision changed after the reviewer loaded it.
        """
        if expected_revision != self.current_revision:
            raise RuntimeError(
                f"Concurrency Conflict: Review submitted for revision #{expected_revision}, "
                f"but session has advanced to revision #{self.current_revision}."
            )

        if any(c.is_stale for c in self.calculations.values()):
            raise RuntimeError("Cannot approve report revision: One or more calculations are STALE.")

        if len(self.observations) < 2:
            raise RuntimeError("Cannot approve report revision: Required observation points missing.")

        if enforce_completeness:
            comp = self.check_completeness()
            if not comp["complete"]:
                raise RuntimeError(
                    f"Cannot approve report revision: Session is incomplete. Missing: {', '.join(comp['missing_requirements'])}"
                )

        self.review_status = ReportReviewStatus.APPROVED
        
        obs_payload = [o.to_dict() for o in self.observations.values()]
        calc_payload = [c.to_dict() for c in self.calculations.values()]
        diagnostics = self._compute_diagnostic_data()

        ecc_results = copy.deepcopy(self.form3.positions)
        rep_results = copy.deepcopy(self.form5.evaluate()) if any(self.form5.series.values()) else {}
        sw_results = copy.deepcopy(self.form15.evaluate()) if self.form15.checks else {}

        snapshot = ReportRevisionSnapshot(
            revision_number=self.current_revision,
            reviewer_id=reviewer_id,
            review_status=ReportReviewStatus.APPROVED,
            instrument_verdict=self.instrument_verdict,
            instrument_snapshot=self.instrument_snapshot,
            engine_version=self.engine_version,
            observations=obs_payload,
            calculations=calc_payload,
            diagnostics=diagnostics,
            review_comments=comments,
            eccentricity_results=ecc_results,
            repeatability_results=rep_results,
            software_exam_results=sw_results
        )
        self.archived_report_revisions.append(snapshot)
        return snapshot

    def _evaluate_observation(self, obs: ObservationRecord) -> CalculationSnapshot:
        active_e, active_d = MetrologyMath.get_active_partial_range(obs.load, self.spec)

        p = MetrologyMath.calculate_turning_point(obs.indication, obs.delta_l, active_e, active_d)
        raw_e = MetrologyMath.calculate_raw_error(p, obs.load)
        ec = MetrologyMath.calculate_corrected_error(raw_e, self.zero_error_e0)
        
        mpe_details = MetrologyMath.get_mpe_details(obs.load, self.spec, VerificationType.INITIAL)
        mpe = mpe_details["mpe_value"]
        passed = abs(ec) <= mpe
        deviation = abs(ec) - mpe if not passed else Decimal("0")

        derivation = {
            "clause_turning_point": "OIML R 76-1:2006 Clause A.4.4.3",
            "p_formula": "P = I + 0.5d - Delta_L",
            "p_substitution": f"P = {obs.indication} + 0.5*({active_d}) - {obs.delta_l} = {p}",
            "raw_error_formula": "E = P - L",
            "raw_error_substitution": f"E = {p} - {obs.load} = {raw_e}",
            "ec_formula": "Ec = E - E0",
            "ec_substitution": f"Ec = {raw_e} - ({self.zero_error_e0}) = {ec}",
            "clause_mpe": "OIML R 76-1:2006 Clause 3.5.1 & Table 6",
            "bracket": mpe_details["bracket"],
            "mpe_limit": str(mpe),
            "condition": f"|{ec}| <= {mpe}",
            "assessment": "PASS" if passed else "FAIL",
            "deviation": str(deviation)
        }

        return CalculationSnapshot(
            observation_id=obs.observation_id,
            observation_revision=obs.revision,
            instrument_snapshot_id=self.instrument_snapshot_id,
            engine_version=self.engine_version,
            step_index=obs.step_index,
            p=p,
            raw_error_e=raw_e,
            corrected_error_ec=ec,
            mpe=mpe,
            passed=passed,
            deviation=deviation,
            derivation=derivation,
            is_stale=False
        )

    def _compute_diagnostic_data(self) -> Dict[str, Any]:
        """Computes diagnostic hysteresis without asserting an unverified pass badge."""
        asc_map = {o.load: self.calculations[s] for s, o in self.observations.items() if o.direction == "ascending" and s in self.calculations}
        desc_map = {o.load: self.calculations[s] for s, o in self.observations.items() if o.direction == "descending" and s in self.calculations}
        
        pairs = []
        for load, c_asc in asc_map.items():
            if load in desc_map:
                c_desc = desc_map[load]
                diff = abs(c_desc.corrected_error_ec - c_asc.corrected_error_ec)
                pairs.append({
                    "load": str(load),
                    "asc_ec": str(c_asc.corrected_error_ec),
                    "desc_ec": str(c_desc.corrected_error_ec),
                    "hysteresis_difference": str(diff),
                    "note": "Informative diagnostic difference; regulatory evaluation pending verified procedure"
                })
        return {"hysteresis_diagnostic_pairs": pairs}

    def _update_instrument_verdict(self):
        active_calcs = [c for c in self.calculations.values() if not c.is_stale]
        form3_passed = self.form3.overall_passed if self.form3.positions else True
        
        rep_eval = self.form5.evaluate() if any(self.form5.series.values()) else {"overall_passed": True}
        form5_passed = rep_eval.get("overall_passed", True)

        form15_eval = self.form15.evaluate() if self.form15.checks else {"passed": True}
        form15_passed = form15_eval.get("passed", True)

        has_any_data = bool(active_calcs or self.form3.positions or any(self.form5.series.values()) or self.form15.checks)
        if not has_any_data:
            self.instrument_verdict = InstrumentAssessment.UNTESTED
            return

        form1_passed = all(c.passed for c in active_calcs) if active_calcs else True

        if not (form1_passed and form3_passed and form5_passed and form15_passed):
            self.instrument_verdict = InstrumentAssessment.FAILED
        else:
            self.instrument_verdict = InstrumentAssessment.PASSED

