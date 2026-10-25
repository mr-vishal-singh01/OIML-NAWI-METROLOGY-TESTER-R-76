"""
OIML R 76-2 Form 15: Examination of Software-Controlled Weighing Instruments
Conforming to OIML R 76-1:2006 Clause 5.5 and WELMEC Guide 7.2 (Software Guide)
SIH26035: Non-Automatic Weighing Instruments Automated Test Suite
"""

from typing import Dict, Any, List, Optional
from enum import Enum

class SoftwareArchitectureType(str, Enum):
    TYPE_P = "Type P (Built-in / Dedicated Embedded System)"
    TYPE_U = "Type U (Universal Computer / PC / POS System)"

class WelmecRiskClass(str, Enum):
    CLASS_B = "Risk Class B (Low economic impact)"
    CLASS_C = "Risk Class C (Commercial trade, retail, industrial)"
    CLASS_D = "Risk Class D (Highways weighbridges, precious metals, legal evidence)"

class SoftwareCheckItem:
    def __init__(
        self,
        item_id: str,
        clause_oiml: str,
        welmec_ref: str,
        title: str,
        passed: bool,
        remarks: str = "",
        evidence_digest: Optional[str] = None
    ):
        self.item_id = item_id
        self.clause_oiml = clause_oiml
        self.welmec_ref = welmec_ref
        self.title = title
        self.passed = passed
        self.remarks = remarks
        self.evidence_digest = evidence_digest

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "clause_oiml": self.clause_oiml,
            "welmec_ref": self.welmec_ref,
            "title": self.title,
            "passed": self.passed,
            "remarks": self.remarks,
            "evidence_digest": self.evidence_digest
        }

class Form15SoftwareExamination:
    """
    OIML R 76-2 Section 15: Formal Examination Engine for Software-Equipped NAWIs.
    Evaluates Software Identification, Software Separation, Audit Trail, and Data Protection.
    """

    def __init__(
        self,
        architecture_type: SoftwareArchitectureType = SoftwareArchitectureType.TYPE_P,
        risk_class: WelmecRiskClass = WelmecRiskClass.CLASS_C
    ):
        self.architecture_type = architecture_type
        self.risk_class = risk_class
        self.checks: List[SoftwareCheckItem] = []

    def add_standard_checks(
        self,
        software_id_verified: bool,
        checksum_verified: bool,
        checksum_value: str,
        software_separation_verified: bool,
        parameter_protection_verified: bool,
        audit_trail_counter_working: bool,
        event_counter_value: int,
        power_failure_protection_verified: bool
    ):
        self.checks = [
            SoftwareCheckItem(
                item_id="SW-01",
                clause_oiml="5.5.1",
                welmec_ref="Guide 7.2 Requirement 1",
                title="Software Identification and Version Display",
                passed=software_id_verified,
                remarks="Software ID visible upon startup or designated command sequence."
            ),
            SoftwareCheckItem(
                item_id="SW-02",
                clause_oiml="5.5.1",
                welmec_ref="Guide 7.2 Requirement 2",
                title="Cryptographic Checksum / Hash Integrity Verification",
                passed=checksum_verified,
                remarks=f"Verified against manufacturer type approval documentation. Value: {checksum_value}",
                evidence_digest=checksum_value
            ),
            SoftwareCheckItem(
                item_id="SW-03",
                clause_oiml="5.5.2.1",
                welmec_ref="Guide 7.2 Requirement 3 (Extension L)",
                title="Software Separation (Legally Relevant vs Non-Legally Relevant)",
                passed=software_separation_verified,
                remarks="Metrological calculations mathematically isolated from UI and OS services."
            ),
            SoftwareCheckItem(
                item_id="SW-04",
                clause_oiml="5.5.2.2",
                welmec_ref="Guide 7.2 Requirement 4",
                title="Protection of Metrological Adjustment Parameters",
                passed=parameter_protection_verified,
                remarks="Calibration jumper / hardware lock or cryptographic password protection confirmed."
            ),
            SoftwareCheckItem(
                item_id="SW-05",
                clause_oiml="5.5.3",
                welmec_ref="Guide 7.2 Requirement 5",
                title="Audit Trail / Event Counter Increment Verification",
                passed=audit_trail_counter_working,
                remarks=f"Event counter correctly incremented upon parameter alteration. Current count: {event_counter_value}"
            ),
            SoftwareCheckItem(
                item_id="SW-06",
                clause_oiml="5.5.4",
                welmec_ref="Guide 7.2 Requirement 6",
                title="Data Retention & Integrity on Sudden Power Interruption",
                passed=power_failure_protection_verified,
                remarks="Incomplete transaction discarded or non-volatile storage verified without corrupt state."
            )
        ]

    @property
    def overall_passed(self) -> bool:
        if not self.checks:
            return False
        return all(c.passed for c in self.checks)

    def evaluate(self) -> Dict[str, Any]:
        return {
            "passed": self.overall_passed,
            "overall_passed": self.overall_passed,
            "checks": [c.to_dict() for c in self.checks],
            "architecture_type": self.architecture_type.value,
            "risk_class": self.risk_class.value
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "architecture_type": self.architecture_type.value,
            "risk_class": self.risk_class.value,
            "overall_software_conformity": "PASSED" if self.overall_passed else "FAILED",
            "checks": [c.to_dict() for c in self.checks]
        }

if __name__ == "__main__":
    form15 = Form15SoftwareExamination()
    form15.add_standard_checks(
        software_id_verified=True,
        checksum_verified=True,
        checksum_value="SHA256:7B12C...CRC32:89A4E21D",
        software_separation_verified=True,
        parameter_protection_verified=True,
        audit_trail_counter_working=True,
        event_counter_value=14,
        power_failure_protection_verified=True
    )
    print("Form 15 Overall Passed:", form15.overall_passed)
    print("Check items count:", len(form15.checks))
