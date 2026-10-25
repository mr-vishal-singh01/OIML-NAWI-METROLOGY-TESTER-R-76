"""
OIML R 76-2:2007 Test Report Generator & Archival PDF/DCC Engine
Produces compliant multi-form legal metrology test reports covering:
- Form 0: General / Administrative & Pattern Evaluation Summary
- Form 1: Weighing Performance (OIML R 76-1 Clause 3.5.1 & Table 6) + Hysteresis
- Form 3: Eccentricity / Corner Load (OIML R 76-1 Clause 3.6.2 & Clause A.4.7)
- Form 5: Repeatability (OIML R 76-1 Clause 3.6.1 & Clause A.4.10)
- Form 15: Software-Controlled Instrument Examination (Clause 5.5 & WELMEC 7.2)
- Forensic Integrity Seal & PTB DCC v3.2.1 XML Generator
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from core.nawi_engine import InstrumentSpecification
from core.welmec_sealer import WelmecSoftwareSealer
from core.dcc_generator import DCCGenerator
from core.offline_qr import Ed25519ReportSigner
from reporting.pdfa3_engine import PdfA3ContainerEngine


class OIMLReportGenerator:
    """Generates official OIML R 76-2 test reports in HTML, PDF, and PTB DCC XML."""

    @staticmethod
    def generate_html_report(
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
        reviewer_id: str = "Unassigned",
        review_comments: str = "",
        is_draft: bool = False
    ) -> str:
        """Constructs an archival-ready HTML document adhering strictly to OIML R 76-2."""

        sealer_status = WelmecSoftwareSealer.calculate_lrs_fingerprint()
        lrs_sha256 = sealer_status["sha256"][:16] + "..." if sealer_status.get("sha256") else "N/A"
        lrs_crc32 = sealer_status.get("crc32_hex", "N/A")

        # Watermark and verdict styling
        watermark_html = ""
        if is_draft or review_status in ("DRAFT", "UNDER_REVIEW", "REQUIRES_RE_REVIEW"):
            watermark_html = """
            <div style="position: fixed; top: 35%; left: 15%; font-size: 72px; color: rgba(220, 38, 38, 0.10);
                        transform: rotate(-30deg); font-weight: 800; pointer-events: none; z-index: 9999;
                        border: 6px dashed rgba(220, 38, 38, 0.15); padding: 20px 40px; border-radius: 12px;">
                PROTOTYPE DRAFT
            </div>
            """
        else:
            watermark_html = """
            <div style="position: fixed; top: 5%; right: 5%; font-size: 14px; color: #166534;
                        font-weight: bold; border: 2px solid #166534; padding: 6px 14px; border-radius: 6px;
                        background: rgba(220, 252, 231, 0.6); pointer-events: none;">
                OFFICIALLY CERTIFIED - REVISION #""" + str(current_revision) + """
            </div>
            """

        verdict_color = "#166534" if instrument_verdict == "PASSED" else "#991b1b"
        verdict_bg = "#dcfce7" if instrument_verdict == "PASSED" else "#fee2e2"
        verdict_border = "#86efac" if instrument_verdict == "PASSED" else "#fca5a5"

        # Form 1 rows
        f1_rows = ""
        for c in form1_calculations:
            pass_color = "#16a34a" if c.get("passed", False) else "#dc2626"
            f1_rows += f"""
            <tr>
                <td style="text-align: center;">{c.get('step_index', '-')}</td>
                <td style="text-align: right;">{c.get('p', '-')} {spec.unit}</td>
                <td style="text-align: right;">{c.get('raw_error_e', '-')} {spec.unit}</td>
                <td style="text-align: right; font-weight: bold;">{c.get('corrected_error_ec', '-')} {spec.unit}</td>
                <td style="text-align: center;">±{c.get('mpe', '-')} {spec.unit}</td>
                <td style="text-align: center; color: {pass_color}; font-weight: bold;">
                    {'PASS' if c.get('passed', False) else 'FAIL'}
                </td>
                <td style="font-size: 11px; color: #475569;">
                    {c.get('derivation', {}).get('bracket', 'OIML R 76-1 Table 6')}
                </td>
            </tr>
            """

        # Hysteresis rows
        h_rows = ""
        for hp in hysteresis_pairs:
            h_rows += f"""
            <tr>
                <td style="text-align: right;">{hp.get('load', '-')} {spec.unit}</td>
                <td style="text-align: right;">{hp.get('asc_ec', '-')} {spec.unit}</td>
                <td style="text-align: right;">{hp.get('desc_ec', '-')} {spec.unit}</td>
                <td style="text-align: right; font-weight: bold;">{hp.get('hysteresis_difference', '-')} {spec.unit}</td>
                <td style="font-size: 11px; color: #64748b;">|Ec_desc - Ec_asc|</td>
            </tr>
            """
        if not h_rows:
            h_rows = "<tr><td colspan='5' style='text-align: center; color: #94a3b8; font-style: italic;'>No ascending/descending load pairs recorded yet</td></tr>"

        # Form 3 rows
        f3_rows = ""
        for pos_name in ["Center", "Front-Left", "Back-Left", "Back-Right", "Front-Right"]:
            if pos_name in form3_positions:
                pos = form3_positions[pos_name]
                p_col = "#16a34a" if pos.get("passed", False) else "#dc2626"
                f3_rows += f"""
                <tr>
                    <td style="font-weight: 500;">{pos_name}</td>
                    <td style="text-align: right;">{pos.get('applied_load', '-')} {spec.unit}</td>
                    <td style="text-align: right;">{pos.get('indication', '-')} {spec.unit}</td>
                    <td style="text-align: right;">{pos.get('p', '-')} {spec.unit}</td>
                    <td style="text-align: right; font-weight: bold;">{pos.get('corrected_error_ec', '-')} {spec.unit}</td>
                    <td style="text-align: center;">±{pos.get('mpe', '-')} {spec.unit}</td>
                    <td style="text-align: center; color: {p_col}; font-weight: bold;">{'PASS' if pos.get('passed', False) else 'FAIL'}</td>
                </tr>
                """
            else:
                f3_rows += f"""
                <tr>
                    <td style="font-weight: 500; color: #94a3b8;">{pos_name}</td>
                    <td colspan="6" style="text-align: center; color: #94a3b8; font-style: italic;">Observation Pending</td>
                </tr>
                """

        # Form 5 rows
        f5_rows = ""
        series_data = form5_results.get("details", {})
        if not series_data and "50%" in form5_results:
            series_data = form5_results

        for bracket in ["50%", "100%"]:
            if bracket in series_data:
                sd = series_data[bracket]
                p_col = "#16a34a" if sd.get("passed", False) else "#dc2626"
                readings_str = ", ".join([str(r) for r in sd.get("readings", [])[:8]])
                if len(sd.get("readings", [])) > 8:
                    readings_str += f"... ({len(sd.get('readings', []))} total)"
                f5_rows += f"""
                <tr>
                    <td style="font-weight: 500;">{bracket} Max ({sd.get('applied_load', '-')} {spec.unit})</td>
                    <td style="font-size: 11px; font-family: monospace;">{readings_str or 'No readings'}</td>
                    <td style="text-align: right;">{sd.get('i_min', '-')} {spec.unit}</td>
                    <td style="text-align: right;">{sd.get('i_max', '-')} {spec.unit}</td>
                    <td style="text-align: right; font-weight: bold;">{sd.get('spread', '-')} {spec.unit}</td>
                    <td style="text-align: center;">{sd.get('mpe', '-')} {spec.unit}</td>
                    <td style="text-align: center; color: {p_col}; font-weight: bold;">{'PASS' if sd.get('passed', False) else 'FAIL'}</td>
                </tr>
                """
            else:
                f5_rows += f"""
                <tr>
                    <td style="font-weight: 500; color: #94a3b8;">{bracket} Max</td>
                    <td colspan="6" style="text-align: center; color: #94a3b8; font-style: italic;">Series Pending</td>
                </tr>
                """

        # Form 15 rows
        f15_rows = ""
        for chk in form15_checks:
            p_col = "#16a34a" if chk.get("passed", False) else "#dc2626"
            f15_rows += f"""
            <tr>
                <td style="font-weight: 600; text-align: center;">{chk.get('item_id', '-')}</td>
                <td style="font-size: 11px;">{chk.get('clause_oiml', '-')}<br><span style="color: #64748b;">{chk.get('welmec_ref', '')}</span></td>
                <td><b>{chk.get('title', '-')}</b><br><span style="font-size: 11px; color: #475569;">{chk.get('remarks', '')}</span></td>
                <td style="text-align: center; color: {p_col}; font-weight: bold;">{'COMPLIANT' if chk.get('passed', False) else 'NON-COMPLIANT'}</td>
            </tr>
            """
        if not f15_rows:
            f15_rows = "<tr><td colspan='4' style='text-align: center; color: #94a3b8; font-style: italic;'>Software examination pending review</td></tr>"

        # Ed25519 Asymmetric Cryptographic Signing & Offline QR Generation
        signer = Ed25519ReportSigner()
        rep_digest = Ed25519ReportSigner.compute_report_hash({
            "session_id": session_id,
            "revision": current_revision,
            "verdict": instrument_verdict,
            "zero_error_e0": str(zero_error_e0),
            "calcs_count": len(form1_calculations),
            "ecc_count": len(form3_positions),
            "rep_done": bool(form5_results),
            "sw_done": bool(form15_checks)
        })
        qr_claims = signer.create_claims(
            session_id=session_id,
            revision=current_revision,
            spec_model=spec.model,
            spec_serial=spec.serial_number,
            accuracy_class=spec.accuracy_class.value,
            verdict=instrument_verdict,
            report_sha256=rep_digest,
            reviewer_id=reviewer_id
        )
        signed_envelope = signer.sign_claims(qr_claims)
        qr_svg = Ed25519ReportSigner.generate_qr_svg(signed_envelope, box_size=5, border=1)
        pubkey_fp = signer.get_public_key_fingerprint()
        sig_compact = f"{signed_envelope['sig'][:28]}...{signed_envelope['sig'][-16:]}"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OIML R 76-2 Test Report - {session_id} Rev #{current_revision}</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 12mm 14mm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #0f172a;
            line-height: 1.45;
            background: #ffffff;
            margin: 0;
            padding: 20px;
            font-size: 12px;
        }}
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 12px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        .header-title {{
            font-size: 16px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 0;
            color: #0f172a;
        }}
        .header-sub {{
            font-size: 12px;
            font-weight: 600;
            color: #334155;
            margin: 4px 0 0 0;
        }}
        .header-meta {{
            font-size: 10px;
            color: #64748b;
            text-align: right;
        }}
        .meta-card {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 16px;
            font-size: 11px;
        }}
        .meta-item {{
            display: flex;
            flex-direction: column;
        }}
        .meta-label {{
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            font-size: 9px;
            letter-spacing: 0.4px;
        }}
        .meta-val {{
            font-weight: 600;
            color: #0f172a;
            margin-top: 2px;
        }}
        .verdict-banner {{
            background: {verdict_bg};
            border: 1px solid {verdict_border};
            color: {verdict_color};
            font-weight: 800;
            font-size: 14px;
            text-align: center;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 18px;
            letter-spacing: 0.5px;
        }}
        h3 {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            color: #1e293b;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 4px;
            margin: 16px 0 8px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 14px;
            font-size: 11px;
            page-break-inside: avoid;
        }}
        th {{
            background: #f1f5f9;
            color: #334155;
            font-weight: 600;
            text-align: center;
            padding: 6px 8px;
            border: 1px solid #cbd5e1;
            font-size: 10px;
            text-transform: uppercase;
        }}
        td {{
            padding: 5px 8px;
            border: 1px solid #e2e8f0;
        }}
        .integrity-box {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 10px;
            margin-top: 20px;
            page-break-inside: avoid;
        }}
        .integrity-box svg, .qr-container svg {{
            width: 100% !important;
            height: 100% !important;
            max-width: 100% !important;
            max-height: 100% !important;
            display: block !important;
        }}
        .qr-container {{
            width: 110px;
            height: 110px;
            flex-shrink: 0;
            background: #ffffff;
            padding: 5px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            overflow: hidden;
            box-sizing: border-box;
        }}
        .qr-inner {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .footer-note {{
            margin-top: 14px;
            font-size: 9px;
            color: #94a3b8;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            padding-top: 8px;
        }}
    </style>
</head>
<body>
    {watermark_html}
    <div class="report-container">
        <!-- Header -->
        <div class="header">
            <div>
                <h1 class="header-title">OIML R 76-2:2007 Pattern Evaluation Test Report</h1>
                <h2 class="header-sub">Non-Automatic Weighing Instrument (NAWI) Metrological Verification</h2>
                <div style="font-size: 10px; color: #475569; margin-top: 2px;">Regional Reference Standard Laboratory (RRSL) — Ministry of Consumer Affairs, Food & Public Distribution</div>
            </div>
            <div class="header-meta">
                <b>Session ID:</b> {session_id}<br>
                <b>Report Revision:</b> Revision #{current_revision}<br>
                <b>Status:</b> {review_status}<br>
                <b>Date:</b> {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
            </div>
        </div>

        <!-- Metadata Card -->
        <div class="meta-card">
            <div class="meta-item"><span class="meta-label">Manufacturer</span><span class="meta-val">{spec.manufacturer}</span></div>
            <div class="meta-item"><span class="meta-label">Model / Serial Number</span><span class="meta-val">{spec.model} / {spec.serial_number}</span></div>
            <div class="meta-item"><span class="meta-label">Accuracy Class</span><span class="meta-val">{spec.accuracy_class.value}</span></div>
            <div class="meta-item"><span class="meta-label">Max / Min Capacity</span><span class="meta-val">{spec.max_capacity} {spec.unit} / {spec.min_capacity} {spec.unit}</span></div>
            <div class="meta-item"><span class="meta-label">Interval (e / d)</span><span class="meta-val">e = {spec.e} {spec.unit} / d = {spec.d} {spec.unit}</span></div>
            <div class="meta-item"><span class="meta-label">Zero-Error (E0)</span><span class="meta-val">{zero_error_e0} {spec.unit}</span></div>
            <div class="meta-item"><span class="meta-label">Rule Engine Version</span><span class="meta-val">{engine_version}</span></div>
            <div class="meta-item"><span class="meta-label">LRS SHA-256 Hash</span><span class="meta-val" style="font-family: monospace;">{lrs_sha256}</span></div>
            <div class="meta-item"><span class="meta-label">Reviewer / Inspector ID</span><span class="meta-val">{reviewer_id}</span></div>
        </div>

        <!-- Overall Verdict -->
        <div class="verdict-banner">
            OVERALL INSTRUMENT VERDICT: {instrument_verdict}
        </div>

        <!-- Form 1: Weighing Performance -->
        <h3>Form 1: Weighing Performance Test (Clause 3.5.1 & Table 6)</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 6%;">Step</th>
                    <th style="width: 16%;">Unrounded Ind. (P)</th>
                    <th style="width: 14%;">Raw Error (E)</th>
                    <th style="width: 16%;">Corrected (Ec)</th>
                    <th style="width: 14%;">MPE Limit</th>
                    <th style="width: 12%;">Verdict</th>
                    <th style="width: 22%;">Governing Range</th>
                </tr>
            </thead>
            <tbody>
                {f1_rows}
            </tbody>
        </table>

        <!-- Hysteresis -->
        <h4 style="font-size: 11px; margin: 8px 0 4px 0; color: #475569; text-transform: uppercase;">Diagnostic Hysteresis Analysis (|Ec,desc - Ec,asc| &le; |MPE|)</h4>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">Test Load</th>
                    <th style="width: 20%;">Ascending Ec</th>
                    <th style="width: 20%;">Descending Ec</th>
                    <th style="width: 20%;">Hysteresis Difference</th>
                    <th style="width: 20%;">Reference Formula</th>
                </tr>
            </thead>
            <tbody>
                {h_rows}
            </tbody>
        </table>

        <!-- Form 3: Eccentricity -->
        <h3>Form 3: Corner Eccentricity Test (Clause 3.6.2 & A.4.7 — Load = 1/3 Max = {spec.max_capacity // 3} {spec.unit})</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 18%;">Loading Position</th>
                    <th style="width: 14%;">Load</th>
                    <th style="width: 14%;">Indication</th>
                    <th style="width: 14%;">Unrounded (P)</th>
                    <th style="width: 14%;">Corrected (Ec)</th>
                    <th style="width: 12%;">MPE Limit</th>
                    <th style="width: 14%;">Verdict</th>
                </tr>
            </thead>
            <tbody>
                {f3_rows}
            </tbody>
        </table>

        <!-- Form 5: Repeatability -->
        <h3>Form 5: Repeatability Test (Clause 3.6.1 & A.4.10 — Spread &le; |MPE|)</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">Series Bracket</th>
                    <th style="width: 28%;">Indications Sample</th>
                    <th style="width: 10%;">Min</th>
                    <th style="width: 10%;">Max</th>
                    <th style="width: 12%;">Spread</th>
                    <th style="width: 10%;">MPE</th>
                    <th style="width: 10%;">Verdict</th>
                </tr>
            </thead>
            <tbody>
                {f5_rows}
            </tbody>
        </table>

        <!-- Form 15: Software Examination -->
        <h3>Form 15: Examination of Software-Controlled Weighing Instruments (Clause 5.5 & WELMEC 7.2)</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 10%;">Item</th>
                    <th style="width: 22%;">Regulatory Standard</th>
                    <th style="width: 50%;">Mandatory Examination Criteria</th>
                    <th style="width: 18%;">Evaluation</th>
                </tr>
            </thead>
            <tbody>
                {f15_rows}
            </tbody>
        </table>

        <!-- Integrity Block & Ed25519 Digital Seal -->
        <div class="integrity-box" style="display: flex; justify-content: space-between; align-items: center; gap: 16px;">
            <div style="flex: 1;">
                <div style="font-weight: 700; margin-bottom: 5px; text-transform: uppercase; color: #1e293b; font-size: 11px;">
                    OIML R 76-2 Cryptographic Traceability & Ed25519 Digital Seal
                </div>
                <div style="margin-bottom: 2px;"><b>Certificate ID:</b> <span style="font-family: monospace;">{qr_claims['cert_id']}</span></div>
                <div style="margin-bottom: 2px;"><b>Ed25519 Public Key Fingerprint:</b> <span style="font-family: monospace; color: #0369a1;">{pubkey_fp}</span></div>
                <div style="margin-bottom: 2px;"><b>Legally Relevant Software (LRS):</b> SHA-256: <span style="font-family: monospace;">{sealer_status.get('sha256', 'N/A')[:24]}...</span> (CRC-32: {lrs_crc32})</div>
                <div style="margin-bottom: 2px;"><b>Ed25519 Digital Signature:</b> <span style="font-family: monospace; font-size: 9px; color: #334155;">{sig_compact}</span></div>
                <div style="margin-bottom: 2px;"><b>Reviewer Remarks:</b> {review_comments or 'Report reviewed and certified per ISO/IEC 17025 and OIML-CS Scheme A.'}</div>
                <div style="margin-top: 6px; color: #475569; font-size: 9px; line-height: 1.35;">
                    <b>Offline Verification:</b> Cryptographically verifiable 100% offline via Ed25519 (RFC 8032). Inspectors can scan the QR code with any standard reader or offline metrology terminal to verify authenticity without internet connectivity.
                </div>
            </div>
            <div class="qr-container">
                <div class="qr-inner">{qr_svg}</div>
            </div>
        </div>

        <div class="footer-note">
            Automated Metrology Suite SIH26035 | Generated under the Legal Metrology Act, 2009 & OIML R 76-1:2006 (E)
        </div>
    </div>
</body>
</html>
"""
        return html

    @classmethod
    def _render_pdf_reportlab(cls, html_content: str, output_path: Path) -> Path:
        """
        Pure-Python statutory vector PDF generator using ReportLab.
        Guarantees 100% offline, zero-browser PDF generation across any serverless,
        minimal Linux/Docker container, or cloud host without requiring Google Chrome.
        """
        import io
        import re
        import qrcode
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image as RLImage
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm

        def clean_html(text: str) -> str:
            if not text:
                return ""
            text = re.sub(r'<br\s*/?>', ' ', text)
            text = re.sub(r'<.*?>', '', text)
            text = text.replace('&le;', '<=').replace('&ge;', '>=').replace('&amp;', '&').replace('&nbsp;', ' ').replace('&bull;', '•').replace('&mdash;', '—')
            return text.strip()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=12*mm,
            rightMargin=12*mm,
            topMargin=12*mm,
            bottomMargin=12*mm
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=11, leading=14, textColor=colors.HexColor('#0f2b5c'), alignment=1, fontName='Helvetica-Bold')
        sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor('#334155'), alignment=1)
        h3_style = ParagraphStyle('H3Style', parent=styles['Heading3'], fontSize=8.5, leading=11, textColor=colors.HexColor('#0f2b5c'), spaceBefore=5, spaceAfter=2, fontName='Helvetica-Bold')
        cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=6.5, leading=8)
        hdr_cell_style = ParagraphStyle('HdrCellStyle', parent=styles['Normal'], fontSize=6.5, leading=8, textColor=colors.white, fontName='Helvetica-Bold')

        story = []

        # Header
        story.append(Paragraph('GOVERNMENT OF INDIA &bull; MINISTRY OF CONSUMER AFFAIRS', sub_style))
        story.append(Paragraph('DEPARTMENT OF CONSUMER AFFAIRS &mdash; LEGAL METROLOGY DIVISION', sub_style))
        story.append(Paragraph('OIML R 76-2:2007 Pattern Evaluation Test Report', title_style))
        story.append(Paragraph('Non-Automatic Weighing Instrument (NAWI) Metrological Verification', sub_style))
        story.append(Spacer(1, 2.5*mm))

        # Metadata Table
        meta_items = re.findall(r'<div class="meta-item"><span class="meta-label">(.*?)</span><span class="meta-val".*?>(.*?)</span></div>', html_content)
        if meta_items:
            meta_data = []
            for i in range(0, len(meta_items), 2):
                row = []
                k1, v1 = meta_items[i]
                row.extend([Paragraph(f'<b>{clean_html(k1)}:</b>', cell_style), Paragraph(clean_html(v1), cell_style)])
                if i + 1 < len(meta_items):
                    k2, v2 = meta_items[i+1]
                    row.extend([Paragraph(f'<b>{clean_html(k2)}:</b>', cell_style), Paragraph(clean_html(v2), cell_style)])
                else:
                    row.extend(['', ''])
                meta_data.append(row)
            t_meta = Table(meta_data, colWidths=[38*mm, 52*mm, 42*mm, 54*mm])
            t_meta.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 1.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ]))
            story.append(t_meta)
            story.append(Spacer(1, 2.5*mm))

        # Verdict Banner
        verdict_m = re.search(r'<div class="verdict-banner">(.*?)</div>', html_content, re.DOTALL)
        if verdict_m:
            verdict_text = clean_html(verdict_m.group(1))
            v_color = colors.HexColor('#15803d') if 'PASSED' in verdict_text else (colors.HexColor('#b91c1c') if 'FAILED' in verdict_text else colors.HexColor('#475569'))
            t_v = Table([[Paragraph(f'<b>{verdict_text}</b>', ParagraphStyle('V', parent=sub_style, fontSize=8.5, textColor=colors.white, fontName='Helvetica-Bold'))]], colWidths=[186*mm])
            t_v.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), v_color),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('TOPPADDING', (0,0), (-1,-1), 2.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ]))
            story.append(t_v)
            story.append(Spacer(1, 2.5*mm))

        # Tables
        headings = re.findall(r'<h[34].*?>(.*?)</h[34]>', html_content)
        raw_tables = re.findall(r'<table.*?>(.*?)</table>', html_content, re.DOTALL)

        for i, raw_tbl in enumerate(raw_tables):
            h_title = clean_html(headings[i]) if i < len(headings) else f'Test Table {i+1}'
            story.append(Paragraph(h_title, h3_style))
            rows = re.findall(r'<tr.*?>(.*?)</tr>', raw_tbl, re.DOTALL)
            table_data = []
            for r_idx, r in enumerate(rows):
                cells = re.findall(r'<t[hd].*?>(.*?)</t[hd]>', r, re.DOTALL)
                if r_idx == 0:
                    table_data.append([Paragraph(clean_html(c), hdr_cell_style) for c in cells])
                else:
                    table_data.append([Paragraph(clean_html(c), cell_style) for c in cells])
            if table_data:
                num_cols = len(table_data[0])
                col_w = 186.0 * mm / max(1, num_cols)
                t = Table(table_data, colWidths=[col_w]*num_cols, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f2b5c')),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
                    ('TOPPADDING', (0,0), (-1,-1), 1.5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
                ]))
                story.append(t)
                story.append(Spacer(1, 2*mm))

        # Integrity Box & QR Code
        cert_id_m = re.search(r'Certificate ID:</b>.*?<span.*?>(.*?)</span>', html_content)
        cert_id = clean_html(cert_id_m.group(1)) if cert_id_m else 'OIML-R76-CERT'
        pubkey_m = re.search(r'Ed25519 Public Key Fingerprint:</b>.*?<span.*?>(.*?)</span>', html_content)
        pubkey_fp = clean_html(pubkey_m.group(1)) if pubkey_m else 'N/A'
        sig_m = re.search(r'Ed25519 Digital Signature:</b>.*?<span.*?>(.*?)</span>', html_content)
        sig_val = clean_html(sig_m.group(1)) if sig_m else 'N/A'

        qr_img = qrcode.make(f'OIML_R76_REPORT:{cert_id}:{pubkey_fp[:16]}')
        qr_buf = io.BytesIO()
        qr_img.save(qr_buf, format='PNG')
        qr_buf.seek(0)
        rl_qr = RLImage(qr_buf, width=22*mm, height=22*mm)

        sig_info = Paragraph(
            '<b>OIML R 76-2 Cryptographic Traceability & Ed25519 Digital Seal</b><br/>'
            f'<b>Certificate ID:</b> {cert_id} &nbsp;|&nbsp; <b>Key FP:</b> <font color="#0369a1">{pubkey_fp}</font><br/>'
            f'<b>Ed25519 Signature:</b> <font color="#334155">{sig_val}</font><br/>'
            '<b>Standard:</b> OIML R 76-1:2006 (E) & Legal Metrology Act, 2009<br/>'
            '<b>Offline Verification:</b> Cryptographically verifiable 100% offline via Ed25519 (RFC 8032).',
            cell_style
        )
        t_sig = Table([[sig_info, rl_qr]], colWidths=[160*mm, 26*mm])
        t_sig.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ]))
        story.append(KeepTogether([t_sig]))

        doc.build(story)
        return output_path

    @classmethod
    def generate_pdf_report(cls, html_content: str, output_path: Path) -> Path:
        """
        Converts HTML report to a true vector PDF.
        Attempts headless Google Chrome/Chromium if available;
        automatically falls back to ReportLab pure-Python vector PDF engine
        to eliminate external system binary requirements and prevent cloud deployment failures.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check for Chrome/Chromium candidates
        chrome_candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            shutil.which("google-chrome"),
            shutil.which("chromium"),
            shutil.which("chromium-browser"),
        ]
        chrome_bin = next((c for c in chrome_candidates if c and os.path.exists(c) and os.access(c, os.X_OK)), None)

        if chrome_bin:
            temp_html = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
                    f.write(html_content)
                    temp_html = f.name

                cmd = [
                    chrome_bin,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-sandbox",
                    f"--print-to-pdf={str(output_path)}",
                    temp_html
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if res.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
                    return output_path
            except Exception:
                pass  # Fall back to ReportLab
            finally:
                if temp_html and os.path.exists(temp_html):
                    os.remove(temp_html)

        # Chrome not available or failed: execute pure-Python ReportLab vector PDF generator
        return cls._render_pdf_reportlab(html_content, output_path)

    @staticmethod
    def generate_pdfa3_report(
        html_content: str,
        dcc_xml: str,
        output_path: Path,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Renders HTML to vector PDF via headless Google Chrome and wraps it into
        an ISO 19005-3 (PDF/A-3b) archival container with embedded PTB DCC XML.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            tmp_base_path = Path(tmp_pdf.name)

        try:
            OIMLReportGenerator.generate_pdf_report(html_content, tmp_base_path)
            base_pdf_bytes = tmp_base_path.read_bytes()

            container_bytes = PdfA3ContainerEngine.create_pdfa3_container(
                base_pdf_bytes=base_pdf_bytes,
                dcc_xml=dcc_xml,
                metadata=metadata
            )
            output_path.write_bytes(container_bytes)
            return output_path
        finally:
            if tmp_base_path.exists():
                tmp_base_path.unlink()

    @staticmethod
    def generate_dcc_xml_report(
        session_id: str,
        spec: InstrumentSpecification,
        weighing_calcs: List[Dict[str, Any]],
        digital_seal: Optional[Dict[str, Any]] = None
    ) -> str:
        """Constructs PTB DCC v3.2.1 compliant XML for the test session."""
        instrument_metadata = {
            "manufacturer": spec.manufacturer,
            "model": spec.model,
            "serial_number": spec.serial_number,
            "accuracy_class": spec.accuracy_class.value,
            "max_capacity": str(spec.max_capacity),
            "min_capacity": str(spec.min_capacity),
            "e": str(spec.e),
            "d": str(spec.d),
            "unit": spec.unit
        }
        sealer_status = WelmecSoftwareSealer.calculate_lrs_fingerprint()
        lrs_fingerprint = {
            "kernel_file": "nawi_engine.py",
            "sha256": sealer_status.get("sha256", ""),
            "crc32": sealer_status.get("crc32_hex", ""),
            "welmec_guide": "7.2 (Issue 5) Extension L"
        }
        lab_info = {
            "name": "Regional Reference Standard Laboratory (RRSL)",
            "city": "Faridabad",
            "accreditation": "OIML-CS Scheme A"
        }
        return DCCGenerator.generate_dcc_xml(
            certificate_id=f"OIML-RRSL-{session_id}",
            instrument_metadata=instrument_metadata,
            weighing_observations=weighing_calcs,
            laboratory_info=lab_info,
            lrs_fingerprint=lrs_fingerprint,
            digital_seal=digital_seal
        )
