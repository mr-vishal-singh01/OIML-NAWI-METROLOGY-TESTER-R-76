# 🇮🇳 OIML-NAWI-METROLOGY-TESTER-R-76

### Automated OIML R-76 Guided NAWI Testing Suite, ISO 19005-3 PDF/A-3, PTB DCC v3.2.1 XML & Ed25519 Cryptographic Verification
**Smart India Hackathon (SIH26035) — Team PrecisionX**  
*Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division, Govt. of India*

---

## 📌 Executive Summary

India is an official issuing authority under the **OIML-CS (OIML Certificate System)**, yet verification of Non-Automatic Weighing Instruments (NAWIs) across Regional Reference Standards Laboratories (RRSLs) and field inspection stations often relies on error-prone spreadsheets, unauthenticated paper printouts, and disconnected calibration software.

**PrecisionX (OIML-NAWI-METROLOGY-TESTER-R-76)** provides a zero-trust, local-first metrological testing suite conforming strictly to **OIML R 76-1:2006 (E)** and **ISO/IEC 17025:2017**. It automates guided testing, derives turning point errors, enforces anti-rollback amendment state machines, and cryptographically signs test certificates with **Ed25519 digital seals** and **PTB DCC v3.2.1 XML embedded inside ISO 19005-3 PDF/A-3 archival containers**.

---

## 🏛️ National Metrological Context: India as the 13th OIML-CS Issuing Authority
![India 13th OIML-CS Issuing Authority](docs/screenshots/14_india_13th_oiml_cs_issuing_authority.png)

* **Name**: `India as the 13th OIML-CS Issuing Authority in the World`
* **Work**: Commemorates and visualizes India's accession to the elite circle of **13 nations** globally recognized by the International Organization of Legal Metrology (OIML) to issue international OIML Pattern Approval Certificates.
* **How It Works**: Under the OIML Certificate System (OIML-CS), 13 countries (*Australia, Switzerland, China, Czech Republic, Germany, Denmark, France, United Kingdom, Japan, Netherlands, Sweden, Slovakia, and India*) possess peer-reviewed legal metrology infrastructure to test, verify, and issue certificates of conformity that are accepted internationally by member nations without repetitive re-testing.
* **Why It Is Needed**: 
  - Historically, Indian manufacturers were forced to spend large amounts of foreign currency and endure 6–12 months of shipping delays to get weighing scales tested in European labs like PTB (Germany) or NMi (Netherlands).
  - While India achieved this historic 13th issuing authority status, domestic Regional Reference Standards Laboratories (RRSLs) still relied on manual excel spreadsheets and unverified printouts.
  - **PrecisionX** was directly engineered for **Smart India Hackathon Problem Statement SIH26035** to bridge this gap: replacing manual sheets with an automated, tamper-proof, ISO/IEC 17025 compliant digital workbench to uphold India's global issuing credibility.
* **Where It Is Used**: National policy presentations, Ministry of Consumer Affairs defenses, RRSL lab accreditations, and international OIML peer audits.

---

## 📸 Comprehensive Visual Walkthrough & System Architecture

Below is a detailed engineering and regulatory breakdown of each interface module, detailing its **Name**, **Work (Function)**, **How It Works (Technical Mechanics)**, **Why It Is Needed (Standards Compliance)**, and **Where It Is Used (Operational Context)**.

---

### 1. Admin Control & Lab Supervisor Sign-Off Panel
![Admin Control & Supervisor Sign-off](docs/screenshots/01_admin_control_supervisor_signoff.png)

* **Name**: `Admin Control & Authorized Supervisor Sign-Off Panel`
* **Work**: Provides role-based administrative governance (Security Level 3) for authorized scientists and laboratory directors. Allows reviewing testing remarks, locking test revisions with asymmetric digital seals, inspecting the cryptographic ledger, and exporting JSON audit logs.
* **How It Works**: Verifies user session claims (`Dr. A. K. Sharma`, Director RRSL) via session tokens. Upon clicking **"Sign & Certify Revision"**, it signs the active session hash with an Ed25519 private key (RFC 8032), transitions review lifecycle from `DRAFT` to `APPROVED`, and calculates the SHA-256 Merkle root and CRC-32 checksum of all underlying observation records.
* **Why It Is Needed**: Mandated by **WELMEC Guide 7.2 (Extension L & Extension U)** and **ISO/IEC 17025:2017 Clause 7.8.2.1**; calibration certificates cannot be approved or published by standard operators without verified supervisory technical authorization.
* **Where It Is Used**: Regional Reference Standards Laboratories (RRSLs) and State Legal Metrology verification centers during final certification review.

---

### 2. Form 1: Weighing Performance & Turning Point Derivation
![Form 1: Weighing Performance](docs/screenshots/02_form1_weighing_performance.png)

* **Name**: `Form 1: Weighing Performance & Hysteresis Test (Clause A.4.4)`
* **Work**: Guides the metrologist through 12 standardized test loads across loading and unloading cycles. Derives sub-division turning point errors to eliminate digital rounding ambiguities.
* **How It Works**: 
  1. The operator enters Indication ($I$) and applies fractional additive weights ($\Delta L$) until the scale indication rolls over to $I + d$.
  2. The turning point calculation derives exact unrounded load:
     $$P = I + 0.5d - \Delta L$$
  3. Raw error is calculated as $E = P - L$, and corrected for zero-drift ($E_0$):
     $$E_c = E - E_0$$
  4. $E_c$ is evaluated against statutory MPE brackets ($\pm 0.5e, \pm 1.0e, \pm 1.5e$) per OIML R 76-1 Table 6.
* **Why It Is Needed**: Required under **OIML R 76-1 Clause A.4.4.1 & A.4.4.3**. Standard digital displays only show stepped values rounded to division $d$; fractional weights are strictly mandatory to determine the actual turning point.
* **Where It Is Used**: On calibration test benches during initial pattern approval and mandatory periodic reverification.

---

### 3. Form 3: Corner Eccentricity Test
![Form 3: Corner Eccentricity](docs/screenshots/03_form3_corner_eccentricity.png)

* **Name**: `Form 3: Corner Eccentricity Test (Clause 3.6.2 & A.4.7)`
* **Work**: Assesses whether off-center loading on the weighing platform introduces non-linear load-cell torque or lever errors.
* **How It Works**: An interactive scale pan top-view guides the operator across 5 geometric quadrants (Center, Front-Left, Front-Right, Back-Left, Back-Right) applying $\frac{1}{3}\text{ Max}$ ($5000\text{ g}$ on a 4-point platform). Evaluates that the difference between any corner reading and the center reading does not exceed statutory maximum permissible error ($|\Delta E_{\text{corner}}| \le \text{MPE}$).
* **Why It Is Needed**: Mandated by **OIML R 76-1 Clause 3.6.2**. In retail and trade, goods are rarely placed dead center; scales must maintain accuracy regardless of eccentric pan placement.
* **Where It Is Used**: Verification laboratories during mechanical inspection of load receptors and pan mounts.

---

### 4. Form 5: Repeatability Test
![Form 5: Repeatability](docs/screenshots/04_form5_repeatability_series.png)

* **Name**: `Form 5: Repeatability Verification (Clause 3.6.1 & A.4.10)`
* **Work**: Verifies measurement consistency when the identical load is repeatedly deposited and removed under invariant conditions.
* **How It Works**: Tracks 10 consecutive load applications across two distinct operational ranges: Series A at $\sim 50\%\text{ Max}$ ($7,500\text{ g}$) and Series B at $100\%\text{ Max}$ ($15,000\text{ g}$). Computes the maximum reading spread:
  $$\Delta I = I_{\text{max}} - I_{\text{min}}$$
  Asserts that $\Delta I \le |\text{MPE}|$ for that load bracket.
* **Why It Is Needed**: Required by **OIML R 76-1 Clause 3.6.1** to detect mechanical creep, hysteresis friction, temperature coefficient drift, or load-cell zero-point instability.
* **Where It Is Used**: Production quality assurance and laboratory pattern approval testing.

---

### 5. Form 15: Software Examination (WELMEC 7.2)
![Form 15: Software Examination](docs/screenshots/05_form15_software_examination_welmec.png)

* **Name**: `Form 15: Legally Relevant Software (LRS) Examination`
* **Work**: Validates software separation, checksums, audit counters, and tamper sealing to ensure that metrological firmware cannot be altered to shortchange consumers.
* **How It Works**: Performs real-time runtime hashing of the metrological kernel (`nawi_engine.py`) using SHA-256 and CRC-32 algorithms (`CRC-32: 653BB67C`). Compares against the factory certified baseline and verifies WELMEC Guide 7.2 Extension L (Long-term storage) & Extension U (Software update) checklists.
* **Why It Is Needed**: Enforces **OIML R 76-1 Clause 5.5** and **WELMEC 7.2**. Prevents unauthorized firmware flashing or fraudulent calibration offsets from being embedded into trading scales.
* **Where It Is Used**: Type examination laboratories and government cybersecurity audits.

---

### 6. Interactive Statutory MPE Trumpet Envelope Curve
![MPE Trumpet Curve](docs/screenshots/06_mpe_trumpet_envelope_curve.png)

* **Name**: `Statutory MPE Trumpet Corridor Chart (OIML R 76-1 Table 6)`
* **Work**: Provides real-time visual cartography of test observations against the legal statutory error corridor.
* **How It Works**: 
  - Renders stepped tolerance boundaries:
    - **Bracket 1 ($0 \le m \le 500e$)**: $\text{MPE} = \pm 0.5e = \pm 2.5\text{ g}$
    - **Bracket 2 ($500e < m \le 2000e$)**: $\text{MPE} = \pm 1.0e = \pm 5.0\text{ g}$
    - **Bracket 3 ($2000e < m \le \text{Max}$)**: $\text{MPE} = \pm 1.5e = \pm 7.5\text{ g}$
  - Overlays ascending and descending measurement points in real-time. Any point breaching the corridor is highlighted in bright red as a failing violation.
* **Why It Is Needed**: Prevents human misinterpretation of stepped tabular error limits and gives metrologists instant graphical confirmation of scale linearity.
* **Where It Is Used**: Visual laboratory display and executive jury demonstrations.

---

### 7. Batch CSV Ingestion Engine
![Batch CSV Ingestion Engine](docs/screenshots/07_batch_csv_ingestion_engine.png)

* **Name**: `Batch CSV Ingestion & Data Logger Import Engine`
* **Work**: Enables rapid batch ingestion of test measurements from legacy RS-232 serial dumps, automated calibration rigs, or standardized spreadsheets.
* **How It Works**: Parses multi-line CSV streams (`step_index, load, indication, delta_l, direction`), validates data types against Pydantic schemas, routes records to the appropriate test form, and recalculates turning points and error envelopes atomically in SQLite WAL mode.
* **Why It Is Needed**: Eliminates tedious manual re-entry of data collected from automated test rigs or benchtop calibration hardware.
* **Where It Is Used**: High-throughput industrial scale manufacturing lines and calibration testing houses.

---

### 8. ISO 19005-3 PDF/A-3 & PTB DCC v3.2.1 Verifier
![PDF/A-3 & PTB DCC Verifier](docs/screenshots/08_pdfa3_ptb_dcc_verifier.png)

* **Name**: `ISO 19005-3 PDF/A-3 Container & PTB DCC XML Offline Verifier`
* **Work**: Inspects digital calibration certificate containers, extracts embedded XML datasets, and validates cryptographic seals without an internet connection.
* **How It Works**: 
  - Parses the PDF/A-3 catalog to extract embedded files (`/EmbeddedFiles`).
  - Validates the embedded **PTB DCC v3.2.1** XML schema conforming to Physikalisch-Technische Bundesanstalt standards.
  - Verifies the RFC 8032 Ed25519 digital signature against the public key fingerprint. Includes a **"Simulate Tampered PDF"** button to prove that modifying even 1 byte invalidates the seal.
* **Why It Is Needed**: Conforms to **ISO 19005-3:2012** and **CIPM-MRA** guidelines for machine-readable digital calibration certificates (DCC) suitable for international trade cross-recognition.
* **Where It Is Used**: Third-party verification audits, customs checkpoints, and inter-laboratory peer reviews.

---

### 9. Legal Metrology Review & Formal Certification
![Legal Metrology Review & Certification](docs/screenshots/09_legal_metrology_review_certification.png)

* **Name**: `Legal Metrology Review & Formal Certification Workflow`
* **Work**: Guides the inspector through formal regulatory review, mandatory review comments, completeness gating, and certificate issuance.
* **How It Works**: Enforces **Regulatory Completeness Gating** (verifies that Form 1, Form 3, Form 5, and Form 15 are 100% filled and passing). Prompts the reviewer for credentials (`SCIENTIST_DR_SHARMA`), records formal comments, and executes atomic state transition.
* **Why It Is Needed**: Mandated by **ISO/IEC 17025 Clause 7.8.2** to prevent incomplete, premature, or unauthorized calibration reports from entering legal circulation.
* **Where It Is Used**: Official issuance desk of the Legal Metrology Division.

---

### 10. Anti-Rollback Lifecycle & Revision Audit Trail
![Anti-Rollback Revision Audit Trail](docs/screenshots/10_anti_rollback_revision_audit_trail.png)

* **Name**: `ISO/IEC 17025 Anti-Rollback Revision Audit Trail & Invalidation Engine`
* **Work**: Prevents silent record tampering. Any attempt to modify an observation in an approved report immediately triggers invalidation, mandates an amendment reason, increments the revision number, and preserves superseded snapshots permanently.
* **How It Works**: 
  1. Once Revision 1 is locked and certified, all raw readings are frozen.
  2. If an operator amends a reading (e.g., at $2500\text{ g}$), the engine demands a mandatory technical justification reason.
  3. The system sets the report state to `REVOKED / DRAFT (Revision #2)` and flags all dependent calculations as `STALE`.
  4. The original Revision #1 PDF and state remain archived in an immutable ledger.
* **Why It Is Needed**: Strictly required under **ISO/IEC 17025:2017 Clause 7.10** (Nonconforming work) and **Clause 7.8.8** (Amendments to reports). Completely eliminates retrospective fraud.
* **Where It Is Used**: Regulatory compliance audits and forensic inspection investigations.

---

### 11. Generated Archival Artifacts & Ed25519 Offline QR Seal
![Generated Archival Artifacts & Ed25519 QR](docs/screenshots/11_archival_artifacts_ed25519_qr.png)

* **Name**: `Multi-Format Archival Artifacts & Offline Ed25519 QR Generator`
* **Work**: Generates three synchronized output artifacts upon test completion:
  1. **Print-optimized HTML Report** conforming to OIML R 76-2 forms 0 to 15.
  2. **Archival Vector PDF Report** with security headers and watermarks.
  3. **PTB DCC v3.2.1 XML** for automated calibration cloud sync.
  4. **High-Density Level H Offline QR Code**.
* **How It Works**: Compacts essential certificate metadata (Certificate ID, Issuer, Accuracy Class, Capacity, MPE Verdict, Turning Point Hash) into a CBOR/Base45 payload signed with a 64-byte Ed25519 asymmetric signature.
* **Why It Is Needed**: Allows instant verification in rural markets or shielded factory floors with **zero cellular connectivity**.
* **Where It Is Used**: Physical scale stamping stickers, verification certificates, and trading scale inspection labels.

---

### 12. Offline Field Inspector Verification Tool
![Offline Field Inspector Tool](docs/screenshots/12_offline_field_inspector_verifier.png)

* **Name**: `Offline Field Inspector Mobile Verification Engine`
* **Work**: Simulates the exact verification workflow performed by consumer protection officers on mobile phones or handheld terminals in the field.
* **How It Works**: Ingests the scanned QR JSON envelope, extracts claims (`iss`, `cert_id`, `sess_id`, `rev`), and verifies the asymmetric digital signature using the embedded public key without querying any remote server. Features a **"Simulate Forgery (Flip Verdict)"** test button demonstrating that altering a single character causes immediate signature failure.
* **Why It Is Needed**: Protects consumers against counterfeit verification certificates and cloned physical calibration seals.
* **Where It Is Used**: Market surprise inspections, mandi weight verifications, and highway weighbridge checks.

---

### 13. Collapsible Sidebar & Rapid Jury Demonstration Bar
![Collapsible Sidebar & Toolbar](docs/screenshots/13_responsive_sidebar_and_toolbar.png)

* **Name**: `Collapsible Ergonomic Sidebar & Rapid Jury Demonstration Toolbar`
* **Work**: Provides an intuitive, responsive navigation experience across all 8 workbench modules while offering a 1-click demonstration mode for hackathon juries and training seminars.
* **How It Works**: 
  - Left-hand collapsible rail provides instant access to OIML Testing, Tools, and Governance modules.
  - Top action bar includes the **"⚡ Load Winning Pitch Data (F1, F3, F5, F15)"** button, which pre-loads a complete, mathematically pristine Class III Essae DS-852 test scenario in under 200 milliseconds.
* **Why It Is Needed**: Maximizes screen estate on rugged touchscreens and allows examiners to inspect the complete multi-form workflow without manually typing 50 data points.
* **Where It Is Used**: Live presentations, hackathon jury defenses, and training workshops for metrology inspectors.

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
├── docs/
│   └── screenshots/                   # High-resolution architectural screenshots
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
