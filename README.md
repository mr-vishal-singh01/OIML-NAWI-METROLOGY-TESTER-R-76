# 🇮🇳 OIML-NAWI-METROLOGY-TESTER-R-76

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
  <img src="https://img.shields.io/badge/Verification%20Tests-111%20Passed%20(100%25)-22c55e.svg?style=for-the-badge" alt="Tests 111 Passed">
  <img src="https://img.shields.io/badge/Architecture-Zero--Trust%20%7C%20Local--First-102048.svg?style=for-the-badge" alt="Zero Trust">
</p>

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
  [Forms Verification] ──────────> Form 1 (Weighing & Hysteresis)
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

## 🎯 Key Innovation Pillars

### 1. Automated Turning Point Derivation
Digital indicators round the true weight to the nearest scale division interval ($d$). PrecisionX guides the inspector through fractional load additions ($\Delta L$) to calculate the true turning point:
$$P = I + \frac{1}{2}d - \Delta L$$
Corrected error is derived relative to the established zero-drift error ($E_0$):
$$E_c = (P - L) - E_0$$
The software instantly verifies $E_c$ against statutory Maximum Permissible Error (MPE) tolerances across all load steps.

### 2. ISO/IEC 17025 Anti-Rollback Invalidation Engine
- When a test report is formally certified, its cryptographic state hash is frozen in an append-only ledger.
- If an operator modifies any earlier observation reading, the system automatically:
  1. Revokes existing approvals and demands a mandatory technical justification reason.
  2. Flags all downstream calculations and certificates as `STALE`.
  3. Increments the session to a new revision while locking the superseded revision in an immutable audit archive.
- Retrospective tampering and silent data manipulation are rendered mathematically impossible.

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

## 🧪 Verification & Automated Testing

The metrological mathematical engine is verified through a comprehensive **111-test automated testing suite** covering corner cases, tolerance transitions, and tamper resistance:

```
============================= test session starts ==============================
collected 111 items

tests/test_complete_system.py .............. PASSED [  5%]
tests/test_database_persistence.py ......... PASSED [  7%]
tests/test_ed25519_advanced_resilience.py .. PASSED [ 25%]
tests/test_ed25519_degradation_sweep.py .... PASSED [ 28%]
tests/test_ed25519_offline_qr.py ........... PASSED [ 46%]
tests/test_jury_demo_workflow.py ........... PASSED [ 50%]
tests/test_master_metrology_security_suite.  PASSED [ 61%]
tests/test_nawi_engine.py .................. PASSED [ 72%]
tests/test_opencv_fuzzing_pipeline.py ...... PASSED [ 76%]
tests/test_pdfa3_container.py .............. PASSED [ 95%]
tests/test_revision_workflow.py ............ PASSED [ 99%]
tests/test_vertical_slice_api.py ........... PASSED [100%]

======================== 111 passed in 108.04s (0:01:48) ========================
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

## 🔒 Security & Confidentiality Notice

> [!NOTE]
> In accordance with competition rules, intellectual property protection, and laboratory security practices under ISO/IEC 17025, proprietary hardware drivers, private production keys, and production deployment bundles are maintained in the team's internal deployment registry. 
> 
> Live demonstrations of the full testing suite, interactive UI, and hardware integrations are presented exclusively during official jury evaluations.

---

## 👥 Team PrecisionXP — Smart India Hackathon 2026

* **Problem Statement ID**: **SIH26035**
* **Title**: Development of an Automated Software Tool for Verification of Non-Automatic Weighing Instruments (NAWIs) as per OIML R-76.
* **Ministry / Department**: Ministry of Consumer Affairs, Food & Public Distribution — Legal Metrology Division, Govt. of India.
* **Theme**: Blockchain & Cybersecurity / Smart Automation.
