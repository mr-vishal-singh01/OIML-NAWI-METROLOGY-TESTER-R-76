# 🇮🇳 OIML-NAWI-METROLOGY-TESTER-R-76

### Automated OIML R-76 Guided NAWI Testing Suite, ISO 19005-3 PDF/A-3, PTB DCC v3.2.1 XML & Ed25519 Cryptographic Verification
**Smart India Hackathon (SIH26035) — Team PrecisionX**  
*Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division, Govt. of India*

---

## 📌 Executive Summary

India is an issuing authority under the **OIML-CS (OIML Certificate System)**, yet verification of Non-Automatic Weighing Instruments (NAWIs) across Regional Reference Standards Laboratories (RRSLs) and field inspection stations often relies on error-prone spreadsheets, unauthenticated paper printouts, and disconnected calibration software.

**PrecisionX (OIML-NAWI-METROLOGY-TESTER-R-76)** provides a zero-trust, local-first metrological testing suite conforming strictly to **OIML R 76-1:2006 (E)** and **ISO/IEC 17025:2017**. It automates guided testing, derives turning point errors, enforces anti-rollback amendment state machines, and cryptographically signs test certificates with **Ed25519 digital seals** and **PTB DCC v3.2.1 XML embedded inside ISO 19005-3 PDF/A-3 archival containers**.

---

## 🎯 Key Capabilities & Technical Features

- **Automated OIML R-76 Guided Testing**:
  - **Form 1 (Weighing Performance & Hysteresis)**: 12 standardized load steps (Loading & Unloading) with sub-division turning point derivation:
    $$P = I + 0.5d - \Delta L$$
    $$E = P - L, \quad E_c = E - E_0$$
    Automatic evaluation against Class I, II, III, and IIII Maximum Permissible Error (MPE Table 6).
  - **Form 3 (Corner Eccentricity)**: 5 platform positions tested at $\frac{1}{3} \text{Max}$ or $\frac{1}{4} \text{Max}$ for off-center loading.
  - **Form 5 (Repeatability)**: Automatic standard deviation and maximum error spread ($\Delta E_{\text{max}}$) across 50% and 100% capacity series.
  - **Form 15 (WELMEC 7.2 Software Examination)**: Checksum verification, legally relevant parameter audit, and software sealing (Extension L & U).
- **ISO/IEC 17025 Invalidation Engine & Merkle Audit Trail**:
  - Any post-hoc amendment of an observation revokes approval, demands mandatory technical justification, and flags calculations `STALE`.
  - Immutable historical archives maintain previous revisions frozen with cryptographic SHA-256 state hashes.
- **Cryptographic Portability (Zero-Internet Verification)**:
  - **Ed25519 Asymmetric Signatures**: 64-byte compact cryptographic seal generated using RFC 8032.
  - **Damage-Tolerant QR Seals**: High-density QR (Level H) with OpenCV 5-stage computer vision preprocessing recovering up to 30% physical tears or abrasions.
  - **Dual Interoperable Archival Format**: Generates ISO 19005-3 compliant PDF/A-3 documents embedding machine-readable PTB Digital Calibration Certificate (DCC v3.2.1) XML.
- **Cross-Platform Architecture**:
  - **Desktop Workbench**: 1-click execution for Windows (`run_workbench.bat`) and Linux (`run_workbench.sh`).
  - **Field Mobile Inspector**: Offline Progressive Web App (PWA) and Android scanner with laser viewfinder.
  - **Raspberry Pi Bench Appliance**: Headless or full-screen touch kiosk with systemd autostart and RS-232 serial scale bridge.

---

## 📁 Repository Architecture

```
OIML-NAWI-METROLOGY-TESTER-R-76/
├── backend/
│   ├── core/
│   │   ├── nawi_engine.py             # Metrological kernel, OIML R-76 MPE formulas & turning point logic
│   │   ├── welmec_sealer.py           # WELMEC 7.2 software verification, checksums & security levels
│   │   ├── dcc_generator.py           # PTB Digital Calibration Certificate (DCC v3.2.1) XML generator
│   │   ├── offline_qr.py              # Ed25519 signing/verification & base45/cbor QR serialization
│   │   └── opencv_qr_pipeline.py     # CLAHE, adaptive thresholding & damaged QR recovery
│   ├── api/
│   │   ├── main.py                    # FastAPI REST backend, live test session state & admin portal
│   │   ├── database.py                # SQLite WAL persistence layer conforming to WELMEC Ext L
│   │   └── workflow.py                # ISO/IEC 17025 test session workflow & invalidation engine
│   ├── hardware/
│   │   └── scale_driver.py            # Serial bridge for MT-SICS, SMA & continuous scale streams
│   └── reporting/
│       ├── report_generator.py        # OIML R-76 report builder & calibration summary
│       └── pdfa3_engine.py            # ISO 19005-3 PDF/A-3 container embedding PTB DCC XML
├── desktop/                           # Desktop application assets and launchers
├── mobile/                            # Field Inspector PWA & Capacitor Android camera scanner
├── pi-kiosk/                          # Raspberry Pi 4 / 5 auto-boot touch appliance scripts
├── schemas/                           # JSON schemas for OIML R-76 test definitions & DCC templates
├── tests/                             # Complete 111-Test unit & metrological verification test suite
├── requirements.txt                   # Production Python dependencies
├── run_workbench.bat                  # 1-Click Windows launcher
├── install.bat                        # 1-Click Windows dependency & shortcut installer
├── run_workbench.sh                   # 1-Click Linux launcher
└── README.md
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.10+** (Python 3.11 / 3.12 recommended)
- **Git**

### 2. Installation

#### 🐧 Linux / macOS
```bash
git clone https://github.com/mr-vishal-singh01/OIML-NAWI-METROLOGY-TESTER-R-76.git
cd OIML-NAWI-METROLOGY-TESTER-R-76

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 🪟 Windows
```bat
git clone https://github.com/mr-vishal-singh01/OIML-NAWI-METROLOGY-TESTER-R-76.git
cd OIML-NAWI-METROLOGY-TESTER-R-76

# Run 1-click installer
install.bat
```

---

## 🚀 Running the Workbench

### Using the Automated Runner:
- **Linux / macOS**: `./run_workbench.sh`
- **Windows**: Double-click `run_workbench.bat`

### Manual Execution:
```bash
python -m uvicorn api.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
Once launched, navigate to:
- **Interactive Workbench UI**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Mobile Field Inspector PWA**: [http://127.0.0.1:8000/mobile/scanner.html](http://127.0.0.1:8000/mobile/scanner.html)
- **Live PDF/A-3 Export**: `http://127.0.0.1:8000/api/report/pdfa3`
- **PTB DCC v3.2.1 XML**: `http://127.0.0.1:8000/api/report/dcc`

### Default Admin Credentials:
- **Username:** `admin` (or `DR_SHARMA`)
- **Password:** `PrecisionX@2026`

---

## 🧪 Verification & Automated Testing

The codebase includes an extensive **111-test suite** covering metrology calculations, error bounds, tamper resistance, and PDF/A-3 container generation:

```bash
python -m pytest tests -v
```

```
============================= test session starts ==============================
collected 111 items

tests/test_complete_system.py .............. PASSED
tests/test_database_persistence.py ......... PASSED
tests/test_ed25519_advanced_resilience.py .. PASSED
tests/test_ed25519_degradation_sweep.py .... PASSED
tests/test_ed25519_offline_qr.py ........... PASSED
tests/test_jury_demo_workflow.py ........... PASSED
tests/test_master_metrology_security_suite.  PASSED
tests/test_nawi_engine.py .................. PASSED
tests/test_opencv_fuzzing_pipeline.py ...... PASSED
tests/test_pdfa3_container.py .............. PASSED
tests/test_revision_workflow.py ............ PASSED
tests/test_vertical_slice_api.py ........... PASSED

======================== 111 passed in 108.04s (0:01:48) ========================
```

---

## 🏛️ Standards & Regulatory Compliance

- **OIML R 76-1:2006 (E)**: *Non-automatic weighing instruments — Part 1: Metrological and technical requirements — Tests.*
- **WELMEC Guide 7.2 (Issue 5)**: *Software Guide (Measuring Instruments Directive 2014/32/EU).*
- **ISO/IEC 17025:2017**: *General requirements for the competence of testing and calibration laboratories.*
- **ISO 19005-3:2012 (PDF/A-3)**: *Document management — Electronic document file format for long-term preservation.*
- **PTB DCC v3.2.1**: *Physikalisch-Technische Bundesanstalt Digital Calibration Certificate XML Schema.*
- **RFC 8032**: *Edwards-Curve Digital Signature Algorithm (Ed25519).*

---

## 👥 Team PrecisionX (Smart India Hackathon 2026)

- **Problem Statement**: SIH26035 — Development of an Automated Software Tool for Verification of Non-Automatic Weighing Instruments (NAWIs) as per OIML R-76.
- **Organization**: Ministry of Consumer Affairs, Food and Public Distribution (Legal Metrology Division).
