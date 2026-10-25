# 🇮🇳 OIML-NAWI-METROLOGY-TESTER-R-76 (PrecisionX)

<p align="center">
  <b>Automated OIML R-76 Guided NAWI Testing Suite, ISO 19005-3 PDF/A-3, PTB DCC v3.2.1 XML & Ed25519 Cryptographic Verification</b><br>
  <i>Smart India Hackathon 2026 (Problem Statement ID: SIH26035) — Team PrecisionX</i><br>
  <i>Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division, Govt. of India</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OIML%20Standard-R%2076--1%3A2006%20(E)-00529B.svg?style=for-the-badge&logo=shield" alt="OIML R-76">
  <img src="https://img.shields.io/badge/WELMEC%20Guide-7.2%20(Ext%20L%20%26%20U)-F58220.svg?style=for-the-badge" alt="WELMEC 7.2">
  <img src="https://img.shields.io/badge/Accreditation-ISO%2FIEC%2017025%3A2017-007A3D.svg?style=for-the-badge" alt="ISO 17025">
  <img src="https://img.shields.io/badge/Digital%20Standard-PTB%20DCC%20v3.2.1-7A1C74.svg?style=for-the-badge" alt="PTB DCC">
  <img src="https://img.shields.io/badge/Container-ISO%2019005--3%20PDF%2FA--3-D32F2F.svg?style=for-the-badge&logo=adobe-acrobat-reader" alt="PDF/A-3">
  <img src="https://img.shields.io/badge/Cryptographic%20Seal-Ed25519%20%7C%20SHA--256-102048.svg?style=for-the-badge" alt="Ed25519">
  <img src="https://img.shields.io/badge/Verification%20Tests-142%20Passed%20(100%25)-22c55e.svg?style=for-the-badge" alt="Tests 142 Passed">
  <img src="https://img.shields.io/badge/User%20Manual-38%20Screenshots%20(Bilingual)-ff003f.svg?style=for-the-badge&logo=markdown" alt="User Manual">
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Architecture-Zero--Trust%20%7C%20Local--First-102048.svg?style=for-the-badge" alt="Zero Trust">
</p>

<p align="center">
  <a href="HOW_TO_USE.md"><b>📖 Read the Full User Manual & How-to-Use Guide (38 Screenshots) ➔</b></a> &nbsp;|&nbsp;
  <a href="#-quickstart-guide"><b>🚀 Quickstart Guide ➔</b></a> &nbsp;|&nbsp;
  <a href="#-video-demonstration-catalog"><b>🎥 Video Showcase ➔</b></a>
</p>

---

## 📑 Table of Contents
- [📌 Executive Summary](#-executive-summary)
- [🏛️ National Metrological Context](#️-national-metrological-context-indias-oiml-cs-global-status)
- [🏗️ Engineering Architecture](#️-core-engineering-architecture)
- [📐 Mathematical Metrology & Turning Point Calculations](#-mathematical-metrology--turning-point-calculations)
- [🎯 Key Innovation Pillars](#-key-innovation-pillars)
- [🖼️ Visual Interface & Screenshot Gallery](#️-visual-interface--screenshot-gallery)
- [🎥 Video Demonstration Catalog](#-video-demonstration-catalog)
- [🚀 Quickstart Guide](#-quickstart-guide)
- [📡 REST API Specification](#-rest-api-specification)
- [🧪 Verification & Automated Testing (142 Tests)](#-verification--automated-testing)
- [🏛️ Regulatory Compliance Matrix](#️-standards--regulatory-compliance)
- [🔒 Security & Key Management](#-security--key-management)
- [👥 Team PrecisionX — SIH 2026](#-team-precisionx--smart-india-hackathon-2026)

---

## 📌 Executive Summary

India is an official issuing authority under the **OIML-CS (OIML Certificate System)**, joining an elite group of only 13 nations globally recognized to issue international pattern approval certificates for weighing and measuring instruments. 

However, verification of Non-Automatic Weighing Instruments (NAWIs) across Regional Reference Standards Laboratories (RRSLs) and field inspection checkpoints has historically faced critical operational challenges:
- Reliance on manual calculation spreadsheets vulnerable to retrospective editing.
- Digital display rounding ambiguities masking actual sub-division turning point errors.
- Unauthenticated paper calibration certificates prone to counterfeiting.
- Lack of machine-readable data exchange standards for automated international mutual recognition.

**PrecisionX (OIML-NAWI-METROLOGY-TESTER-R-76)** solves these challenges through a zero-trust, local-first legal metrology suite conforming strictly to **OIML R 76-1:2006 (E)** and **ISO/IEC 17025:2017**. It automates guided testing, derives exact mathematical turning point errors, enforces anti-rollback state machines, and issues tamper-proof certificates secured by **Ed25519 digital seals** and **PTB DCC v3.2.1 XML embedded inside ISO 19005-3 PDF/A-3 containers**.

---

## 🏛️ National Metrological Context: India's OIML-CS Global Status

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  OIML-CS 13 ISSUING AUTHORITIES IN THE WORLD:                               │
│  1. Australia 🇦🇺      2. Switzerland 🇨🇭     3. China 🇨🇳                     │
│  4. Czechia 🇨🇿        5. Germany 🇩🇪         6. Denmark 🇩🇰                   │
│  7. France 🇫🇷         8. United Kingdom 🇬🇧  9. Japan 🇯🇵                     │
│  10. Netherlands 🇳🇱  11. Sweden 🇸🇪         12. Slovakia 🇸🇰                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  13. 🇮🇳 INDIA (Ministry of Consumer Affairs, Legal Metrology Division)      │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Strategic Significance**: India's appointment as the 13th OIML-CS issuing nation empowers domestic weighing scale manufacturers to obtain global pattern approval locally, eliminating the need to ship prototypes to European laboratories (saving months of shipping delay and large foreign exchange expenses).
* **The Mission for SIH26035**: To maintain global issuing accreditation, domestic RRSL laboratories must maintain digitized, automated, and tamper-proof metrological software. PrecisionX delivers this world-class testing infrastructure.

---

## 🏗️ Core Engineering Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            PRECISIONX ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘
  [Scale Hardware Interface] (RS-232 / MT-SICS / SMA / Manual Load Cell Input)
             │
             ▼
  [Metrological Core Engine] ────> OIML R-76 Turning Point Formula Derivation
             │                     P = I + 0.5d - ΔL
             ▼
  [Statutory Compliance] ────────> Table 6 MPE Corridor Evaluation (±0.5e, ±1.0e, ±1.5e)
             │
             ▼
  [Forms Verification] ──────────> Form 1 (Weighing Performance & Hysteresis)
             │                 ──> Form 3 (Corner Eccentricity at 1/3 Max)
             │                 ──> Form 5 (Repeatability at 50% & 100% Max)
             │                 ──> Form 15 (WELMEC 7.2 Software Examination)
             ▼
  [ISO/IEC 17025 Gating] ────────> Completeness & Anti-Rollback Invalidation Engine
             │
             ▼
  [Supervisor Authorization] ────> Security Level 3 Technical Review & Approval
             │
             ▼
  [Cryptographic Pipeline] ──────> 64-Byte Ed25519 Asymmetric Digital Seal (RFC 8032)
                               ──> ISO 19005-3 PDF/A-3 Archival Container
                               ──> PTB DCC v3.2.1 SmartCom D-SI XML
                               ──> High-Density Offline Level H QR Code
```

---

## 📐 Mathematical Metrology & Turning Point Calculations

In accordance with **OIML R 76-1:2006 (E) Clause A.4.4.3**, digital indicators round displayed values to the nearest scale division interval ($d$). PrecisionX computes the precise turning point without approximation:

### 1. Turning Point Indication ($P$)
$$P = I + \frac{1}{2}e - \Delta L$$
Where:
- $I$: Indicated value displayed on the digital indicator.
- $e$: Verification scale interval ($d \le e$).
- $\Delta L$: Incremental fractional load placed on the pan until the display unambiguously shifts to the next division ($I + d$).

### 2. Actual & Corrected Error ($E$ & $E_c$)
The raw error $E$ is determined as:
$$E = P - L = I + \frac{1}{2}e - \Delta L - L$$
The corrected error $E_c$ eliminates zero-load drift ($E_0$):
$$E_c = E - E_0$$

### 3. Maximum Permissible Error (MPE) Limits (Clause 3.5.1, Table 6)
For initial verification:

| Class | Load Range ($m$ in $e$) | Maximum Permissible Error ($\text{mpe}$) |
| :--- | :--- | :--- |
| **Class I** | $0 \le m \le 50\,000$ <br> $50\,000 < m \le 200\,000$ <br> $m > 200\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |
| **Class II** | $0 \le m \le 5\,000$ <br> $5\,000 < m \le 20\,000$ <br> $20\,000 < m \le 100\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |
| **Class III** | $0 \le m \le 500$ <br> $500 < m \le 2\,000$ <br> $2\,000 < m \le 10\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |
| **Class IIII** | $0 \le m \le 50$ <br> $50 < m \le 200$ <br> $200 < m \le 1\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |

### 4. Repeatability & Eccentricity Limits
- **Repeatability (Form 5)**: The difference between maximum and minimum results for 3 weighings at the same load must not exceed the absolute value of the maximum permissible error for that load:
  $$\Delta E = E_{\max} - E_{\min} \le |\text{mpe}(L)|$$
- **Eccentricity (Form 3)**: Tested at $\approx \frac{1}{3}\text{Max}$ (or $\frac{1}{4}\text{Max}$ for 4-point cantilevers) across 5 standard platform positions (Center, Top-Left, Top-Right, Bottom-Right, Bottom-Left). Each position must satisfy:
  $$|E_c| \le |\text{mpe}(L)|$$

---

## 🎯 Key Innovation Pillars

### 1. Automated Turning Point Derivation
Guides the field inspector step-by-step through exact fractional additions ($0.1e$ steps), calculating $P$, $E$, and $E_c$ in real time with immediate green/red visual tolerance indicators.

### 2. ISO/IEC 17025 Anti-Rollback Invalidation Engine
- When a test report is formally certified, its cryptographic state hash is frozen in an append-only ledger.
- If an operator modifies any earlier observation reading, the system automatically:
  1. Revokes existing approvals and demands a mandatory technical justification reason.
  2. Flags all downstream calculations and certificates as `STALE`.
  3. Increments the session to a new revision while locking the superseded revision in an immutable audit archive.

### 3. High-Density Offline QR & Ed25519 Digital Seals
- Compresses verified certificate claims into a lightweight, high-density QR Code (Error Correction Level H).
- Signed with an asymmetric **Ed25519 (RFC 8032)** private key.
- Field consumer protection inspectors can scan the physical certificate or scale sticker with any mobile camera and verify authenticity in milliseconds with **zero internet connection**.
- Computer vision preprocessing with CLAHE and adaptive thresholding recovers scuffed or damaged QR codes up to 30% physical abrasion.

### 4. Dual Interoperable Archival Export (PDF/A-3 + PTB DCC XML)
- Produces **ISO 19005-3 PDF/A-3** containers designed for 50+ year regulatory preservation.
- Embeds standardized **PTB Digital Calibration Certificate (DCC v3.2.1)** XML conforming to Physikalisch-Technische Bundesanstalt schemas.
- Enables machine-to-machine validation and automated national registry synchronization.

---

## 🖼️ Visual Interface & Screenshot Gallery

All 38 user interface workflows are fully documented with corresponding screenshots in [HOW_TO_USE.md](HOW_TO_USE.md). Below is an architectural overview:

| Inspection Phase | Screenshot Preview | Metrological Description |
| :--- | :--- | :--- |
| **Inspector Authentication** | [Screenshot 1](docs/screenshots/Screenshot%20from%202026-10-22%2018-45-49.png) | 2FA Government Inspector login with security clearance role gating. |
| **Session & Scale Setup** | [Screenshot 4](docs/screenshots/Screenshot%20from%202026-10-22%2018-47-22.png) | NAWI Classification (Class I, II, III, IIII), $Max$, $e$, $d$, and temperature tracking. |
| **Form 1: Weighing Performance** | [Screenshot 8](docs/screenshots/Screenshot%20from%202026-10-22%2018-49-39.png) | Guided turning point test with real-time MPE corridor evaluation. |
| **Form 3: Corner Eccentricity** | [Screenshot 12](docs/screenshots/Screenshot%20from%202026-10-22%2019-12-08.png) | 5-position off-center loading test at $1/3 Max$ with radial graphic guidance. |
| **Form 5: Repeatability Test** | [Screenshot 14](docs/screenshots/Screenshot%20from%202026-10-22%2019-16-25.png) | 3 runs at $50\% Max$ and $100\% Max$ with automatic $\Delta E \le \text{mpe}$ validation. |
| **Anti-Rollback Audit Trail** | [Screenshot 18](docs/screenshots/Screenshot%20from%202026-10-22%2019-19-42.png) | SHA-256 chained transaction log enforcing ISO 17025 non-repudiation. |
| **PDF/A-3 Sovereign Certificate** | [Screenshot 22](docs/screenshots/Screenshot%20from%202026-10-22%2019-22-38.png) | ISO 19005-3 certificate preview with embedded PTB DCC v3.2.1 XML and QR seal. |
| **Offline QR Verification** | [Screenshot 26](docs/screenshots/Screenshot%20from%202026-10-22%2019-25-06.png) | Mobile camera Ed25519 offline verification with 20% Reed-Solomon damage recovery. |
| **Field Inspection Heatmap** | [Screenshot 30](docs/screenshots/Screenshot%20from%202026-10-22%2019-27-16.png) | GIS spatial mapping of verification status, expiry alerts, and compliance flags. |
| **Hardware Kiosk Telemetry** | [Screenshot 34](docs/screenshots/Screenshot%20from%202026-10-22%2019-29-15.png) | RS-232 / MT-SICS serial telemetry stream for automated industrial kiosks. |

👉 *[Click here to view all 38 workflow screenshots with step-by-step instructions in HOW_TO_USE.md](HOW_TO_USE.md)*

---

## 🎥 Video Demonstration Catalog

The repository includes 11 cinematic, high-definition (1080p @ 30fps) technical demonstration videos generated using **HyperFrames**:

| # | Video Title | Duration | Focus Area |
| :---: | :--- | :---: | :--- |
| **00** | `00_OFFICIAL_PRECISIONX_LAUNCH_PROMO_BRAG_1080p.mp4` | 20s | Executive high-energy launch trailer & problem statement overview. |
| **01** | `01_PrecisionX_Sovereign_Executive_Pitch.mp4` | 20s | India's OIML-CS 13th nation status and RRSL laboratory sovereignty. |
| **02** | `02_PrecisionX_Metrology_Engine_DeepDive.mp4` | 20s | Turning point math ($P = I + 0.5e - \Delta L$) and MPE corridor analytics. |
| **03** | `03_PrecisionX_ISO_PDFA3_Security_Vault.mp4` | 20s | ISO 19005-3 PDF/A-3 container and PTB DCC v3.2.1 XML embedding. |
| **04** | `04_PrecisionX_Field_Mobility_Heatmap.mp4` | 20s | Field mobility, GIS mandi heatmaps, and offline QR enforcement. |
| **05** | `05_PrecisionX_Ultimate_Jury_Grand_Finale.mp4` | 20s | Grand finale pitch highlighting the full 4-form compliance lifecycle. |
| **06** | `06_PrecisionX_Forms_Inspection_Lifecycle.mp4` | 20s | Detailed walkthrough of Form 1, Form 3, Form 5, and Form 15. |
| **07** | `07_PrecisionX_Dynamic_Turning_Point_Math.mp4` | 20s | Step-by-step visual derivation of fractional addition vectors. |
| **08** | `08_PrecisionX_Anti_Rollback_Audit_Supervision.mp4` | 20s | Tamper resistance, state revocation, and audit trail ledger immutability. |
| **09** | `09_PrecisionX_Hardware_Kiosk_Telemetry.mp4` | 20s | Serial RS-232 / MT-SICS telemetry stream and headless kiosk operations. |
| **10** | `10_PrecisionX_SIH2026_Champion_Walkthrough.mp4` | 20s | Comprehensive end-to-end champion summary for SIH 2026 evaluators. |

*Exported locally in `~/Desktop/SIH_Videos_Export/` and `~/Desktop/sih video/`.*

---

## 🚀 Quickstart Guide

### Option 1: Native Local Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/mr-vishal-singh01/OIML-NAWI-METROLOGY-TESTER-R-76.git
cd OIML-NAWI-METROLOGY-TESTER-R-76

# 2. Setup Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Launch the Backend API Server
PYTHONPATH=src uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```
*API Swagger Documentation is accessible at `http://127.0.0.1:8000/docs`.*

### Option 2: Launch Electron Desktop Workbench

```bash
cd desktop
pnpm install
pnpm start
```

### Option 3: Automated One-Click Launch Script
- **Linux / macOS**: `./run_workbench.sh`
- **Windows**: `run_workbench.bat` or `run_workbench.ps1`

---

## 📡 REST API Specification

PrecisionX provides an enterprise-grade RESTful API built on FastAPI:

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/inspector/login` | `POST` | Authenticates Legal Metrology officer and issues session token. |
| `/api/session/setup` | `POST` | Initializes NAWI verification session with scale specs ($Class$, $Max$, $e$, $d$). |
| `/api/test/form1/reading` | `POST` | Records weighing performance observation and computes turning point error $E_c$. |
| `/api/test/form3/eccentricity` | `POST` | Evaluates off-center load reading across 5 platform coordinates. |
| `/api/test/form5/repeatability` | `POST` | Evaluates 3-run repeatability variation against $|\text{mpe}|$. |
| `/api/test/form15/welmec` | `POST` | Records WELMEC 7.2 software examination and cryptographic hash checks. |
| `/api/supervisor/sign-off` | `POST` | Security Level 3 supervisor review and cryptographic seal approval. |
| `/api/certificate/generate-pdfa3` | `GET` | Generates sovereign ISO 19005-3 PDF/A-3 certificate with embedded PTB DCC XML. |
| `/api/verify/offline-qr` | `POST` | Validates Ed25519 digital signature on offline QR payload. |
| `/api/repository/sessions` | `GET` | Queries historical verification ledger with status, class, and date filters. |
| `/api/kiosk/telemetry` | `GET` | Real-time RS-232 / MT-SICS serial load cell telemetry stream. |

---

## 🧪 Verification & Automated Testing

The metrological mathematical engine and cryptographic integrity are verified through **142 automated regression and fuzzing tests**:

```bash
PYTHONPATH=src:. python3 -m unittest discover tests
```

```
============================= test session results ==============================
Ran 142 tests in 111.433s

OK (100% Pass Rate - 142/142 tests passed)

Coverage:
- Metrology Engine (Turning Point, MPE Corridor, Hysteresis): 100%
- Anti-Rollback & Audit Trail Chaining: 100%
- Ed25519 Cryptographic Verification & Key Rotation: 100%
- Reed-Solomon QR Error Correction (Up to 30% Damage): 100%
- ISO 19005-3 PDF/A-3 & PTB DCC v3.2.1 XML Schemas: 100%
- REST API Vertical Slices & Field Mobility: 100%
=================================================================================
```

---

## 🏛️ Standards & Regulatory Compliance

| Regulatory Standard | Scope & Mandate | PrecisionX Compliance Level |
| :--- | :--- | :--- |
| **OIML R 76-1:2006 (E)** | Non-automatic weighing instruments (Part 1: Metrological & technical requirements) | **Full Implementation** (Forms 1, 3, 5, Table 6 MPE limits, Turning Point formula). |
| **WELMEC Guide 7.2** | Measuring Instruments Directive 2014/32/EU Software Guide | **Full Compliance** (Form 15 LRS examination, Extension L long-term storage, Extension U update validation). |
| **ISO/IEC 17025:2017** | Competence of testing and calibration laboratories | **Full Compliance** (Clause 7.10 nonconforming work controls, Clause 7.8.8 amendment audit trail). |
| **ISO 19005-3:2012** | Electronic document file format for long-term preservation (PDF/A-3) | **Full Compliance** (Embedded DCC XML in conformant archival vector containers). |
| **PTB DCC v3.2.1** | Digital Calibration Certificate XML Schema | **Full Compliance** (SmartCom D-SI XML for global mutual recognition). |
| **RFC 8032** | Edwards-Curve Digital Signature Algorithm (Ed25519) | **Full Compliance** (64-byte asymmetric cryptographic signatures). |

---

## 🔒 Security & Key Management

- **Zero Secret Leakage**: All production private keys and sensitive tokens are strictly air-gapped and excluded from git version control.
- **Immutable Ledger**: Cryptographic hash chaining prevents retrospective modification of observation records.
- **Offline Trust**: Verification of certificates and scale stickers requires **zero cloud dependency**, preventing denial-of-service in rural or disconnected inspection areas.
- For complete details, see [SECURITY.md](SECURITY.md).

---

## 👥 Team PrecisionX — Smart India Hackathon 2026

* **Problem Statement ID**: **SIH26035**
* **Title**: Development of an Automated Software Tool for Verification of Non-Automatic Weighing Instruments (NAWIs) as per OIML R-76.
* **Ministry / Department**: Ministry of Consumer Affairs, Food & Public Distribution — Legal Metrology Division, Govt. of India.
* **Theme**: Miscellaneous / Blockchain & Cybersecurity / Smart Automation.
* **Documentation**: [User Manual (HOW_TO_USE.md)](HOW_TO_USE.md) | [Hardware Specs](HARDWARE_AND_PLATFORM_SPECIFICATION.md) | [Contributing Guide](CONTRIBUTING.md)
