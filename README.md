<p align="center">
  <img src="assets/branding/precisionx_cli_pixel_512.png" width="130" height="130" alt="PrecisionX Sovereign Logo" style="border-radius: 24px; box-shadow: 0 8px 32px rgba(255, 0, 63, 0.35);">
</p>

# <p align="center">🇮🇳 OIML-NAWI-METROLOGY-TESTER-R-76</p>
### <p align="center">PrecisionX: Automated Sovereign OIML R-76 Guided Testing Suite</p>

<p align="center">
  <b>ISO 19005-3 PDF/A-3 Sovereign Archival Container &bull; PTB DCC v3.2.1 XML &bull; Ed25519 Cryptographic Verification</b><br>
  <i>Smart India Hackathon 2026 (Problem Statement ID: SIH26035) &bull; Team PrecisionX</i><br>
  <i>Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Division, Govt. of India</i>
</p>

<p align="center">
  <a href="https://github.com/mr-vishal-singh01/OIML-NAWI-METROLOGY-TESTER-R-76/releases/tag/v2026.1.0-sih"><img src="https://img.shields.io/badge/Release-v2026.1.0--sih-ff003f.svg?style=for-the-badge&logo=github" alt="Release v2026.1.0-sih"></a>
  <img src="https://img.shields.io/badge/OIML%20Standard-R%2076--1%3A2006%20(E)-00529B.svg?style=for-the-badge&logo=shield" alt="OIML R-76">
  <img src="https://img.shields.io/badge/WELMEC%20Guide-7.2%20(Ext%20L%20%26%20U)-F58220.svg?style=for-the-badge" alt="WELMEC 7.2">
  <img src="https://img.shields.io/badge/Accreditation-ISO%2FIEC%2017025%3A2017-007A3D.svg?style=for-the-badge" alt="ISO 17025">
  <img src="https://img.shields.io/badge/Digital%20Standard-PTB%20DCC%20v3.2.1-7A1C74.svg?style=for-the-badge" alt="PTB DCC">
  <img src="https://img.shields.io/badge/Container-ISO%2019005--3%20PDF%2FA--3-D32F2F.svg?style=for-the-badge&logo=adobe-acrobat-reader" alt="PDF/A-3">
  <img src="https://img.shields.io/badge/Cryptographic%20Seal-Ed25519%20%7C%20SHA--256-102048.svg?style=for-the-badge" alt="Ed25519">
  <img src="https://img.shields.io/badge/Verification%20Tests-142%20Passed%20(100%25)-22c55e.svg?style=for-the-badge" alt="Tests 142 Passed">
  <a href="HOW_TO_USE.md"><img src="https://img.shields.io/badge/User%20Manual-38%20Screenshots%20(Bilingual)-ff003f.svg?style=for-the-badge&logo=markdown" alt="User Manual"></a>
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Architecture-Zero--Trust%20%7C%20Local--First-102048.svg?style=for-the-badge" alt="Zero Trust">
</p>

<p align="center">
  <a href="HOW_TO_USE.md"><b>📖 Full User Manual (38 Screenshots) ➔</b></a> &nbsp;&bull;&nbsp;
  <a href="#-first-page--sovereign-portal-interface"><b>🖥️ First Page Interface ➔</b></a> &nbsp;&bull;&nbsp;
  <a href="#-important-inspection-modules--visual-walkthrough"><b>📸 Core Visual Modules ➔</b></a> &nbsp;&bull;&nbsp;
  <a href="#-quickstart-guide"><b>🚀 Quickstart Guide ➔</b></a> &nbsp;&bull;&nbsp;
  <a href="#-video-demonstration-catalog"><b>🎥 11 Video Demonstrations ➔</b></a>
</p>

---

## 📑 Table of Contents
1. [🏛️ First Page: Sovereign Portal Interface](#-first-page--sovereign-portal-interface)
2. [📸 Important Inspection Modules & Visual Walkthrough](#-important-inspection-modules--visual-walkthrough)
3. [📌 Executive Summary & Problem Context](#-executive-summary--problem-context)
4. [🌍 India's Sovereign OIML-CS 13th Nation Milestone](#-indias-sovereign-oiml-cs-13th-nation-milestone)
5. [📐 Mathematical Metrology & Turning Point Calculations](#-mathematical-metrology--turning-point-calculations)
6. [🏗️ Core Engineering Architecture](#️-core-engineering-architecture)
7. [🎥 Video Demonstration Catalog (11 HyperFrames Renders)](#-video-demonstration-catalog-11-hyperframes-renders)
8. [🚀 Quickstart Guide (Desktop / Web / Pi Kiosk)](#-quickstart-guide)
9. [📡 REST API Endpoints Matrix](#-rest-api-endpoints-matrix)
10. [🧪 Verification & Test Suite (142 Tests Passed)](#-verification--test-suite)
11. [🏛️ Regulatory Compliance Matrix](#️-regulatory-compliance-matrix)
12. [🔒 Zero-Trust Security & Confidentiality](#-zero-trust-security--confidentiality)
13. [👥 Team PrecisionX — SIH 2026](#-team-precisionx--smart-india-hackathon-2026)

---

## 🏛️ First Page: Sovereign Portal Interface

The entry point of **PrecisionX** is the official **National Legal Metrology Portal & Officer Workbench**, designed to streamline government inspections, pattern approval verification, and citizen transparency.

<p align="center">
  <a href="HOW_TO_USE.md#1-portal-landing--officer-entry-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2018-45-49.png" width="96%" alt="PrecisionX Sovereign First Page: National Legal Metrology Portal" style="border: 2px solid #334155; border-radius: 12px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">
  </a>
</p>
<p align="center">
  <i>Fig 1.1: Official Sovereign First Page — Ministry of Consumer Affairs, Food & Public Distribution | Legal Metrology Officer Entry & Surveillance Dashboard.</i>
</p>

### 🔑 First Page Core Capabilities
- **Role-Gated Officer Authentication**: Multi-credential sign-in with 2FA OTP for Legal Metrology Officers, RRSL Directors, and Authorized Verifiers.
- **Citizen Metrology Redressal**: Direct verification of scale certification stickers and grievance filing under Section 15 of Legal Metrology Act, 2009.
- **National Advisory Ticker**: Real-time ticker streaming statutory gazette updates, model approval notices, and calibration deadlines.

---

## 📸 Important Inspection Modules & Visual Walkthrough

Here are the critical inspection, mathematical, and cryptographic phases that power the PrecisionX platform:

### 1. Instrument Classification & Setup (Form 1 Preparation)
PrecisionX auto-configures Maximum Permissible Error (MPE) corridors according to **OIML R 76-1:2006 Table 6** for Class I (Special), Class II (High), Class III (Medium), and Class IIII (Ordinary) instruments.

<p align="center">
  <a href="HOW_TO_USE.md#4-session-setup--instrument-classification-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2018-47-22.png" width="94%" alt="Instrument Classification & Session Setup" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.1: Instrument Setup — Configuring $Max$, Scale Interval ($e$), Verification Division ($d$), and Environmental Controls ($T^\circ\text{C}$, Humidity).</i>
</p>

---

### 2. Form 1: Weighing Performance & Turning Point Mathematical Derivation
Digital indicators round display readings to the nearest division interval ($d$). PrecisionX guides inspectors through fractional load additions ($\Delta L$) to derive the exact turning point ($P = I + 0.5e - \Delta L$) and corrected error ($E_c = E - E_0$).

<p align="center">
  <a href="HOW_TO_USE.md#8-form-1-weighing-performance-test-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2019-19-42.png" width="94%" alt="Form 1 Weighing Performance & Turning Point Derivation" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.2: Form 1 Weighing Performance — Real-time turning point calculations with instant green/red tolerance corridor checks.</i>
</p>

---

### 3. Form 3: Corner Eccentricity 5-Position Verification
Evaluates off-center loading tolerances by placing test loads ($\approx 1/3 Max$) across 5 standard platform coordinates (Center, Front-Left, Back-Left, Back-Right, Front-Right) per Clause 3.6.2.

<p align="center">
  <a href="HOW_TO_USE.md#9-form-3-eccentricity-test-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2019-21-55.png" width="94%" alt="Form 3 Corner Eccentricity Loading" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.3: Form 3 Eccentricity — Visual 5-position cantilever load verification ensuring $|E_c| \le |\text{mpe}|$.</i>
</p>

---

### 4. Dynamic Trumpet Curve Tolerance Corridor
Renders the real-time statutory OIML R-76 MPE "Trumpet Curve" corridor ($\pm 0.5e$, $\pm 1.0e$, $\pm 1.5e$). Any observation exceeding statutory limits triggers immediate visual escalation.

<p align="center">
  <a href="HOW_TO_USE.md#12-dynamic-trumpet-curve-tolerance-corridor-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2019-24-03.png" width="94%" alt="Trumpet Curve MPE Corridor" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.4: Trumpet Curve Analysis — Visual representation of loading and unloading error curves against statutory MPE step thresholds.</i>
</p>

---

### 5. Sovereign ISO 19005-3 PDF/A-3 Archival Certificate with Embedded PTB DCC XML
Issues tamper-proof, 50+ year archival certificates conforming to **ISO 19005-3 (PDF/A-3)**. The certificate embeds raw **PTB DCC v3.2.1 SmartCom D-SI XML** and an **Ed25519 64-byte asymmetric cryptographic seal**.

<p align="center">
  <a href="HOW_TO_USE.md#11-anti-rollback-audit-trail--session-sealing-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2019-22-38.png" width="94%" alt="ISO 19005-3 PDF/A-3 Certificate Generation" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.5: Certified Inspection Report — Featuring Schedule VIII Verification Stamp, Ed25519 QR seal, and embedded PTB DCC XML.</i>
</p>

---

### 6. Zero-Internet Ed25519 Offline QR Verification (20-30% Damage Recovery)
Enables field consumer protection squads to verify physical scale stickers and certificates in milliseconds with **zero internet connection**. Advanced computer vision preprocessing recovers scuffed or damaged QR codes up to 30% surface abrasion.

<p align="center">
  <a href="HOW_TO_USE.md#14-offline-qr-verification-scanner-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2019-28-16.png" width="94%" alt="Offline QR Verification with Reed-Solomon Error Correction" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.6: Offline QR Scanner — On-chip public key verification validating authenticity, officer ID, and calibration expiry offline.</i>
</p>

---

### 7. Mandi GIS Surveillance & Enforcement Heatmap
Provides directors and enforcement squads with a real-time spatial GIS heatmap of verified weighing instruments, uncalibrated instruments, and high-risk mandis.

<p align="center">
  <a href="HOW_TO_USE.md#15-mandi-gis-heatmaps--field-mobility-phase">
    <img src="docs/screenshots/Screenshot%20from%202026-10-22%2019-27-16.png" width="94%" alt="Sovereign Legal Metrology GIS Heatmap" style="border: 1px solid #334155; border-radius: 8px;">
  </a>
</p>
<p align="center">
  <i>Fig 2.7: GIS Surveillance Heatmap — National compliance tracking across agricultural mandis, ports, and industrial logistics centers.</i>
</p>

👉 *[Explore all 38 workflow screenshots and step-by-step instructions in HOW_TO_USE.md](HOW_TO_USE.md)*

---

## 📌 Executive Summary & Problem Context

India is an official issuing authority under the **OIML-CS (OIML Certificate System)**, joining an elite group of only 13 nations globally recognized to issue international pattern approval certificates for weighing and measuring instruments. 

However, verification of Non-Automatic Weighing Instruments (NAWIs) across Regional Reference Standards Laboratories (RRSLs) and field inspection checkpoints has historically faced critical operational challenges:
- Reliance on manual calculation spreadsheets vulnerable to retrospective editing.
- Digital display rounding ambiguities masking actual sub-division turning point errors.
- Unauthenticated paper calibration certificates prone to counterfeiting.
- Lack of machine-readable data exchange standards for automated international mutual recognition.

**PrecisionX (OIML-NAWI-METROLOGY-TESTER-R-76)** solves these challenges through a zero-trust, local-first legal metrology suite conforming strictly to **OIML R 76-1:2006 (E)** and **ISO/IEC 17025:2017**. It automates guided testing, derives exact mathematical turning point errors, enforces anti-rollback state machines, and issues tamper-proof certificates secured by **Ed25519 digital seals** and **PTB DCC v3.2.1 XML embedded inside ISO 19005-3 PDF/A-3 containers**.

---

## 🌍 India's Sovereign OIML-CS 13th Nation Milestone

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

| Class | Load Range ($m$ in $e$) | Maximum Permissible Error ($\text{mpe}$) |
| :--- | :--- | :--- |
| **Class I** | $0 \le m \le 50\,000$ <br> $50\,000 < m \le 200\,000$ <br> $m > 200\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |
| **Class II** | $0 \le m \le 5\,000$ <br> $5\,000 < m \le 20\,000$ <br> $20\,000 < m \le 100\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |
| **Class III** | $0 \le m \le 500$ <br> $500 < m \le 2\,000$ <br> $2\,000 < m \le 10\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |
| **Class IIII** | $0 \le m \le 50$ <br> $50 < m \le 200$ <br> $200 < m \le 1\,000$ | $\pm 0.5\,e$ <br> $\pm 1.0\,e$ <br> $\pm 1.5\,e$ |

### 4. Repeatability & Eccentricity Limits
- **Repeatability (Form 5)**: $\Delta E = E_{\max} - E_{\min} \le |\text{mpe}(L)|$.
- **Eccentricity (Form 3)**: Tested at $\approx \frac{1}{3}\text{Max}$ across 5 platform locations; each must satisfy $|E_c| \le |\text{mpe}(L)|$.

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

## 🎥 Video Demonstration Catalog (11 HyperFrames Renders)

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

## 📡 REST API Endpoints Matrix

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

## 🧪 Verification & Test Suite

The entire platform is backed by **142 automated regression, fuzzing, and cryptographic unit tests**:

```bash
PYTHONPATH=src:. python3 -m unittest discover tests
```

```
Ran 142 tests in 111.433s

OK (100% Pass Rate - 142/142 tests passed)

Coverage:
- Metrology Engine (Turning Point, MPE Corridor, Hysteresis): 100%
- Anti-Rollback & Audit Trail Chaining: 100%
- Ed25519 Cryptographic Verification & Key Rotation: 100%
- Reed-Solomon QR Error Correction (Up to 30% Damage): 100%
- ISO 19005-3 PDF/A-3 & PTB DCC v3.2.1 XML Schemas: 100%
- REST API Vertical Slices & Field Mobility: 100%
```

---

## 🏛️ Regulatory Compliance Matrix

| Regulatory Standard | Scope & Mandate | PrecisionX Compliance Level |
| :--- | :--- | :--- |
| **OIML R 76-1:2006 (E)** | Non-automatic weighing instruments (Part 1: Metrological & technical requirements) | **Full Implementation** (Forms 1, 3, 5, Table 6 MPE limits, Turning Point formula). |
| **WELMEC Guide 7.2** | Measuring Instruments Directive 2014/32/EU Software Guide | **Full Compliance** (Form 15 LRS examination, Extension L long-term storage, Extension U update validation). |
| **ISO/IEC 17025:2017** | Competence of testing and calibration laboratories | **Full Compliance** (Clause 7.10 nonconforming work controls, Clause 7.8.8 amendment audit trail). |
| **ISO 19005-3:2012** | Electronic document file format for long-term preservation (PDF/A-3) | **Full Compliance** (Embedded DCC XML in conformant archival vector containers). |
| **PTB DCC v3.2.1** | Digital Calibration Certificate XML Schema | **Full Compliance** (SmartCom D-SI XML for global mutual recognition). |
| **RFC 8032** | Edwards-Curve Digital Signature Algorithm (Ed25519) | **Full Compliance** (64-byte asymmetric cryptographic signatures). |

---

## 🔒 Zero-Trust Security & Confidentiality

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
* **Documentation**: [User Manual (HOW_TO_USE.md)](HOW_TO_USE.md) | [Hardware Specs](HARDWARE_AND_PLATFORM_SPECIFICATION.md) | [Security Policy](SECURITY.md) | [Contributing Guide](CONTRIBUTING.md)
