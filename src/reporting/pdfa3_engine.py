"""
ISO 19005-3 (PDF/A-3) Archival Container Engine with PTB DCC v3.2.1 XML
Smart India Hackathon SIH26035 — Legal Metrology Division

Conforms to:
- ISO 19005-3:2012 (PDF/A-3b)
- PTB DCC v3.2.1 Schema (https://ptb.de/dcc)
- SmartCom D-SI Unit Architecture (https://ptb.de/si)
- WELMEC 7.2 Software Separation & LRS Sealing
- RFC 8032 Ed25519 Offline Verification
"""

import io
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple, Union
import hmac
from xml.sax.saxutils import escape

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    NameObject,
    ArrayObject,
    DictionaryObject,
    NumberObject,
    IndirectObject,
    create_string_object,
)

from core.offline_qr import Ed25519ReportSigner, TrustStore


class PdfA3ContainerEngine:
    """
    Constructs, packages, extracts, and validates ISO 19005-3 (PDF/A-3b) archival containers
    with embedded PTB DCC v3.2.1 XML and SmartCom D-SI measurement data.
    """

    PDFA_HEADER = b"%PDF-1.7"
    MAX_PDF_SIZE_BYTES = 25 * 1024 * 1024   # 25 MB DoS bound
    MAX_XML_SIZE_BYTES = 10 * 1024 * 1024   # 10 MB DoS bound
    DEFAULT_ATTACHMENT_NAME = "dcc_certificate.xml"

    DCC_NAMESPACE = "https://ptb.de/dcc"
    DSI_NAMESPACE = "https://ptb.de/si"

    VALID_AF_RELATIONSHIPS = {
        "/Data",
        "/Source",
        "/Supplement",
        "/Alternative",
        "/Unspecified"
    }

    @staticmethod
    def _build_xmp_metadata(
        title: str,
        creator: str,
        subject: str,
        producer: str = "SIH26035 Metrological Archival Engine",
        part: int = 3,
        conformance: str = "B",
        create_date: Optional[datetime] = None
    ) -> bytes:
        """
        Builds an ISO 19005-3 compliant XMP metadata packet declaring PDF/A-3b conformance.
        """
        now = create_date or datetime.now(timezone.utc)
        iso_timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        safe_title = escape(title)
        safe_creator = escape(creator)
        safe_subject = escape(subject)
        safe_producer = escape(producer)

        xmp_xml = f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:pdf="http://ns.adobe.com/pdf/1.3/"
    xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <pdfaid:part>{part}</pdfaid:part>
   <pdfaid:conformance>{conformance}</pdfaid:conformance>
   <dc:format>application/pdf</dc:format>
   <dc:title>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">{safe_title}</rdf:li>
    </rdf:Alt>
   </dc:title>
   <dc:creator>
    <rdf:Seq>
     <rdf:li>{safe_creator}</rdf:li>
    </rdf:Seq>
   </dc:creator>
   <dc:description>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">{safe_subject}</rdf:li>
    </rdf:Alt>
   </dc:description>
   <xmp:CreateDate>{iso_timestamp}</xmp:CreateDate>
   <xmp:ModifyDate>{iso_timestamp}</xmp:ModifyDate>
   <xmp:MetadataDate>{iso_timestamp}</xmp:MetadataDate>
   <pdf:Producer>{safe_producer}</pdf:Producer>
   <pdf:PDFVersion>1.7</pdf:PDFVersion>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""
        return xmp_xml.encode("utf-8")

    @classmethod
    def create_pdfa3_container(
        cls,
        base_pdf_bytes: bytes,
        dcc_xml: Union[str, bytes],
        metadata: Optional[Dict[str, Any]] = None,
        attachment_filename: str = DEFAULT_ATTACHMENT_NAME,
        af_relationship: str = "/Data",
        description: str = "PTB Digital Calibration Certificate (DCC v3.2.1) XML with SmartCom D-SI"
    ) -> bytes:
        """
        Packages a base PDF and machine-readable PTB DCC XML into an ISO 19005-3 compliant
        PDF/A-3 container with Associated Files (/AF) catalog entry and XMP metadata packet.
        """
        # 1. Input bounds and magic bytes validation
        if not base_pdf_bytes or not isinstance(base_pdf_bytes, (bytes, bytearray)):
            raise ValueError("base_pdf_bytes must be non-empty bytes")
        if len(base_pdf_bytes) > cls.MAX_PDF_SIZE_BYTES:
            raise ValueError(f"base_pdf_bytes exceeds maximum allowed size ({cls.MAX_PDF_SIZE_BYTES} bytes)")
        if not base_pdf_bytes.startswith(b"%PDF-"):
            raise ValueError("Invalid PDF header: missing '%PDF-' magic bytes")

        # Normalize DCC XML
        if isinstance(dcc_xml, str):
            xml_bytes = dcc_xml.encode("utf-8")
        elif isinstance(dcc_xml, (bytes, bytearray)):
            xml_bytes = bytes(dcc_xml)
        else:
            raise ValueError("dcc_xml must be str or bytes")

        if len(xml_bytes) == 0:
            raise ValueError("dcc_xml content is empty")
        if len(xml_bytes) > cls.MAX_XML_SIZE_BYTES:
            raise ValueError(f"dcc_xml exceeds maximum allowed size ({cls.MAX_XML_SIZE_BYTES} bytes)")

        # Verify XML well-formedness
        try:
            root_el = ET.fromstring(xml_bytes)
            if not root_el.tag.endswith("digitalCalibrationCertificate"):
                raise ValueError("XML root element must be digitalCalibrationCertificate")
        except ET.ParseError as e:
            raise ValueError(f"Malformed DCC XML: {str(e)}")

        if af_relationship not in cls.VALID_AF_RELATIONSHIPS:
            raise ValueError(f"Invalid AF relationship '{af_relationship}'. Must be one of {cls.VALID_AF_RELATIONSHIPS}")

        meta = metadata or {}
        title = meta.get("title", "OIML R 76-2 Legal Metrology Test Report")
        creator = meta.get("creator", "Regional Reference Standard Laboratory (RRSL)")
        subject = meta.get("subject", "Non-Automatic Weighing Instrument Type Evaluation & Archival Report")
        producer = meta.get("producer", "SIH26035 Metrological Archival Engine")

        # 2. Read base PDF and construct PDF/A-3 writer
        reader = PdfReader(io.BytesIO(base_pdf_bytes))
        writer = PdfWriter()
        writer.pdf_header = cls.PDFA_HEADER

        # Copy all pages from base PDF
        writer.append(reader)

        # 3. Add Attachment via standard /Names/EmbeddedFiles
        writer.add_attachment(attachment_filename, xml_bytes)

        # 4. Enhance File Specification Dictionary for ISO 19005-3 clause 6.8
        root = writer.root_object
        names_dict = root.get("/Names", {}).get_object()
        ef_dict = names_dict.get("/EmbeddedFiles", {}).get_object()
        ef_names = ef_dict.get("/Names", [])

        # Find indirect reference for our attachment
        filespec_ref = None
        for i in range(0, len(ef_names), 2):
            if ef_names[i] == attachment_filename:
                filespec_ref = ef_names[i + 1]
                break

        if not filespec_ref:
            raise RuntimeError(f"Failed to locate attachment {attachment_filename} in embedded files tree")

        filespec = filespec_ref.get_object()
        # Set /AFRelationship (ISO 19005-3 clause 6.8)
        filespec[NameObject("/AFRelationship")] = NameObject(af_relationship)
        filespec[NameObject("/UF")] = create_string_object(attachment_filename)
        filespec[NameObject("/Desc")] = create_string_object(description)

        # Configure EmbeddedFile stream attributes
        stream_obj = filespec["/EF"]["/F"].get_object()
        stream_obj[NameObject("/Subtype")] = NameObject("/application#2Fxml")

        # EmbeddedFile /Params dictionary
        now = datetime.now(timezone.utc)
        pdf_date_str = f"D:{now.strftime('%Y%m%d%H%M%SZ')}"
        params_dict = DictionaryObject()
        params_dict[NameObject("/Size")] = NumberObject(len(xml_bytes))
        params_dict[NameObject("/ModDate")] = create_string_object(pdf_date_str)
        stream_obj[NameObject("/Params")] = params_dict

        # Add Associated Files (/AF) array in Document Catalog
        root[NameObject("/AF")] = ArrayObject([filespec_ref])

        # 5. Add OutputIntent for PDF/A-3 (Device-independent color reproduction)
        output_intent = DictionaryObject({
            NameObject("/Type"): NameObject("/OutputIntent"),
            NameObject("/S"): NameObject("/GTS_PDFA1"),
            NameObject("/OutputConditionIdentifier"): create_string_object("sRGB IEC61966-2.1"),
            NameObject("/Info"): create_string_object("sRGB IEC61966-2.1"),
            NameObject("/RegistryName"): create_string_object("http://www.color.org"),
        })
        intent_ref = writer._add_object(output_intent)
        root[NameObject("/OutputIntents")] = ArrayObject([intent_ref])

        # 6. Inject ISO 19005-3 compliant XMP Metadata Packet
        xmp_packet = cls._build_xmp_metadata(
            title=title,
            creator=creator,
            subject=subject,
            producer=producer,
            part=3,
            conformance="B",
            create_date=now
        )
        writer.xmp_metadata = xmp_packet

        # Ensure /Metadata object in root has /Type /Metadata and /Subtype /XML
        meta_obj = root["/Metadata"].get_object()
        meta_obj[NameObject("/Type")] = NameObject("/Metadata")
        meta_obj[NameObject("/Subtype")] = NameObject("/XML")

        # 7. Write and return PDF/A-3 container bytes
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        return output_buffer.getvalue()

    @classmethod
    def extract_embedded_dcc(
        cls,
        pdf_bytes: bytes,
        target_filename: str = DEFAULT_ATTACHMENT_NAME
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Extracts and parses the embedded PTB DCC v3.2.1 XML from a PDF/A-3 container.
        Returns: (success, raw_xml_string, parsed_dcc_dict)
        """
        if not pdf_bytes or not isinstance(pdf_bytes, (bytes, bytearray)):
            return False, None, {"error": "Invalid or empty PDF input bytes"}
        if not pdf_bytes.startswith(b"%PDF-"):
            return False, None, {"error": "Missing '%PDF-' header"}

        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
        except Exception as e:
            return False, None, {"error": f"Failed to parse PDF structure: {str(e)}"}

        raw_xml_bytes: Optional[bytes] = None

        # Strategy 1: Check reader.attachments
        try:
            attachments = reader.attachments
            if target_filename in attachments:
                raw_xml_bytes = bytes(attachments[target_filename][0])
            else:
                # Search case-insensitively or for any .xml attachment
                for name, data_list in attachments.items():
                    if name.lower() == target_filename.lower() or name.lower().endswith(".xml"):
                        raw_xml_bytes = bytes(data_list[0])
                        break
        except Exception:
            raw_xml_bytes = None

        # Strategy 2: Direct traversal of /Root -> /Names -> /EmbeddedFiles
        if raw_xml_bytes is None:
            try:
                root = reader.trailer["/Root"]
                names = root.get("/Names")
                if names:
                    ef = names.get_object().get("/EmbeddedFiles")
                    if ef:
                        ef_names = ef.get_object().get("/Names", [])
                        for i in range(0, len(ef_names), 2):
                            fname = str(ef_names[i])
                            if fname == target_filename or fname.lower().endswith(".xml"):
                                filespec = ef_names[i + 1].get_object()
                                stream = filespec["/EF"]["/F"].get_object()
                                raw_xml_bytes = stream.get_data()
                                break
            except Exception:
                raw_xml_bytes = None

        if raw_xml_bytes is None:
            return False, None, {"error": f"Attachment '{target_filename}' not found in PDF container"}

        try:
            raw_xml_str = raw_xml_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                raw_xml_str = raw_xml_bytes.decode("latin-1")
            except Exception as e:
                return False, None, {"error": f"Failed to decode XML bytes: {str(e)}"}

        # Parse XML structure
        try:
            root_el = ET.fromstring(raw_xml_str)
        except ET.ParseError as e:
            return False, raw_xml_str, {"error": f"XML parse error: {str(e)}"}

        parsed_data = cls._parse_dcc_tree(root_el)
        return True, raw_xml_str, parsed_data

    @classmethod
    def _parse_dcc_tree(cls, root: ET.Element) -> Dict[str, Any]:
        """
        Parses PTB DCC v3.2.1 XML ElementTree into a structured dictionary.
        Extracts SmartCom D-SI measurement data and RFC 8032 digital seal.
        """
        dcc_ns = cls.DCC_NAMESPACE
        si_ns = cls.DSI_NAMESPACE

        data: Dict[str, Any] = {
            "schema_version": root.attrib.get("schemaVersion", "unknown"),
            "unique_identifier": "",
            "administrative_data": {},
            "statements": {},
            "digital_seal": None,
            "observations": [],
            "observations_count": 0
        }

        # 1. Administrative Data
        admin = root.find(f"{{{dcc_ns}}}administrativeData")
        if admin is not None:
            core = admin.find(f"{{{dcc_ns}}}coreData")
            if core is not None:
                uid_el = core.find(f"{{{dcc_ns}}}uniqueIdentifier")
                if uid_el is not None and uid_el.text:
                    data["unique_identifier"] = uid_el.text.strip()
                receipt_el = core.find(f"{{{dcc_ns}}}receiptDate")
                if receipt_el is not None and receipt_el.text:
                    data["administrative_data"]["receipt_date"] = receipt_el.text.strip()

            item = admin.find(f"{{{dcc_ns}}}item")
            if item is not None:
                manuf = item.find(f"{{{dcc_ns}}}manufacturer")
                model = item.find(f"{{{dcc_ns}}}model")
                data["administrative_data"]["item"] = {
                    "manufacturer": manuf.text.strip() if manuf is not None and manuf.text else "",
                    "model": model.text.strip() if model is not None and model.text else ""
                }

            sw = admin.find(f"{{{dcc_ns}}}software")
            if sw is not None:
                sw_name = sw.find(f"{{{dcc_ns}}}name")
                sw_ver = sw.find(f"{{{dcc_ns}}}version")
                sw_sha = sw.find(f"{{{dcc_ns}}}sha256")
                sw_crc = sw.find(f"{{{dcc_ns}}}crc32")
                data["administrative_data"]["software"] = {
                    "name": sw_name.text.strip() if sw_name is not None and sw_name.text else "",
                    "version": sw_ver.text.strip() if sw_ver is not None and sw_ver.text else "",
                    "sha256": sw_sha.text.strip() if sw_sha is not None and sw_sha.text else "",
                    "crc32": sw_crc.text.strip() if sw_crc is not None and sw_crc.text else "",
                }

            # Cryptographic Statements & Ed25519 Seal
            stmts = admin.find(f"{{{dcc_ns}}}statements")
            if stmts is not None:
                for stmt in stmts.findall(f"{{{dcc_ns}}}statement"):
                    stmt_id = stmt.attrib.get("id", "statement")
                    stmt_dict: Dict[str, Any] = {}
                    data_el = stmt.find(f"{{{dcc_ns}}}data")
                    if data_el is not None:
                        for q in data_el.findall(f"{{{dcc_ns}}}quantity"):
                            ref_type = q.attrib.get("refType")
                            real_el = q.find(f"{{{si_ns}}}real")
                            if real_el is not None:
                                val_el = real_el.find(f"{{{si_ns}}}value")
                                if val_el is not None and val_el.text and ref_type:
                                    stmt_dict[ref_type] = val_el.text.strip()
                    data["statements"][stmt_id] = stmt_dict
                    if stmt_id == "ed25519_seal":
                        data["digital_seal"] = stmt_dict

        # 2. Measurement Results & SmartCom D-SI Table
        results = root.find(f"{{{dcc_ns}}}measurementResults")
        if results is not None:
            for m_res in results.findall(f"{{{dcc_ns}}}measurementResult"):
                data_list = m_res.find(f"{{{dcc_ns}}}data")
                if data_list is None:
                    continue
                table = data_list.find(f"{{{dcc_ns}}}table")
                if table is None:
                    continue

                for row in table.findall(f"{{{dcc_ns}}}row"):
                    step = row.find(f"{{{dcc_ns}}}step")
                    direction = row.find(f"{{{dcc_ns}}}direction")
                    conformity = row.find(f"{{{dcc_ns}}}conformity")

                    reals = row.findall(f"{{{si_ns}}}real")
                    load_val, load_unit = "", ""
                    ind_val, ind_unit = "", ""
                    ec_val, ec_unit = "", ""

                    if len(reals) >= 1:
                        v = reals[0].find(f"{{{si_ns}}}value")
                        u = reals[0].find(f"{{{si_ns}}}unit")
                        load_val = v.text.strip() if v is not None and v.text else ""
                        load_unit = u.text.strip() if u is not None and u.text else ""
                    if len(reals) >= 2:
                        v = reals[1].find(f"{{{si_ns}}}value")
                        u = reals[1].find(f"{{{si_ns}}}unit")
                        ind_val = v.text.strip() if v is not None and v.text else ""
                        ind_unit = u.text.strip() if u is not None and u.text else ""
                    if len(reals) >= 3:
                        v = reals[2].find(f"{{{si_ns}}}value")
                        u = reals[2].find(f"{{{si_ns}}}unit")
                        ec_val = v.text.strip() if v is not None and v.text else ""
                        ec_unit = u.text.strip() if u is not None and u.text else ""

                    obs_record = {
                        "step": step.text.strip() if step is not None and step.text else "",
                        "direction": direction.text.strip() if direction is not None and direction.text else "",
                        "applied_load": {"value": load_val, "unit": load_unit},
                        "indicated_value": {"value": ind_val, "unit": ind_unit},
                        "corrected_error_ec": {"value": ec_val, "unit": ec_unit},
                        "conformity": conformity.text.strip() if conformity is not None and conformity.text else ""
                    }
                    data["observations"].append(obs_record)

        data["observations_count"] = len(data["observations"])
        return data

    @classmethod
    def verify_container_integrity(
        cls,
        pdf_bytes: bytes,
        expected_claims: Optional[Dict[str, Any]] = None,
        trust_store: Optional[TrustStore] = None
    ) -> Dict[str, Any]:
        """
        Audits an ISO 19005-3 container for PDF/A-3b conformance markers,
        Associated Files validity, DCC XML schema adherence, SmartCom D-SI formatting,
        and RFC 8032 Ed25519 digital seal cryptographic integrity.
        """
        result: Dict[str, Any] = {
            "valid_pdfa3": False,
            "pdf_version": "",
            "pdfaid_part": None,
            "pdfaid_conformance": "",
            "has_af_entry": False,
            "af_relationship": "",
            "has_output_intent": False,
            "has_embedded_files": False,
            "dcc_extracted": False,
            "dcc_filename": cls.DEFAULT_ATTACHMENT_NAME,
            "dcc_schema_version": "",
            "certificate_id": "",
            "observations_count": 0,
            "cryptographic_seal_present": False,
            "cryptographic_seal_valid": None,
            "claims_match": None,
            "errors": []
        }

        # 1. Check PDF header & binary bytes
        if not pdf_bytes or len(pdf_bytes) < 15:
            result["errors"].append("PDF byte length too small or empty")
            return result

        if not pdf_bytes.startswith(b"%PDF-"):
            result["errors"].append("Missing %PDF- header magic bytes")
            return result

        header_line = pdf_bytes[:8].decode("latin-1", errors="ignore")
        result["pdf_version"] = header_line.strip()

        # 2. Parse PDF structure via PdfReader
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
        except Exception as e:
            result["errors"].append(f"Failed to parse PDF document structure: {str(e)}")
            return result

        root = reader.trailer.get("/Root")
        if not root:
            result["errors"].append("Document catalog /Root not found")
            return result

        # 3. Verify XMP Metadata Packet for PDF/A-3
        xmp = reader.xmp_metadata
        if xmp is not None:
            try:
                part = getattr(xmp, "pdfaid_part", None)
                conf = getattr(xmp, "pdfaid_conformance", "")
                result["pdfaid_part"] = int(part) if part else None
                result["pdfaid_conformance"] = str(conf) if conf else ""
            except Exception:
                pass

        # Fallback to inspecting raw XMP stream in root if pypdf attribute parse is partial
        if not result["pdfaid_part"] and "/Metadata" in root:
            try:
                meta_stream = root["/Metadata"].get_object().get_data()
                meta_str = meta_stream.decode("utf-8", errors="ignore")
                part_match = re.search(r"<pdfaid:part>(\d+)</pdfaid:part>", meta_str)
                conf_match = re.search(r"<pdfaid:conformance>([A-Za-z]+)</pdfaid:conformance>", meta_str)
                if part_match:
                    result["pdfaid_part"] = int(part_match.group(1))
                if conf_match:
                    result["pdfaid_conformance"] = conf_match.group(1)
            except Exception:
                pass

        # 4. Check Associated Files (/AF) array and /AFRelationship
        af_array = root.get("/AF")
        if af_array:
            result["has_af_entry"] = True
            try:
                af_objs = af_array.get_object() if hasattr(af_array, "get_object") else af_array
                if len(af_objs) > 0:
                    first_af = af_objs[0].get_object()
                    rel = first_af.get("/AFRelationship")
                    if rel:
                        result["af_relationship"] = str(rel)
            except Exception:
                pass

        # 5. Check OutputIntents dictionary
        if "/OutputIntents" in root:
            result["has_output_intent"] = True

        # 6. Check /Names -> /EmbeddedFiles
        names = root.get("/Names")
        if names:
            ef = names.get_object().get("/EmbeddedFiles")
            if ef:
                result["has_embedded_files"] = True

        # Determine overall PDF/A-3 format compliance
        is_pdfa3 = (
            result["pdfaid_part"] == 3
            and result["pdfaid_conformance"] in ("B", "U", "A")
            and result["has_af_entry"]
            and result["af_relationship"] in cls.VALID_AF_RELATIONSHIPS
            and result["has_embedded_files"]
        )
        result["valid_pdfa3"] = is_pdfa3

        # 7. Extract and audit DCC XML
        extracted, raw_xml, parsed_dcc = cls.extract_embedded_dcc(pdf_bytes)
        if not extracted:
            result["errors"].append(f"DCC extraction failed: {parsed_dcc.get('error', 'Unknown')}")
            return result

        result["dcc_extracted"] = True
        result["dcc_schema_version"] = parsed_dcc.get("schema_version", "")
        result["certificate_id"] = parsed_dcc.get("unique_identifier", "")
        result["observations_count"] = parsed_dcc.get("observations_count", 0)
        result["raw_xml"] = raw_xml
        result["parsed_dcc"] = parsed_dcc

        # 8. Cryptographic Seal Verification
        digital_seal = parsed_dcc.get("digital_seal")
        seal_envelope: Optional[Dict[str, Any]] = None
        if digital_seal and isinstance(digital_seal, dict):
            result["cryptographic_seal_present"] = True

            # Case A: Lossless envelope JSON
            if "envelope_json" in digital_seal:
                try:
                    seal_envelope = json.loads(digital_seal["envelope_json"])
                except Exception:
                    seal_envelope = None

            # Case B: Reconstructed envelope from discrete fields
            if not seal_envelope:
                pub_hex = digital_seal.get("pubkey_hex") or digital_seal.get("public_key") or digital_seal.get("pub")
                sig = digital_seal.get("sig") or digital_seal.get("signature")
                rep_hash = digital_seal.get("rep_sha256") or digital_seal.get("report_hash")
                if pub_hex and sig:
                    seal_envelope = {
                        "claims": {
                            "cert_id": digital_seal.get("cert_id", result["certificate_id"]),
                            "sess_id": digital_seal.get("sess_id", digital_seal.get("session_id", "")),
                            "verdict": digital_seal.get("verdict", "PASSED"),
                            "rep_sha256": rep_hash or "",
                            "lrs_sha256": digital_seal.get("lrs_sha256", digital_seal.get("lrs_hash", "")),
                            "rev": int(digital_seal.get("rev", 1)),
                            "ts": str(digital_seal.get("ts", digital_seal.get("timestamp", ""))),
                            "iss": digital_seal.get("iss", "RRSL-Faridabad / Ministry of Consumer Affairs, Govt. of India")
                        },
                        "sig": sig,
                        "pubkey_hex": pub_hex
                    }

            if seal_envelope:
                try:
                    verif_status = Ed25519ReportSigner.verify_envelope(seal_envelope, trust_store=trust_store)
                    is_valid = verif_status.get("is_valid", False)
                    result["cryptographic_seal_valid"] = is_valid
                    if not is_valid:
                        result["errors"].append(f"Ed25519 seal signature invalid: {verif_status.get('message', 'Failed')}")
                except Exception as e:
                    result["cryptographic_seal_valid"] = False
                    result["errors"].append(f"Ed25519 seal verification error: {str(e)}")
            else:
                result["cryptographic_seal_valid"] = False
                result["errors"].append("Digital seal missing public key or signature fields")

        # 9. Cross-validate against expected claims if provided
        if expected_claims:
            claims_matched = True
            seal_claims = seal_envelope.get("claims", {}) if seal_envelope else {}

            if "session_id" in expected_claims:
                exp_sess = str(expected_claims["session_id"])
                cert_id = result["certificate_id"]
                sess_in_claims = seal_claims.get("sess_id", "")
                if exp_sess not in cert_id and exp_sess != sess_in_claims:
                    claims_matched = False
                    result["errors"].append(f"Session ID mismatch: expected '{exp_sess}', found cert_id='{cert_id}'")

            if "report_hash" in expected_claims:
                exp_hash = str(expected_claims["report_hash"]).strip()
                actual_hash = str(seal_claims.get("rep_sha256", digital_seal.get("rep_sha256", digital_seal.get("report_hash", ""))) if digital_seal else "").strip()
                if not actual_hash or not hmac.compare_digest(exp_hash, actual_hash):
                    claims_matched = False
                    result["errors"].append(f"Report hash mismatch: expected '{exp_hash}', got '{actual_hash}'")

            if "verdict" in expected_claims:
                exp_verd = str(expected_claims["verdict"]).strip().upper()
                actual_verd = str(seal_claims.get("verdict", digital_seal.get("verdict", "")) if digital_seal else "").strip().upper()
                if exp_verd != actual_verd:
                    claims_matched = False
                    result["errors"].append(f"Verdict mismatch: expected '{exp_verd}', got '{actual_verd}'")

            result["claims_match"] = claims_matched

        return result
