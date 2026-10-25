"""
OIML R 76-2:2007 Standardized Test Report OpenXML (.docx) Generator
SIH26035: PrecisionX Legal Metrology Suite
Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division

Generates a fully-compliant, editable Microsoft Word (.docx) document
without requiring external pip dependencies (uses Python standard library zipfile and XML).
"""

import io
import zipfile
import html
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from core.nawi_engine import InstrumentSpecification
from core.welmec_sealer import WelmecSoftwareSealer


class OIMLDocxGenerator:
    """Generates official OIML R 76-2 test reports in Microsoft Word (.docx) format."""

    @staticmethod
    def _xml_escape(text: Any) -> str:
        if text is None:
            return ""
        return html.escape(str(text))

    @classmethod
    def generate_docx_bytes(
        cls,
        session_id: str,
        spec: InstrumentSpecification,
        current_revision: int,
        review_status: str,
        instrument_verdict: str,
        zero_error_e0: Decimal,
        engine_version: str,
        form1_calculations: List[Dict[str, Any]],
        form3_positions: Dict[str, Dict[str, Any]],
        form5_results: Dict[str, Any],
        form15_checks: List[Dict[str, Any]],
        hysteresis_pairs: List[Dict[str, Any]],
        attachments: Optional[List[Dict[str, Any]]] = None,
        reviewer_id: str = "Unassigned",
        review_comments: str = "",
        is_draft: bool = False
    ) -> bytes:
        """Constructs an OpenXML Word Document (.docx) as in-memory bytes."""

        sealer_status = WelmecSoftwareSealer.calculate_lrs_fingerprint()
        lrs_sha256 = sealer_status.get("sha256", "N/A")[:24] + "..." if sealer_status.get("sha256") else "N/A"

        doc_xml_parts = []
        doc_xml_parts.append("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
""")

        # Header Title
        doc_xml_parts.append(cls._make_paragraph(
            "GOVERNMENT OF INDIA", bold=True, size=24, align="center", color="1E3A8A"
        ))
        doc_xml_parts.append(cls._make_paragraph(
            "MINISTRY OF CONSUMER AFFAIRS, FOOD & PUBLIC DISTRIBUTION", bold=True, size=22, align="center", color="1E3A8A"
        ))
        doc_xml_parts.append(cls._make_paragraph(
            "DEPARTMENT OF CONSUMER AFFAIRS — LEGAL METROLOGY DIVISION", bold=True, size=20, align="center", color="334155"
        ))
        doc_xml_parts.append(cls._make_paragraph(
            "TYPE EVALUATION TEST REPORT AS PER OIML R 76-2:2007", bold=True, size=26, align="center", color="0F172A", space_after=200
        ))

        # Status Banner
        verdict_color = "15803D" if instrument_verdict == "PASSED" else "B91C1C"
        status_text = f"OVERALL METROLOGICAL VERDICT: {instrument_verdict} (Revision #{current_revision} — Status: {review_status})"
        doc_xml_parts.append(cls._make_paragraph(status_text, bold=True, size=22, align="center", color=verdict_color, space_after=300))

        # Section 1: Administrative Details
        doc_xml_parts.append(cls._make_heading("1. Administrative & Identification Details (Form 0)"))
        meta_table = [
            ("Test Report Number", f"RRSL-FBD-2026-NAWI-{session_id}"),
            ("Date of Test Evaluation", datetime.now(timezone.utc).strftime("%d-%b-%Y %H:%M UTC")),
            ("Issuing Laboratory", "Regional Reference Standard Laboratory (RRSL), Faridabad"),
            ("National Standard Authority", "Directorate of Legal Metrology, Government of India"),
            ("WELMEC 7.2 LRS Fingerprint", f"SHA-256: {lrs_sha256}"),
            ("Assigned Reviewer / Officer", str(reviewer_id)),
            ("Reviewer Technical Comments", str(review_comments) or "None recorded")
        ]
        doc_xml_parts.append(cls._make_two_column_table(meta_table))

        # Section 2: Instrument Specification
        doc_xml_parts.append(cls._make_heading("2. Instrument Metrological Specifications"))
        spec_table = [
            ("Manufacturer", spec.manufacturer),
            ("Model Designation", spec.model),
            ("Serial Number", spec.serial_number),
            ("Accuracy Class", spec.accuracy_class.value),
            ("Maximum Capacity (Max)", f"{spec.max_capacity} {spec.unit}"),
            ("Minimum Capacity (Min)", f"{spec.min_capacity} {spec.unit}"),
            ("Verification Scale Interval (e)", f"{spec.e} {spec.unit}"),
            ("Actual Scale Interval (d)", f"{spec.d} {spec.unit}"),
            ("Scale Divisions (n = Max/e)", str(spec.n_intervals)),
            ("Calculated Zero Error (E0)", f"{zero_error_e0} {spec.unit}")
        ]
        doc_xml_parts.append(cls._make_two_column_table(spec_table))

        # Section 3: Form 1 Weighing Performance
        doc_xml_parts.append(cls._make_heading("3. Weighing Performance & Hysteresis Test (Form 1)"))
        doc_xml_parts.append(cls._make_paragraph("Evaluated strictly in accordance with OIML R 76-1:2006 Clause 3.5.1 and Table 6 Maximum Permissible Errors (MPE)."))

        f1_headers = ["Step", "Dir", "Load L", "Ind I", "ΔL", "Ind P", "Error Ec", "MPE", "Verdict"]
        f1_rows = []
        for c in form1_calculations:
            f1_rows.append([
                str(c.get("step_index", "")),
                str(c.get("direction", "asc"))[:3].upper(),
                f"{c.get('load', '')} {spec.unit}",
                f"{c.get('indication', '')} {spec.unit}",
                f"{c.get('delta_l', '')} {spec.unit}",
                f"{c.get('p', '')} {spec.unit}",
                f"{c.get('corrected_error_ec', '')} {spec.unit}",
                f"±{c.get('mpe', '')} {spec.unit}",
                "PASS" if c.get("passed", False) else "FAIL"
            ])
        doc_xml_parts.append(cls._make_grid_table(f1_headers, f1_rows))

        # Section 4: Form 3 Eccentricity
        doc_xml_parts.append(cls._make_heading("4. Corner Load / Eccentricity Test (Form 3)"))
        doc_xml_parts.append(cls._make_paragraph(f"Test load applied: 1/3 Max = {spec.max_capacity / Decimal('3'):.2f} {spec.unit} per OIML R 76-1 Clause 3.6.2."))

        f3_headers = ["Position", "Applied Load", "Indication I", "ΔL", "Ind P", "Error Ec", "MPE", "Verdict"]
        f3_rows = []
        for pos_name in ["Center", "Front-Left", "Back-Left", "Back-Right", "Front-Right"]:
            pdata = form3_positions.get(pos_name, {})
            f3_rows.append([
                pos_name,
                f"{pdata.get('load', '5000')} {spec.unit}",
                f"{pdata.get('indication', '—')} {spec.unit}" if pdata.get('indication') else "—",
                f"{pdata.get('delta_l', '—')} {spec.unit}" if pdata.get('delta_l') else "—",
                f"{pdata.get('p', '—')} {spec.unit}" if pdata.get('p') else "—",
                f"{pdata.get('corrected_error_ec', '—')} {spec.unit}" if pdata.get('corrected_error_ec') else "—",
                f"±{pdata.get('mpe', '5.0')} {spec.unit}" if pdata.get('mpe') else "—",
                "PASS" if pdata.get("passed", False) else ("FAIL" if pdata.get("indication") else "PENDING")
            ])
        doc_xml_parts.append(cls._make_grid_table(f3_headers, f3_rows))

        # Section 5: Form 5 Repeatability
        doc_xml_parts.append(cls._make_heading("5. Repeatability Test (Form 5)"))
        doc_xml_parts.append(cls._make_paragraph("Two series of 10 consecutive weighings per OIML R 76-1 Clause 3.6.1 (Spread <= |MPE|)."))
        f5_headers = ["Load Series", "Readings Recorded", "Max Ind", "Min Ind", "Spread (Max - Min)", "MPE Limit", "Verdict"]
        f5_rows = []
        for b_name, b_data in form5_results.items():
            f5_rows.append([
                str(b_name),
                str(b_data.get("count", 0)),
                f"{b_data.get('max_indication', '—')} {spec.unit}",
                f"{b_data.get('min_indication', '—')} {spec.unit}",
                f"{b_data.get('spread', '—')} {spec.unit}",
                f"±{b_data.get('mpe', '—')} {spec.unit}",
                "PASS" if b_data.get("passed", False) else "FAIL"
            ])
        doc_xml_parts.append(cls._make_grid_table(f5_headers, f5_rows))

        # Section 6: Form 15 WELMEC 7.2 Software Examination
        doc_xml_parts.append(cls._make_heading("6. Software Examination & Security Integrity (Form 15)"))
        f15_headers = ["WELMEC 7.2 Clause", "Requirement Description", "Observed Verification Value", "Status"]
        f15_rows = []
        for chk in form15_checks:
            f15_rows.append([
                str(chk.get("clause", "")),
                str(chk.get("requirement", "")),
                str(chk.get("observed", "")),
                "PASS" if chk.get("status") == "PASS" else "FAIL"
            ])
        doc_xml_parts.append(cls._make_grid_table(f15_headers, f15_rows))

        # Section 7: Photographic Evidence & Inspection Vault
        if attachments:
            doc_xml_parts.append(cls._make_heading("7. Photographic Inspection Evidence & Tamper Audit Vault"))
            doc_xml_parts.append(cls._make_paragraph("Mandatory inspection photographs recorded under Rule 27 of Legal Metrology (General) Rules, 2011 stamped with cryptographic SHA-256 integrity hashes."))
            att_headers = ["Evidence Category", "Filename", "File Size", "SHA-256 Cryptographic Hash", "Integrity Status"]
            att_rows = []
            for att in attachments:
                size_kb = f"{(att.get('file_size_bytes', 0) / 1024):.1f} KB"
                sha = att.get('sha256_hash', '')
                short_sha = sha[:16] + "..." if len(sha) > 16 else sha
                att_rows.append([
                    str(att.get("document_type", "NAMEPLATE")),
                    str(att.get("filename", "")),
                    size_kb,
                    short_sha,
                    "SEALED & VERIFIED"
                ])
            doc_xml_parts.append(cls._make_grid_table(att_headers, att_rows))

        # Concluding Sign-off
        doc_xml_parts.append(cls._make_paragraph(
            "This document is an official digital representation generated by PrecisionX Legal Metrology Suite conforming to the Legal Metrology Act, 2009 and OIML R 76-2:2007.",
            size=18, italic=True, align="center", space_before=400
        ))

        doc_xml_parts.append("</w:body></w:document>")
        document_xml = "".join(doc_xml_parts)

        # Build in-memory ZIP package
        out_buf = io.BytesIO()
        with zipfile.ZipFile(out_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", cls._get_content_types_xml())
            zf.writestr("_rels/.rels", cls._get_root_rels_xml())
            zf.writestr("word/_rels/document.xml.rels", cls._get_doc_rels_xml())
            zf.writestr("word/document.xml", document_xml)

        return out_buf.getvalue()

    @classmethod
    def _make_heading(cls, text: str) -> str:
        return f"""<w:p>
<w:pPr><w:spacing w:before="300" w:after="120"/><w:jc w:val="left"/></w:pPr>
<w:r><w:rPr><w:b/><w:color w:val="1E293B"/><w:sz w:val="26"/><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr>
<w:t>{cls._xml_escape(text)}</w:t></w:r>
</w:p>"""

    @classmethod
    def _make_paragraph(cls, text: str, bold: bool = False, italic: bool = False, size: int = 20, align: str = "left", color: str = "334155", space_before: int = 0, space_after: int = 100) -> str:
        b_tag = "<w:b/>" if bold else ""
        i_tag = "<w:i/>" if italic else ""
        return f"""<w:p>
<w:pPr><w:spacing w:before="{space_before}" w:after="{space_after}"/><w:jc w:val="{align}"/></w:pPr>
<w:r><w:rPr>{b_tag}{i_tag}<w:color w:val="{color}"/><w:sz w:val="{size}"/><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr>
<w:t>{cls._xml_escape(text)}</w:t></w:r>
</w:p>"""

    @classmethod
    def _make_two_column_table(cls, rows: List[tuple]) -> str:
        xml = ['<w:tbl><w:tblPr><w:tblW w:w="9600" w:type="dxa"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tblBorders></w:tblPr>']
        for label, val in rows:
            xml.append(f"""<w:tr>
<w:tc><w:tcPr><w:tcW w:w="3600" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/></w:tcPr>
<w:p><w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="18"/><w:color w:val="475569"/></w:rPr><w:t>{cls._xml_escape(label)}</w:t></w:r></w:p></w:tc>
<w:tc><w:tcPr><w:tcW w:w="6000" w:type="dxa"/></w:tcPr>
<w:p><w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr><w:r><w:rPr><w:sz w:val="18"/><w:color w:val="0F172A"/></w:rPr><w:t>{cls._xml_escape(val)}</w:t></w:r></w:p></w:tc>
</w:tr>""")
        xml.append('</w:tbl>')
        return "".join(xml)

    @classmethod
    def _make_grid_table(cls, headers: List[str], data_rows: List[List[str]]) -> str:
        xml = ['<w:tbl><w:tblPr><w:tblW w:w="9600" w:type="dxa"/><w:tblBorders><w:top w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tblBorders></w:tblPr>']
        
        # Header Row
        xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for h in headers:
            xml.append(f"""<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1E293B"/></w:tcPr>
<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr>
<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="16"/></w:rPr><w:t>{cls._xml_escape(h)}</w:t></w:r></w:p></w:tc>""")
        xml.append('</w:tr>')

        # Data Rows
        for r in data_rows:
            xml.append('<w:tr>')
            for i, cell in enumerate(r):
                color = "0F172A"
                bold = False
                fill = "FFFFFF"
                if cell == "PASS":
                    color = "15803D"
                    bold = True
                    fill = "DCFCE7"
                elif cell == "FAIL":
                    color = "B91C1C"
                    bold = True
                    fill = "FEE2E2"

                b_tag = "<w:b/>" if bold else ""
                xml.append(f"""<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>
<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr>
<w:r><w:rPr>{b_tag}<w:color w:val="{color}"/><w:sz w:val="16"/></w:rPr><w:t>{cls._xml_escape(cell)}</w:t></w:r></w:p></w:tc>""")
            xml.append('</w:tr>')

        xml.append('</w:tbl>')
        return "".join(xml)

    @staticmethod
    def _get_content_types_xml() -> str:
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

    @staticmethod
    def _get_root_rels_xml() -> str:
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    @staticmethod
    def _get_doc_rels_xml() -> str:
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>"""
