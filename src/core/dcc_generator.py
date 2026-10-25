"""
PTB Digital Calibration Certificate (DCC v3.2.1) Generator with SmartCom D-SI
SIH26035: International Machine-Readable Legal Metrology XML Schema Builder
Conforms to PTB GEMIMEG-II and OIML Digital Metrology Guidelines
"""

import xml.etree.ElementTree as ET
import json
from xml.dom import minidom
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from decimal import Decimal

class DCCGenerator:
    """
    Constructs an ISO/IEC 17025 & OIML compliant Digital Calibration Certificate (DCC XML).
    """

    @staticmethod
    def generate_dcc_xml(
        certificate_id: str,
        instrument_metadata: Dict[str, Any],
        weighing_observations: List[Dict[str, Any]],
        laboratory_info: Dict[str, Any],
        lrs_fingerprint: Dict[str, Any],
        digital_seal: Optional[Dict[str, Any]] = None
    ) -> str:
        # Namespace definitions
        DCC_NS = "https://ptb.de/dcc"
        SI_NS = "https://ptb.de/si"
        XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

        ET.register_namespace("dcc", DCC_NS)
        ET.register_namespace("si", SI_NS)

        root = ET.Element(f"{{{DCC_NS}}}digitalCalibrationCertificate", {
            f"{{{XSI_NS}}}schemaLocation": f"{DCC_NS} https://ptb.de/dcc/v3.2.1/dcc.xsd",
            "schemaVersion": "3.2.1"
        })

        # 1. Administrative Data
        admin = ET.SubElement(root, f"{{{DCC_NS}}}administrativeData")
        
        # Core data
        core = ET.SubElement(admin, f"{{{DCC_NS}}}coreData")
        ET.SubElement(core, f"{{{DCC_NS}}}countryCodeISO3166_1").text = "IN"
        ET.SubElement(core, f"{{{DCC_NS}}}usedLangCodeISO639_1").text = "en"
        ET.SubElement(core, f"{{{DCC_NS}}}mandatoryLangCodeISO639_1").text = "en"
        ET.SubElement(core, f"{{{DCC_NS}}}uniqueIdentifier").text = certificate_id
        ET.SubElement(core, f"{{{DCC_NS}}}receiptDate").text = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ET.SubElement(core, f"{{{DCC_NS}}}beginPerformanceDate").text = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ET.SubElement(core, f"{{{DCC_NS}}}endPerformanceDate").text = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Calibration Laboratory
        cal_lab = ET.SubElement(admin, f"{{{DCC_NS}}}calibrationLaboratory")
        contact = ET.SubElement(cal_lab, f"{{{DCC_NS}}}contact")
        name = ET.SubElement(contact, f"{{{DCC_NS}}}name")
        ET.SubElement(name, f"{{{DCC_NS}}}content").text = laboratory_info.get("name", "Regional Reference Standard Laboratory (RRSL)")
        ET.SubElement(contact, f"{{{DCC_NS}}}city").text = laboratory_info.get("city", "Faridabad")
        ET.SubElement(contact, f"{{{DCC_NS}}}countryCodeISO3166_1").text = "IN"

        # Item under test
        item = ET.SubElement(admin, f"{{{DCC_NS}}}item")
        item_name = ET.SubElement(item, f"{{{DCC_NS}}}name")
        ET.SubElement(item_name, f"{{{DCC_NS}}}content").text = instrument_metadata.get("model", "NAWI Industrial Scale")
        ET.SubElement(item, f"{{{DCC_NS}}}manufacturer").text = instrument_metadata.get("manufacturer", "Standard Manufacturer")
        ET.SubElement(item, f"{{{DCC_NS}}}model").text = instrument_metadata.get("model", "Model-X")
        ET.SubElement(item, f"{{{DCC_NS}}}identifications")
        
        # WELMEC LRS Software Fingerprint
        sw_elem = ET.SubElement(admin, f"{{{DCC_NS}}}software")
        ET.SubElement(sw_elem, f"{{{DCC_NS}}}name").text = "SIH26035 Metrological LRS Kernel"
        ET.SubElement(sw_elem, f"{{{DCC_NS}}}version").text = "1.0.0-OIML-R76"
        ET.SubElement(sw_elem, f"{{{DCC_NS}}}sha256").text = lrs_fingerprint.get("sha256", "UNKNOWN")
        ET.SubElement(sw_elem, f"{{{DCC_NS}}}crc32").text = lrs_fingerprint.get("crc32", "UNKNOWN")

        # Cryptographic Statements & Ed25519 Digital Seal (RFC 8032)
        if digital_seal:
            statements = ET.SubElement(admin, f"{{{DCC_NS}}}statements")
            stmt = ET.SubElement(statements, f"{{{DCC_NS}}}statement", {"id": "ed25519_seal"})
            stmt_name = ET.SubElement(stmt, f"{{{DCC_NS}}}name")
            ET.SubElement(stmt_name, f"{{{DCC_NS}}}content").text = "RFC 8032 Ed25519 Metrological Seal"
            decl = ET.SubElement(stmt, f"{{{DCC_NS}}}declaration")
            ET.SubElement(decl, f"{{{DCC_NS}}}content").text = "Cryptographically verifiable offline seal binding OIML R 76 visual report to DCC measurement dataset"
            s_data = ET.SubElement(stmt, f"{{{DCC_NS}}}data")

            # Store serialized JSON for full envelope integrity
            env_json = json.dumps(digital_seal, separators=(",", ":"))
            entry = ET.SubElement(s_data, f"{{{DCC_NS}}}quantity", {"refType": "envelope_json"})
            qn = ET.SubElement(entry, f"{{{DCC_NS}}}name")
            ET.SubElement(qn, f"{{{DCC_NS}}}content").text = "envelope_json"
            real_el = ET.SubElement(entry, f"{{{SI_NS}}}real")
            ET.SubElement(real_el, f"{{{SI_NS}}}value").text = env_json
            ET.SubElement(real_el, f"{{{SI_NS}}}unit").text = "\\one"

            # Flatten core claims if available
            claims_dict = digital_seal.get("claims", {}) if isinstance(digital_seal.get("claims"), dict) else {}
            core_fields = {
                "sig": digital_seal.get("sig", ""),
                "pubkey_hex": digital_seal.get("pubkey_hex", "") or digital_seal.get("pub", ""),
                "cert_id": claims_dict.get("cert_id", "") or digital_seal.get("cert_id", ""),
                "sess_id": claims_dict.get("sess_id", "") or digital_seal.get("session_id", ""),
                "verdict": claims_dict.get("verdict", "") or digital_seal.get("verdict", ""),
                "rep_sha256": claims_dict.get("rep_sha256", "") or digital_seal.get("report_hash", ""),
                "lrs_sha256": claims_dict.get("lrs_sha256", "") or digital_seal.get("lrs_hash", ""),
                "ts": str(claims_dict.get("ts", "") or digital_seal.get("timestamp", ""))
            }
            for k, val in core_fields.items():
                if val:
                    f_entry = ET.SubElement(s_data, f"{{{DCC_NS}}}quantity", {"refType": k})
                    f_qn = ET.SubElement(f_entry, f"{{{DCC_NS}}}name")
                    ET.SubElement(f_qn, f"{{{DCC_NS}}}content").text = k
                    f_real = ET.SubElement(f_entry, f"{{{SI_NS}}}real")
                    ET.SubElement(f_real, f"{{{SI_NS}}}value").text = str(val)
                    ET.SubElement(f_real, f"{{{SI_NS}}}unit").text = "\\one"

        # 2. Measurement Results
        results = ET.SubElement(root, f"{{{DCC_NS}}}measurementResults")
        res_node = ET.SubElement(results, f"{{{DCC_NS}}}measurementResult")
        ET.SubElement(res_node, f"{{{DCC_NS}}}name").text = "OIML R 76-2 Weighing Performance Test Results"

        data_list = ET.SubElement(res_node, f"{{{DCC_NS}}}data")
        table = ET.SubElement(data_list, f"{{{DCC_NS}}}table")

        for obs in weighing_observations:
            row = ET.SubElement(table, f"{{{DCC_NS}}}row")
            ET.SubElement(row, f"{{{DCC_NS}}}step").text = str(obs.get("step_index"))
            ET.SubElement(row, f"{{{DCC_NS}}}direction").text = str(obs.get("direction"))
            
            # Load with SmartCom D-SI
            load_el = ET.SubElement(row, f"{{{SI_NS}}}real")
            ET.SubElement(load_el, f"{{{SI_NS}}}value").text = str(obs.get("applied_load"))
            ET.SubElement(load_el, f"{{{SI_NS}}}unit").text = r"\gram"

            # Indication
            ind_el = ET.SubElement(row, f"{{{SI_NS}}}real")
            ET.SubElement(ind_el, f"{{{SI_NS}}}value").text = str(obs.get("indicated_value"))
            ET.SubElement(ind_el, f"{{{SI_NS}}}unit").text = r"\gram"

            # Corrected Error Ec
            ec_el = ET.SubElement(row, f"{{{SI_NS}}}real")
            ET.SubElement(ec_el, f"{{{SI_NS}}}value").text = str(obs.get("corrected_error_ec"))
            ET.SubElement(ec_el, f"{{{SI_NS}}}unit").text = r"\gram"

            # Pass/Fail
            ET.SubElement(row, f"{{{DCC_NS}}}conformity").text = "PASS" if obs.get("passed") else "FAIL"

        # XML pretty print
        raw_xml = ET.tostring(root, encoding="utf-8")
        parsed = minidom.parseString(raw_xml)
        return parsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    xml_out = DCCGenerator.generate_dcc_xml(
        certificate_id="RRSL-FBD-2026-0092",
        instrument_metadata={"model": "Precision-Scale-5000", "manufacturer": "Essae-Teraoka"},
        weighing_observations=[
            {"step_index": 1, "direction": "ascending", "applied_load": "100.0", "indicated_value": "100.0", "corrected_error_ec": "0.0", "passed": True}
        ],
        laboratory_info={"name": "Regional Reference Standard Laboratory", "city": "Faridabad"},
        lrs_fingerprint={"sha256": "abcdef123456", "crc32": "1A2B3C4D"}
    )
    print("Generated PTB DCC XML preview (first 400 chars):")
    print(xml_out[:400])
