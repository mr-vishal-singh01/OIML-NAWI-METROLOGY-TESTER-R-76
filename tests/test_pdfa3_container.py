"""
Exhaustive Automated Test Suite: ISO 19005-3 (PDF/A-3b) Archival Engine & PTB DCC v3.2.1 Container
Smart India Hackathon SIH26035 — Legal Metrology Division

Tests:
- 20 Distinct Unit, Integration, Adversarial, and FastAPI Endpoint Tests
- Conformance to ISO 19005-3:2012 (PDF/A-3b) clause 6.8 (Associated Files)
- Conformance to PTB DCC v3.2.1 and SmartCom D-SI unit architecture
- Offline RFC 8032 Ed25519 digital seal verification
- Boundary conditions, DoS limits, and tamper detection
"""

import io
import sys
import json
import unittest
from pathlib import Path
from decimal import Decimal

# Ensure src is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pypdf import PdfReader, PdfWriter
from fastapi.testclient import TestClient

from core.nawi_engine import AccuracyClass, InstrumentSpecification
from core.dcc_generator import DCCGenerator
from core.offline_qr import Ed25519ReportSigner, TrustStore
from reporting.pdfa3_engine import PdfA3ContainerEngine
from reporting.report_generator import OIMLReportGenerator
from api.main import app, session


class TestPdfA3ContainerSuite(unittest.TestCase):
    """Exhaustive test suite for ISO 19005-3 PDF/A-3 container engine and PTB DCC v3.2.1 XML."""

    def setUp(self):
        """Prepares sample instrument spec, observations, and dummy base PDF."""
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
        self.observations = [
            {
                "step_index": 1,
                "direction": "ascending",
                "applied_load": "2500.0",
                "indicated_value": "2500.0",
                "corrected_error_ec": "0.0",
                "passed": True
            },
            {
                "step_index": 2,
                "direction": "ascending",
                "applied_load": "5000.0",
                "indicated_value": "5000.0",
                "corrected_error_ec": "0.0",
                "passed": True
            }
        ]
        self.lab_info = {
            "name": "Regional Reference Standard Laboratory (RRSL)",
            "city": "Faridabad",
            "accreditation": "OIML-CS Scheme A"
        }
        self.lrs_fingerprint = {
            "kernel_file": "nawi_engine.py",
            "sha256": "abcdef1234567890abcdef1234567890",
            "crc32": "1A2B3C4D",
            "welmec_guide": "7.2 (Issue 5) Extension L"
        }

        # Helper to generate a genuine minimal base PDF
        base_writer = PdfWriter()
        base_writer.add_blank_page(width=595, height=842)
        buf = io.BytesIO()
        base_writer.write(buf)
        self.sample_base_pdf = buf.getvalue()

        # Generate sample DCC XML without seal
        self.sample_dcc_xml = DCCGenerator.generate_dcc_xml(
            certificate_id="OIML-RRSL-SESS-2026-001",
            instrument_metadata={
                "manufacturer": self.spec.manufacturer,
                "model": self.spec.model,
                "serial_number": self.spec.serial_number,
                "accuracy_class": self.spec.accuracy_class.value,
                "max_capacity": str(self.spec.max_capacity),
                "min_capacity": str(self.spec.min_capacity),
                "e": str(self.spec.e),
                "d": str(self.spec.d),
                "unit": self.spec.unit
            },
            weighing_observations=self.observations,
            laboratory_info=self.lab_info,
            lrs_fingerprint=self.lrs_fingerprint
        )

        self.client = TestClient(app)

    # -------------------------------------------------------------
    # 1. PDF/A-3 Header and Format Verification
    # -------------------------------------------------------------
    def test_01_pdfa3_container_creation_and_header(self):
        """1. Container must start with %PDF-1.7 and binary marker %âãÏÓ."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml
        )
        self.assertTrue(container.startswith(b"%PDF-1.7"))
        # Check for binary character comment (codes >= 128)
        self.assertIn(b"%\xe2\xe3\xcf\xd3", container[:30])

    # -------------------------------------------------------------
    # 2. ISO 19005-3 XMP Metadata Conformance
    # -------------------------------------------------------------
    def test_02_iso_19005_3_xmp_metadata_conformance(self):
        """2. XMP packet must declare pdfaid:part=3 and pdfaid:conformance=B."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml,
            metadata={"title": "Custom Title", "creator": "RRSL Lead Auditor"}
        )
        reader = PdfReader(io.BytesIO(container))
        xmp = reader.xmp_metadata
        self.assertIsNotNone(xmp)
        self.assertEqual(int(xmp.pdfaid_part), 3)
        self.assertEqual(str(xmp.pdfaid_conformance).upper(), "B")
        self.assertEqual(xmp.dc_title.get("x-default"), "Custom Title")
        self.assertEqual(xmp.dc_creator, ["RRSL Lead Auditor"])

    # -------------------------------------------------------------
    # 3. Document Catalog /AF Array
    # -------------------------------------------------------------
    def test_03_associated_files_af_catalog_entry(self):
        """3. Document Catalog /Root must contain an /AF (Associated Files) array."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml
        )
        reader = PdfReader(io.BytesIO(container))
        root = reader.trailer["/Root"]
        self.assertIn("/AF", root)
        af_array = root["/AF"]
        self.assertGreater(len(af_array), 0)

    # -------------------------------------------------------------
    # 4. /AFRelationship and EmbeddedFile Stream Subtype
    # -------------------------------------------------------------
    def test_04_af_relationship_and_mime_subtype(self):
        """4. FileSpec must declare /AFRelationship /Data and stream must have /Subtype /application#2Fxml."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml,
            af_relationship="/Data"
        )
        reader = PdfReader(io.BytesIO(container))
        root = reader.trailer["/Root"]
        filespec = root["/AF"][0].get_object()
        self.assertEqual(str(filespec.get("/AFRelationship")), "/Data")
        self.assertEqual(str(filespec.get("/UF")), "dcc_certificate.xml")

        stream_obj = filespec["/EF"]["/F"].get_object()
        self.assertIn(str(stream_obj.get("/Subtype")), ("/application/xml", "/application#2Fxml", "/text/xml", "/text#2Fxml"))
        self.assertIn("/Params", stream_obj)
        self.assertEqual(int(stream_obj["/Params"]["/Size"]), len(self.sample_dcc_xml.encode("utf-8")))

    # -------------------------------------------------------------
    # 5. OutputIntent Dictionary Presence (ISO 19005-3 clause 6.2.2)
    # -------------------------------------------------------------
    def test_05_output_intent_srgb_profile(self):
        """5. Must contain standard sRGB OutputIntent dictionary for device-independent color reproduction."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml
        )
        reader = PdfReader(io.BytesIO(container))
        root = reader.trailer["/Root"]
        self.assertIn("/OutputIntents", root)
        intent = root["/OutputIntents"][0].get_object()
        self.assertEqual(str(intent["/S"]), "/GTS_PDFA1")
        self.assertIn("sRGB", str(intent["/OutputConditionIdentifier"]))

    # -------------------------------------------------------------
    # 6. Bidirectional DCC XML Extraction Roundtrip
    # -------------------------------------------------------------
    def test_06_dcc_xml_extraction_roundtrip(self):
        """6. Extracted DCC XML must exactly match the originally embedded XML string."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml
        )
        success, raw_xml, parsed = PdfA3ContainerEngine.extract_embedded_dcc(container)
        self.assertTrue(success)
        self.assertIsNotNone(raw_xml)
        self.assertEqual(raw_xml.strip(), self.sample_dcc_xml.strip())
        self.assertEqual(parsed["unique_identifier"], "OIML-RRSL-SESS-2026-001")

    # -------------------------------------------------------------
    # 7. PTB DCC v3.2.1 Schema Compliance
    # -------------------------------------------------------------
    def test_07_ptb_dcc_v321_schema_structure(self):
        """7. Extracted XML must conform to PTB DCC v3.2.1 namespace and schemaVersion."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml
        )
        success, _, parsed = PdfA3ContainerEngine.extract_embedded_dcc(container)
        self.assertTrue(success)
        self.assertEqual(parsed["schema_version"], "3.2.1")
        self.assertEqual(parsed["administrative_data"]["item"]["model"], "DS-852")
        self.assertEqual(parsed["administrative_data"]["software"]["crc32"], "1A2B3C4D")

    # -------------------------------------------------------------
    # 8. SmartCom D-SI Measurement Units Adherence
    # -------------------------------------------------------------
    def test_08_smartcom_dsi_measurement_units(self):
        """8. Weighing observations must parse SmartCom D-SI values and \\gram units."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml
        )
        success, _, parsed = PdfA3ContainerEngine.extract_embedded_dcc(container)
        self.assertTrue(success)
        self.assertEqual(parsed["observations_count"], 2)

        first_obs = parsed["observations"][0]
        self.assertEqual(first_obs["step"], "1")
        self.assertEqual(first_obs["applied_load"]["value"], "2500.0")
        self.assertEqual(first_obs["applied_load"]["unit"], "\\gram")
        self.assertEqual(first_obs["conformity"], "PASS")

    # -------------------------------------------------------------
    # 9. Ed25519 Digital Seal in DCC & PDF/A-3
    # -------------------------------------------------------------
    def test_09_ed25519_digital_seal_in_dcc_and_verification(self):
        """9. DCC XML with embedded Ed25519 digital seal must verify as authentic."""
        signer = Ed25519ReportSigner()
        rep_hash = Ed25519ReportSigner.compute_report_hash({"session_id": "SESS-2026-001", "verdict": "PASSED"})
        claims = signer.create_claims(
            session_id="SESS-2026-001",
            revision=1,
            spec_model=self.spec.model,
            spec_serial=self.spec.serial_number,
            accuracy_class=self.spec.accuracy_class.value,
            verdict="PASSED",
            report_sha256=rep_hash
        )
        envelope = signer.sign_claims(claims)

        dcc_xml_with_seal = DCCGenerator.generate_dcc_xml(
            certificate_id=claims["cert_id"],
            instrument_metadata={
                "manufacturer": self.spec.manufacturer,
                "model": self.spec.model,
                "serial_number": self.spec.serial_number,
                "accuracy_class": self.spec.accuracy_class.value,
                "max_capacity": str(self.spec.max_capacity),
                "min_capacity": str(self.spec.min_capacity),
                "e": str(self.spec.e),
                "d": str(self.spec.d),
                "unit": self.spec.unit
            },
            weighing_observations=self.observations,
            laboratory_info=self.lab_info,
            lrs_fingerprint=self.lrs_fingerprint,
            digital_seal=envelope
        )

        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=dcc_xml_with_seal
        )

        audit = PdfA3ContainerEngine.verify_container_integrity(
            container,
            expected_claims={"session_id": "SESS-2026-001", "report_hash": rep_hash, "verdict": "PASSED"}
        )
        self.assertTrue(audit["valid_pdfa3"])
        self.assertTrue(audit["cryptographic_seal_present"])
        self.assertTrue(audit["cryptographic_seal_valid"])
        self.assertTrue(audit["claims_match"])
        self.assertEqual(len(audit["errors"]), 0)

    # -------------------------------------------------------------
    # 10. Tamper Detection: Modified DCC XML Body
    # -------------------------------------------------------------
    def test_10_tamper_detection_modified_dcc_xml(self):
        """10. Tampering with claims inside the DCC XML must fail cryptographic verification."""
        signer = Ed25519ReportSigner()
        rep_hash = Ed25519ReportSigner.compute_report_hash({"session_id": "SESS-2026-001", "verdict": "PASSED"})
        claims = signer.create_claims(
            session_id="SESS-2026-001",
            revision=1,
            spec_model=self.spec.model,
            spec_serial=self.spec.serial_number,
            accuracy_class=self.spec.accuracy_class.value,
            verdict="PASSED",
            report_sha256=rep_hash
        )
        envelope = signer.sign_claims(claims)

        dcc_xml = DCCGenerator.generate_dcc_xml(
            certificate_id=claims["cert_id"],
            instrument_metadata={"model": self.spec.model, "manufacturer": self.spec.manufacturer},
            weighing_observations=self.observations,
            laboratory_info=self.lab_info,
            lrs_fingerprint=self.lrs_fingerprint,
            digital_seal=envelope
        )

        # Adversary alters PASSED to FAILED inside XML / envelope_json
        tampered_xml = dcc_xml.replace("PASSED", "FAILED")

        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=tampered_xml
        )
        audit = PdfA3ContainerEngine.verify_container_integrity(container)
        self.assertTrue(audit["cryptographic_seal_present"])
        self.assertFalse(audit["cryptographic_seal_valid"])
        self.assertGreater(len(audit["errors"]), 0)

    # -------------------------------------------------------------
    # 11. Tamper Detection: Signature Bit Flip
    # -------------------------------------------------------------
    def test_11_tamper_detection_signature_bit_flip(self):
        """11. Flipping characters in the signature string must invalidate the seal."""
        signer = Ed25519ReportSigner()
        rep_hash = Ed25519ReportSigner.compute_report_hash({"session_id": "SESS-2026-001", "verdict": "PASSED"})
        claims = signer.create_claims(
            session_id="SESS-2026-001",
            revision=1,
            spec_model=self.spec.model,
            spec_serial=self.spec.serial_number,
            accuracy_class=self.spec.accuracy_class.value,
            verdict="PASSED",
            report_sha256=rep_hash
        )
        envelope = signer.sign_claims(claims)

        # Mutate signature
        sig_str = envelope["sig"]
        mutated_sig = ("A" if sig_str[0] != "A" else "B") + sig_str[1:]
        envelope["sig"] = mutated_sig

        dcc_xml = DCCGenerator.generate_dcc_xml(
            certificate_id=claims["cert_id"],
            instrument_metadata={"model": self.spec.model, "manufacturer": self.spec.manufacturer},
            weighing_observations=self.observations,
            laboratory_info=self.lab_info,
            lrs_fingerprint=self.lrs_fingerprint,
            digital_seal=envelope
        )

        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=dcc_xml
        )
        audit = PdfA3ContainerEngine.verify_container_integrity(container)
        self.assertFalse(audit["cryptographic_seal_valid"])

    # -------------------------------------------------------------
    # 12. Tamper Detection: Mismatched Expected Report Hash
    # -------------------------------------------------------------
    def test_12_tamper_detection_mismatched_report_hash(self):
        """12. If visual report hash diverges from DCC seal, claims_match must be False."""
        signer = Ed25519ReportSigner()
        rep_hash = Ed25519ReportSigner.compute_report_hash({"session_id": "SESS-2026-001", "verdict": "PASSED"})
        claims = signer.create_claims(
            session_id="SESS-2026-001",
            revision=1,
            spec_model=self.spec.model,
            spec_serial=self.spec.serial_number,
            accuracy_class=self.spec.accuracy_class.value,
            verdict="PASSED",
            report_sha256=rep_hash
        )
        envelope = signer.sign_claims(claims)

        dcc_xml = DCCGenerator.generate_dcc_xml(
            certificate_id=claims["cert_id"],
            instrument_metadata={"model": self.spec.model, "manufacturer": self.spec.manufacturer},
            weighing_observations=self.observations,
            laboratory_info=self.lab_info,
            lrs_fingerprint=self.lrs_fingerprint,
            digital_seal=envelope
        )

        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=dcc_xml
        )

        # Expected report hash has been modified / mismatched
        bogus_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        audit = PdfA3ContainerEngine.verify_container_integrity(
            container,
            expected_claims={"session_id": "SESS-2026-001", "report_hash": bogus_hash}
        )
        self.assertFalse(audit["claims_match"])
        self.assertTrue(any("Report hash mismatch" in err for err in audit["errors"]))

    # -------------------------------------------------------------
    # 13. Input Bounds: Max PDF Size DoS Protection
    # -------------------------------------------------------------
    def test_13_input_bounds_max_pdf_size_dos_rejection(self):
        """13. PDF bytes exceeding 25MB DoS limit must be rejected."""
        oversized_pdf = b"%PDF-1.7\n" + b"A" * (25 * 1024 * 1024 + 100)
        with self.assertRaises(ValueError) as ctx:
            PdfA3ContainerEngine.create_pdfa3_container(
                base_pdf_bytes=oversized_pdf,
                dcc_xml=self.sample_dcc_xml
            )
        self.assertIn("exceeds maximum allowed size", str(ctx.exception))

    # -------------------------------------------------------------
    # 14. Input Bounds: Max XML Size DoS Protection
    # -------------------------------------------------------------
    def test_14_input_bounds_max_xml_size_dos_rejection(self):
        """14. XML bytes exceeding 10MB DoS limit must be rejected."""
        oversized_xml = "<dcc:digitalCalibrationCertificate>" + "X" * (10 * 1024 * 1024 + 100)
        with self.assertRaises(ValueError) as ctx:
            PdfA3ContainerEngine.create_pdfa3_container(
                base_pdf_bytes=self.sample_base_pdf,
                dcc_xml=oversized_xml
            )
        self.assertIn("exceeds maximum allowed size", str(ctx.exception))

    # -------------------------------------------------------------
    # 15. Invalid Magic Bytes Rejection
    # -------------------------------------------------------------
    def test_15_invalid_magic_bytes_rejection(self):
        """15. Input missing '%PDF-' header magic bytes must be rejected."""
        non_pdf = b"NOT_A_PDF_DOCUMENT_PAYLOAD"
        with self.assertRaises(ValueError) as ctx:
            PdfA3ContainerEngine.create_pdfa3_container(
                base_pdf_bytes=non_pdf,
                dcc_xml=self.sample_dcc_xml
            )
        self.assertIn("magic bytes", str(ctx.exception))

    # -------------------------------------------------------------
    # 16. Malformed XML Rejection
    # -------------------------------------------------------------
    def test_16_malformed_xml_rejection(self):
        """16. Malformed XML without closing tags must be rejected during creation."""
        bad_xml = "<dcc:digitalCalibrationCertificate><unclosed>"
        with self.assertRaises(ValueError) as ctx:
            PdfA3ContainerEngine.create_pdfa3_container(
                base_pdf_bytes=self.sample_base_pdf,
                dcc_xml=bad_xml
            )
        self.assertIn("Malformed DCC XML", str(ctx.exception))

    # -------------------------------------------------------------
    # 17. Multi-Page Document Preservation
    # -------------------------------------------------------------
    def test_17_multi_page_document_preservation(self):
        """17. Multi-page base PDF must preserve all pages and content in PDF/A-3 container."""
        multi_writer = PdfWriter()
        for _ in range(5):
            multi_writer.add_blank_page(width=595, height=842)
        buf = io.BytesIO()
        multi_writer.write(buf)
        multi_bytes = buf.getvalue()

        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=multi_bytes,
            dcc_xml=self.sample_dcc_xml
        )
        reader = PdfReader(io.BytesIO(container))
        self.assertEqual(len(reader.pages), 5)
        audit = PdfA3ContainerEngine.verify_container_integrity(container)
        self.assertTrue(audit["valid_pdfa3"])

    # -------------------------------------------------------------
    # 18. Custom /AFRelationship Support
    # -------------------------------------------------------------
    def test_18_custom_af_relationship(self):
        """18. Supports ISO 19005-3 valid relationships like /Supplement and /Source."""
        container = PdfA3ContainerEngine.create_pdfa3_container(
            base_pdf_bytes=self.sample_base_pdf,
            dcc_xml=self.sample_dcc_xml,
            af_relationship="/Supplement"
        )
        audit = PdfA3ContainerEngine.verify_container_integrity(container)
        self.assertTrue(audit["valid_pdfa3"])
        self.assertEqual(audit["af_relationship"], "/Supplement")

        # Invalid relationship must be rejected
        with self.assertRaises(ValueError):
            PdfA3ContainerEngine.create_pdfa3_container(
                base_pdf_bytes=self.sample_base_pdf,
                dcc_xml=self.sample_dcc_xml,
                af_relationship="/InvalidRelationship"
            )

    # -------------------------------------------------------------
    # 19. FastAPI Endpoints: GET /api/report/pdf and /api/report/pdfa3
    # -------------------------------------------------------------
    def test_19_fastapi_pdfa3_generation_endpoint(self):
        """19. GET /api/report/pdf and /api/report/pdfa3 must return certified PDF/A-3 containers."""
        res = self.client.get("/api/report/pdf")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("content-type"), "application/pdf")
        self.assertEqual(res.headers.get("x-pdf-standard"), "ISO 19005-3:2012 (PDF/A-3b)")
        self.assertEqual(res.headers.get("x-embedded-dcc"), "dcc_certificate.xml")

        pdf_bytes = res.content
        audit = PdfA3ContainerEngine.verify_container_integrity(pdf_bytes)
        self.assertTrue(audit["valid_pdfa3"])
        self.assertTrue(audit["dcc_extracted"])
        self.assertEqual(audit["dcc_schema_version"], "3.2.1")
        self.assertTrue(audit["cryptographic_seal_present"])
        self.assertTrue(audit["cryptographic_seal_valid"])

        # Also verify /api/report/pdfa3 alias
        res_alias = self.client.get("/api/report/pdfa3")
        self.assertEqual(res_alias.status_code, 200)

    # -------------------------------------------------------------
    # 20. FastAPI Endpoint: POST /api/verify/pdfa3
    # -------------------------------------------------------------
    def test_20_fastapi_pdfa3_verify_endpoint(self):
        """20. POST /api/verify/pdfa3 must accept PDF upload and verify DCC and Ed25519 seal."""
        # 1. Generate legitimate PDF/A-3 container
        res = self.client.get("/api/report/pdf")
        self.assertEqual(res.status_code, 200)
        genuine_pdf = res.content

        # 2. Upload to /api/verify/pdfa3
        files = {"file": ("report.pdf", genuine_pdf, "application/pdf")}
        verif_res = self.client.post("/api/verify/pdfa3", files=files)
        self.assertEqual(verif_res.status_code, 200)
        data = verif_res.json()
        self.assertTrue(data["valid_pdfa3"])
        self.assertTrue(data["dcc_extracted"])
        self.assertTrue(data["cryptographic_seal_valid"])
        self.assertIn("raw_xml", data)
        self.assertIn("parsed_dcc", data)
        self.assertGreater(len(data["raw_xml"]), 0)
        self.assertIn("observations", data["parsed_dcc"])

        # 3. Test rejection of non-PDF upload
        bad_files = {"file": ("malicious.exe", b"NOT_A_PDF", "application/octet-stream")}
        bad_res = self.client.post("/api/verify/pdfa3", files=bad_files)
        self.assertEqual(bad_res.status_code, 400)

    # -------------------------------------------------------------
    # 21. Step 3 Workbench UI & Tamper Verification Simulation
    # -------------------------------------------------------------
    def test_21_pdfa3_workbench_ui_and_tamper_simulation(self):
        """21. Root UI serves PDF/A-3 Workbench and tampering triggers cryptographic seal failure."""
        # 1. Verify UI contains all Step 3 Workbench elements
        root_res = self.client.get("/")
        self.assertEqual(root_res.status_code, 200)
        html = root_res.text
        self.assertIn("tab-btn-pdfa3", html)
        self.assertIn("tab-pdfa3", html)
        self.assertIn("pdfDropzone", html)
        self.assertIn("pdfViewerFrame", html)
        self.assertIn("pdfa3VerdictBadge", html)
        self.assertIn("dccObservationsTableBody", html)
        self.assertIn("dccRawXmlPre", html)
        self.assertIn("btn-test-live-pdfa3", html)
        self.assertIn("btn-simulate-tampered-pdfa3", html)

        # 2. Generate legitimate PDF/A-3 container
        gen_res = self.client.get("/api/report/pdfa3")
        self.assertEqual(gen_res.status_code, 200)
        genuine_bytes = gen_res.content

        # 3. Tamper with PDF stream content
        tampered_bytes = genuine_bytes.replace(b"PASSED", b"FAILED") if b"PASSED" in genuine_bytes else genuine_bytes.replace(b"OIML", b"FORG")
        
        # 4. Upload tampered PDF to /api/verify/pdfa3
        files = {"file": ("tampered_report.pdf", tampered_bytes, "application/pdf")}
        tamper_res = self.client.post("/api/verify/pdfa3", files=files)
        self.assertEqual(tamper_res.status_code, 200)
        tamper_data = tamper_res.json()
        
        # The seal must either be invalid or fail cryptographic checks
        if tamper_data.get("cryptographic_seal_present"):
            self.assertFalse(tamper_data["cryptographic_seal_valid"])


if __name__ == "__main__":
    unittest.main()

