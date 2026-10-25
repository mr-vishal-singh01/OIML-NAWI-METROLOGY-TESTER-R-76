"""
Ministry Gazette & Legal Metrology Statutory Engine
Smart India Hackathon SIH26035 — PrecisionX Platform

Integrates official Gazette Notifications, Acts, and Statutory Datasets from the
Ministry of Consumer Affairs, Food and Public Distribution (Legal Metrology Division).

Encodes:
1. The Legal Metrology (General) Rules, 2011 (The Seventh Schedule OIML R-76)
2. 4th Amendment G.S.R. 568(E): NAWI Fees Schedule IX & Test Load Substitution Clause 9(2)(ii)
3. 7th Amendment G.S.R. 905(E): 24-Month (2-Year) Verification Stamp Cycle
4. GATC Amendment Rules 2026 G.S.R. 346(E): Private Testing Centre Licensing (Class III & IIII)
5. Jan Vishwas Act 2023 & 2026: Civil Pecuniary Adjudication Matrix (Sections 25, 30, 33, 36)
6. Legal Metrology (IST) Rules 2026 G.S.R. 761(E): CSIR-NPLI Atomic Traceability
7. National Standards Rules 2019: Quantum Planck Constant Mass Traceability
8. Model Approval Rules 2011 & 2019: Pattern Approval Workflow (Section 22)
"""

import os
from decimal import Decimal
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, date

# Dataset directory paths (cross-platform candidates with dynamic fallbacks)
_candidate_paths = [
    os.environ.get("MINISTRY_DATASET_DIR"),
    str(Path(__file__).resolve().parent.parent.parent / "data" / "gazettes"),
    str(Path(__file__).resolve().parent.parent / "data" / "gazettes"),
    str(Path(__file__).resolve().parent.parent.parent / "data" / "gazettes"),
    str(Path.home() / "Desktop" / "DATASET BY SIH MINISTRY "),
    str(Path.home() / "Desktop" / "DATASET BY SIH MINISTRY"),
    str(Path.home() / "Downloads" / "DATASET BY SIH MINISTRY "),
    str(Path.home() / "Downloads" / "DATASET BY SIH MINISTRY"),
]

DATASET_DIR_CANDIDATES = [Path(p) for p in _candidate_paths if p]

MINISTRY_DATASET_DIR = None
for cand in DATASET_DIR_CANDIDATES:
    if cand.exists():
        MINISTRY_DATASET_DIR = cand
        break

# Structured Landmark Gazette Catalog
LANDMARK_GAZETTES = [
    {
        "id": "DOCA-GEN-01",
        "citation": "G.S.R. 71(E) / 2011",
        "act_rule": "The Legal Metrology (General) Rules, 2011",
        "category": "OIML R-76 & General Rules",
        "title": "The Seventh Schedule: Non-Automatic Weighing Instruments (OIML R 76-1)",
        "date_gazetted": "2011-02-07",
        "ministry_dept": "Department of Consumer Affairs • Legal Metrology Division",
        "summary": "Statutory codification of OIML R 76-1 in Indian law. Establishes Table 6 Maximum Permissible Errors (MPE), accuracy classification (Class I, II, III, IIII), turning-point testing (ΔL), zero error (E0), and rounding error correction (Ec).",
        "precisionx_pillar": "Core NAWI Calculation Engine & Automated Table 6 Enforcement Middleware",
        "filename": "stdrules-compressed_0_1732708966.pdf"
    },
    {
        "id": "DOCA-FEES-04",
        "citation": "G.S.R. 568(E) / 2026",
        "act_rule": "General Rules (4th Amendment), 2026",
        "category": "Fees & Substitution",
        "title": "NAWI Verification Fee Slabs (Schedule IX) & Test Load Substitution Rules",
        "date_gazetted": "2026-07-03",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Amends Seventh Schedule Clause 9(2)(ii): Permits test load substitution down to 20% of Max capacity if repeatability error ΔE <= 0.2e, or 33% if ΔE <= 0.3e. Re-calibrates statutory fee slabs under Schedule IX.",
        "precisionx_pillar": "Automated Schedule IX Fee Calculator & Dynamic Test Load Substitution Optimizer",
        "filename": "Gen_Rules_4th_Amendment_NAWI_Fees_1783336378.pdf"
    },
    {
        "id": "DOCA-7TH-CYCLE",
        "citation": "G.S.R. 905(E) / 2025",
        "act_rule": "General Rules (7th Amendment), 2025",
        "category": "OIML R-76 & General Rules",
        "title": "Standardization of 24-Month (2-Year) Verification Stamp Validity",
        "date_gazetted": "2025-12-18",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Amends Rule 27(2)(a): Standardizes verification stamp and legal certificate validity to 24 Months (2 Years) for commercial weighing instruments.",
        "precisionx_pillar": "Dynamic 24-Month Re-Verification Scheduler & Quarter Stamp Engine",
        "filename": "2025.12.18 Gen Rules 7th Amendment 2 yr verification period_1766504014.pdf"
    },
    {
        "id": "DOCA-GATC-26",
        "citation": "G.S.R. 346(E) / 2026",
        "act_rule": "GATC Amendment Rules, 2026",
        "category": "GATC Private Testing",
        "title": "Government Approved Test Centres (GATC) NAWI Testing Scope Expansion",
        "date_gazetted": "2026-05-08",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "First Schedule Entry 6: Authorizes accredited private Government Approved Test Centres (GATC) to verify Class III NAWI (up to 150 kg) and Class IIII instruments under Section 14.",
        "precisionx_pillar": "Multi-Tenant GATC Private Laboratory Workbench & Remote RRSL Audit Relay",
        "filename": "GATC_Amendment_Rules_2026_1778476324.pdf"
    },
    {
        "id": "DOCA-JV-2023",
        "citation": "Act No. 18 of 2023",
        "act_rule": "Jan Vishwas (Amendment of Provisions) Act, 2023",
        "category": "Jan Vishwas Adjudication",
        "title": "Decriminalization of Procedural Infractions into Civil Pecuniary Penalties",
        "date_gazetted": "2023-08-11",
        "ministry_dept": "Ministry of Law and Justice & Department of Consumer Affairs",
        "summary": "Decriminalizes technical metrology infractions under Sections 25, 29, 30, and 33. Replaces criminal court prosecution with structured administrative adjudication and compounding penalty slabs.",
        "precisionx_pillar": "Civil Adjudication Penalty Engine & Tamper-Evident SHA-256 Audit Trail",
        "filename": "Jan Vishwas (Amendment of Provisions) Act, 2023 (18 of 2023)_1732708241.pdf"
    },
    {
        "id": "DOCA-JV-2026",
        "citation": "Act No. 8 of 2026 / S.O. 2103(E)",
        "act_rule": "Jan Vishwas Enforcement Notification, 2026",
        "category": "Jan Vishwas Adjudication",
        "title": "Enforcement of Legal Metrology Decriminalization & Adjudicating Officers",
        "date_gazetted": "2026-04-27",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Formally establishes Adjudicating Officers (State Joint Controller / Deputy Controller) to impose monetary penalties under Section 25 (unverified weights) up to ₹50,000.",
        "precisionx_pillar": "Statutory Penalty Calculator & Adjudication Case Dossier Generator",
        "filename": "2026.4.27 JV Act 2026 for LM Act_1777348318.pdf"
    },
    {
        "id": "DOCA-QR-STAMP",
        "citation": "Notification No. WM-10(5)/2023",
        "act_rule": "Legal Metrology (QR Code Stamping) Mandate",
        "category": "Digital Stamping & QR",
        "title": "Mandatory Dynamic Cryptographic QR Code on Stamped Scales",
        "date_gazetted": "2023-06-23",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Mandates machine-readable QR codes on verification certificates and physical stamping plates containing Certificate ID, Verification Date, Expiry, MPE, and Digital Signature.",
        "precisionx_pillar": "Offline RFC 8032 Ed25519 Compact High-Density QR Stamping Generator",
        "filename": "Notification -  Legal Metrology (QR Code)_1732871487.pdf"
    },
    {
        "id": "DOCA-IST-2026",
        "citation": "G.S.R. 761(E) / 2026",
        "act_rule": "Legal Metrology (IST) Rules, 2026",
        "category": "National Standards & Timing",
        "title": "Indian Standard Time (IST) Atomic Clock Traceability Mandate",
        "date_gazetted": "2026-08-27",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Prohibits non-IST timestamps across legal certificates. Mandates format 'DD-MM-YYYY HH:MM:SS IST' traceable to CSIR-National Physical Laboratory (NPLI) atomic clocks.",
        "precisionx_pillar": "Strict CSIR-NPLI Atomic IST Time Protocol in PDF/A-3, XML, and Ed25519 Signatures",
        "filename": "2026.08.27 IST Rules_1788026429.pdf"
    },
    {
        "id": "DOCA-MODEL-11",
        "citation": "G.S.R. 183(E) / 2011",
        "act_rule": "Legal Metrology (Approval of Models) Rules, 2011",
        "category": "Model Approvals",
        "title": "Pattern Approval Procedures for Weighing and Measuring Instruments",
        "date_gazetted": "2011-03-01",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Requires all manufacturers and importers of NAWI to obtain Model Approval under Section 22 before commercial sale. Mandates OIML R-76 laboratory test reports.",
        "precisionx_pillar": "Section 22 Pattern Approval Registry & PTB DCC v3.2.1 Interoperability",
        "filename": "approval_of_models_rules_0_1732709311.pdf"
    },
    {
        "id": "DOCA-NAT-STD",
        "citation": "G.S.R. 474(E) / 2019",
        "act_rule": "National Standards Rules, 2019",
        "category": "National Standards & Timing",
        "title": "Redefinition of the Kilogram via Planck Constant (Quantum Metrology)",
        "date_gazetted": "2019-07-05",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Redefines SI unit of mass (kg) via Planck Constant h = 6.62607015 × 10^-34 J s. Establishes the 4-tier calibration hierarchy: National Prototype -> Reference Standards -> Secondary Standards -> Working Standards.",
        "precisionx_pillar": "RRSL Traceability Budget Engine (Standard Weight Uncertainty U <= 1/3 MPE)",
        "filename": "National_Std_Rules2019_1732709005.pdf"
    },
    {
        "id": "DOCA-SOP-OIL",
        "citation": "Office Memorandum 2023-WM",
        "act_rule": "Standard Operating Procedure (SOP), 2023",
        "category": "Packaged Commodities",
        "title": "Standard Operating Procedure for Edible Oils & Fats Net Quantity Measurement",
        "date_gazetted": "2023-12-29",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Official procedure for temperature-compensated mass determination of edible oils and fats to prevent under-filling fraud.",
        "precisionx_pillar": "Form 3 Gravimetric Tare & Environmental Temperature Correction Subroutines",
        "filename": "2023.12.29 Standard Operating Procedure for Edible oil & Fats Net Quantity Measurement signed copy_1732872010.pdf"
    },
    {
        "id": "DOCA-GATC-BASE",
        "citation": "G.S.R. 593(E) / 2013",
        "act_rule": "Legal Metrology (GATC) Rules, 2013",
        "category": "GATC Private Testing",
        "title": "Government Approved Test Centres (GATC) Framework & Accreditation",
        "date_gazetted": "2013-09-04",
        "ministry_dept": "Department of Consumer Affairs",
        "summary": "Establishes institutional framework for delegating verification of selected commercial weights and measures to approved private centers under Section 14.",
        "precisionx_pillar": "Statutory GATC Multi-Laboratory Federation & Role Isolation Architecture",
        "filename": "gatc_1732710153.pdf"
    }
]


def list_ministry_gazettes(
    category: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Returns filtered gazettes and scans the physical dataset directory for all 91 PDFs.
    """
    physical_files = {}
    if MINISTRY_DATASET_DIR and MINISTRY_DATASET_DIR.exists():
        for p in MINISTRY_DATASET_DIR.glob("*.pdf"):
            physical_files[p.name] = {
                "filename": p.name,
                "size_kb": p.stat().st_size // 1024,
                "path": str(p)
            }

    # Start with curated landmark gazettes
    results = []
    seen_files = set()

    for g in LANDMARK_GAZETTES:
        fname = g.get("filename")
        seen_files.add(fname)
        item = dict(g)
        item["available_on_disk"] = fname in physical_files
        item["file_size_kb"] = physical_files[fname]["size_kb"] if fname in physical_files else 0
        item["download_url"] = f"/api/ministry/gazette/{fname}" if item["available_on_disk"] else None
        results.append(item)

    # Add remaining physical files from dataset
    for fname, meta in physical_files.items():
        if fname in seen_files:
            continue
        
        # Categorize dynamically
        cat = "Statutory Amendments"
        if "PCR" in fname or "Garments" in fname or "Pan Masala" in fname:
            cat = "Packaged Commodities"
        elif "GATC" in fname or "gatc" in fname:
            cat = "GATC Private Testing"
        elif "General" in fname or "Gen" in fname or "stdrules" in fname:
            cat = "OIML R-76 & General Rules"
        elif "Jan Vishwas" in fname or "JV" in fname:
            cat = "Jan Vishwas Adjudication"
        elif "Approval" in fname or "approval" in fname:
            cat = "Model Approvals"
        elif "QR" in fname:
            cat = "Digital Stamping & QR"

        clean_title = fname.replace(".pdf", "").replace("_", " ")
        results.append({
            "id": f"DOCA-AUTO-{len(results) + 1:02d}",
            "citation": "Official Gazette of India",
            "act_rule": "The Legal Metrology Act, 2009",
            "category": cat,
            "title": clean_title,
            "date_gazetted": "2021-2026",
            "ministry_dept": "Ministry of Consumer Affairs, Food & Public Distribution",
            "summary": f"Official gazette notification record filed under {clean_title}. Preserved in SIH Ministry Dataset.",
            "precisionx_pillar": "Statutory Document Archival & Regulatory Compliance",
            "filename": fname,
            "available_on_disk": True,
            "file_size_kb": meta["size_kb"],
            "download_url": f"/api/ministry/gazette/{fname}"
        })

    # Filter by category
    if category and category.lower() != "all":
        results = [r for r in results if r["category"].lower() == category.lower()]

    # Filter by search query
    if query:
        q = query.lower()
        results = [
            r for r in results
            if q in r["title"].lower()
            or q in r["citation"].lower()
            or q in r["summary"].lower()
            or q in r["category"].lower()
            or q in r.get("precisionx_pillar", "").lower()
        ]

    total_count = len(results)
    paginated = results[offset:offset + limit]

    return {
        "total_count": total_count,
        "dataset_dir_found": MINISTRY_DATASET_DIR is not None,
        "total_dataset_files": len(physical_files),
        "limit": limit,
        "offset": offset,
        "gazettes": paginated
    }


def get_gazette_file_path(filename: str) -> Optional[Path]:
    """Resolves a physical PDF file from the SIH Ministry Dataset."""
    if not MINISTRY_DATASET_DIR or not MINISTRY_DATASET_DIR.exists():
        return None
    target = MINISTRY_DATASET_DIR / filename
    if target.exists() and target.is_file():
        return target
    return None


def calculate_schedule_ix_fee(
    accuracy_class: str,
    max_capacity_kg: float,
    is_in_situ: bool = False
) -> Dict[str, Any]:
    """
    Computes statutory government verification fee under Schedule IX
    of the Legal Metrology (General) Rules as amended by G.S.R. 568(E).
    """
    cap = float(max_capacity_kg)
    ac = accuracy_class.upper()
    fee = 0
    slab = ""

    if ac in ["CLASS_I", "CLASS I", "SPECIAL"]:
        if cap <= 0.2:  # <= 200 g
            fee = 3000
            slab = "Class I Micro/Analytical Balance (Max <= 200 g)"
        else:
            fee = 5000
            slab = "Class I Analytical Balance (Max > 200 g)"

    elif ac in ["CLASS_II", "CLASS II", "HIGH"]:
        if cap <= 50.0:
            fee = 2000
            slab = "Class II Precision Balance (Max <= 50 kg)"
        else:
            fee = 3000
            slab = "Class II Precision Platform Scale (Max > 50 kg)"

    elif ac in ["CLASS_III", "CLASS III", "MEDIUM"]:
        if cap <= 10.0:
            fee = 200
            slab = "Class III Counter Scale (Max <= 10 kg)"
        elif cap <= 50.0:
            fee = 500
            slab = "Class III Industrial Scale (10 kg < Max <= 50 kg)"
        elif cap <= 500.0:
            fee = 1000
            slab = "Class III Heavy Platform Scale (50 kg < Max <= 500 kg)"
        elif cap <= 5000.0:
            fee = 2000
            slab = "Class III Heavy Industrial Scale (500 kg < Max <= 5,000 kg)"
        else:
            # Over 5 tonnes: ₹5,000 + ₹500 for every additional 5 tonnes
            extra_tonnes = max(0.0, cap - 5000.0)
            extra_blocks = int(extra_tonnes / 5000.0) + (1 if extra_tonnes % 5000.0 > 0 else 0)
            fee = 5000 + (extra_blocks * 500)
            slab = f"Class III Weighbridge (Max = {cap:,.0f} kg, Base ₹5,000 + {extra_blocks}x ₹500)"

    elif ac in ["CLASS_IIII", "CLASS IIII", "ORDINARY"]:
        if cap <= 500.0:
            fee = 500
            slab = "Class IIII Ordinary Platform (Max <= 500 kg)"
        elif cap <= 5000.0:
            fee = 1000
            slab = "Class IIII Heavy Scale (500 kg < Max <= 5,000 kg)"
        else:
            fee = 3000
            slab = "Class IIII Weighbridge / Hopper Scale (Max > 5,000 kg)"

    else:
        fee = 500
        slab = "General Weighing Instrument Standard Fee"

    # In-situ verification fee (additional 50% for on-site field testing)
    surcharge = 0
    if is_in_situ:
        surcharge = int(fee * 0.5)

    total_fee = fee + surcharge

    return {
        "statutory_schedule": "The Seventh & Ninth Schedules (G.S.R. 568(E))",
        "accuracy_class": accuracy_class,
        "max_capacity_kg": cap,
        "base_verification_fee_inr": fee,
        "in_situ_field_surcharge_inr": surcharge,
        "total_statutory_fee_inr": total_fee,
        "fee_slab_description": slab,
        "currency": "INR (₹)",
        "statutory_mandate": "Rule 24, The Legal Metrology (General) Rules, 2011"
    }


def calculate_substitution_allowance(
    max_capacity_kg: float,
    repeatability_error_e: float
) -> Dict[str, Any]:
    """
    Calculates test load substitution under 4th Amendment G.S.R. 568(E) Clause 9(2)(ii).
    """
    cap = float(max_capacity_kg)
    err = float(repeatability_error_e)

    if err <= 0.2:
        std_pct = 20.0
        sub_pct = 80.0
        clause = "G.S.R. 568(E) Clause 9(2)(ii)(b): Repeatability <= 0.2e (Maximum Substitution)"
    elif err <= 0.3:
        std_pct = 33.0
        sub_pct = 67.0
        clause = "G.S.R. 568(E) Clause 9(2)(ii)(a): Repeatability <= 0.3e (High Substitution)"
    else:
        std_pct = 50.0
        sub_pct = 50.0
        clause = "G.S.R. 568(E) Baseline Rule: Repeatability > 0.3e (Standard 50% Substitution)"

    std_weight_kg = (std_pct / 100.0) * cap
    sub_weight_kg = (sub_pct / 100.0) * cap

    return {
        "max_capacity_kg": cap,
        "measured_repeatability_error_e": err,
        "statutory_clause": clause,
        "required_standard_weights_pct": std_pct,
        "required_standard_weights_kg": round(std_weight_kg, 3),
        "permitted_substitution_materials_pct": sub_pct,
        "permitted_substitution_materials_kg": round(sub_weight_kg, 3),
        "transportation_savings_kg": round(cap - std_weight_kg, 3)
    }


def calculate_jan_vishwas_penalty(
    infraction_code: str,
    repeat_offense: bool = False
) -> Dict[str, Any]:
    """
    Calculates civil compounding/adjudication penalties under Jan Vishwas Acts (2023 & 2026).
    """
    infractions = {
        "SECTION_25": {
            "title": "Use of Unverified Weight or Measure (Section 25)",
            "statutory_section": "Section 25 of The Legal Metrology Act, 2009",
            "first_offense_penalty_inr": 20000,
            "repeat_offense_penalty_inr": 50000,
            "decriminalized": True,
            "adjudicating_authority": "Adjudicating Officer (Joint / Deputy Controller of Legal Metrology)"
        },
        "SECTION_26": {
            "title": "Tampering of Weight, Measure or Software Seal (Section 26)",
            "statutory_section": "Section 26 of The Legal Metrology Act, 2009",
            "first_offense_penalty_inr": 50000,
            "repeat_offense_penalty_inr": 100000,
            "decriminalized": True,
            "adjudicating_authority": "Adjudicating Officer"
        },
        "SECTION_29": {
            "title": "Use of Non-Standard Weight or Measure (Section 29)",
            "statutory_section": "Section 29 of The Legal Metrology Act, 2009",
            "first_offense_penalty_inr": 25000,
            "repeat_offense_penalty_inr": 50000,
            "decriminalized": True,
            "adjudicating_authority": "Adjudicating Officer"
        },
        "SECTION_30": {
            "title": "Short Weight / Out-of-Tolerance Delivery (Section 30)",
            "statutory_section": "Section 30 of The Legal Metrology Act, 2009",
            "first_offense_penalty_inr": 10000,
            "repeat_offense_penalty_inr": 25000,
            "decriminalized": True,
            "adjudicating_authority": "Adjudicating Officer"
        },
        "SECTION_36": {
            "title": "Contravention of Packaged Commodity Rules (Section 36)",
            "statutory_section": "Section 36 of The Legal Metrology Act, 2009",
            "first_offense_penalty_inr": 25000,
            "repeat_offense_penalty_inr": 50000,
            "decriminalized": True,
            "adjudicating_authority": "Adjudicating Officer"
        }
    }

    info = infractions.get(infraction_code, infractions["SECTION_25"])
    penalty = info["repeat_offense_penalty_inr"] if repeat_offense else info["first_offense_penalty_inr"]

    return {
        "infraction_code": infraction_code,
        "title": info["title"],
        "statutory_section": info["statutory_section"],
        "is_repeat_offense": repeat_offense,
        "adjudication_penalty_inr": penalty,
        "decriminalization_statute": "Jan Vishwas (Amendment of Provisions) Act, 2023 & 2026",
        "adjudicating_authority": info["adjudicating_authority"],
        "appeal_provisions": "Appeal lies to Appellate Authority within 30 days under Section 50"
    }
