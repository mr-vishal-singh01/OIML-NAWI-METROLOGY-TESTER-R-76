# 🛡️ PrecisionX Security Policy & Cryptographic Specifications

**Project**: OIML-NAWI-METROLOGY-TESTER-R-76  
**Problem Statement ID**: SIH26035  
**Governing Authority**: Legal Metrology Division, Ministry of Consumer Affairs, Food & Public Distribution, Govt. of India  
**Accreditation Standards**: ISO/IEC 17025:2017 & WELMEC Guide 7.2 (Extension L & U)

---

## 🔒 Security Architecture Overview

PrecisionX is architected under strict **Zero-Trust** and **Local-First** principles for legal metrology and sovereign statutory verification. Because India is the 13th issuing authority under the OIML-CS, test records, pattern approval data, and verification certificates require cryptographic immutability and complete non-repudiation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ZERO-TRUST CRYPTOGRAPHIC PIPELINE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Local-First Engine    ──> Raw observation data evaluated locally in memory │
│ 2. SHA-256 State Hashing ──> Append-only audit trail chaining every test event  │
│ 3. Anti-Rollback Gate    ──> Prior certified states immutable; edits bump rev  │
│ 4. Ed25519 Signing       ──> RFC 8032 Asymmetric seal (64-byte private key)  │
│ 5. ISO 19005-3 Container ──> Embedded PTB DCC XML in archival PDF/A-3          │
│ 6. Reed-Solomon QR       ──> Offline Level-H verification with 20-30% recovery │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Management & Cryptographic Standards

1. **Digital Seals**:
   - **Algorithm**: Ed25519 (Edwards-Curve Digital Signature Algorithm over Curve25519 as specified in **RFC 8032**).
   - **Key Separation**: Production private signing keys (`ed25519_private.pem`) are strictly air-gapped and excluded from version control via `.gitignore`.
   - **Public Keys**: Public keys (`ed25519_public.pem`) are embedded in the mobile verifier and public verification endpoints to facilitate 100% offline claim validation.

2. **State Immutability (Anti-Rollback)**:
   - Every observation step (e.g., zero drift, turning point addition, corner load) generates a SHA-256 hash incorporating the previous observation's hash:
     $$\text{Hash}_n = \text{SHA256}(\text{Hash}_{n-1} \parallel \text{Reading}_n \parallel \text{Timestamp} \parallel \text{InspectorID})$$
   - Once a session transitions to `APPROVED` or `CERTIFIED`, previous observations cannot be silently altered.
   - Any retrospective alteration automatically invalidates downstream calculations, revokes active certificates, and forces an immutable revision bump (`Rev 1 -> Rev 2`) with logged justification.

3. **Database Security & Secrets**:
   - Application data is maintained in a local SQLite engine running in WAL mode with strict file permissions (`0600`).
   - Private keys and sensitive tokens are barred from Git repositories via pre-commit audit filters.

---

## 🚨 Reporting Security Vulnerabilities

We welcome responsible security disclosures from security researchers, auditors, and metrology professionals.

If you discover a potential vulnerability in the metrological engine, cryptographic signing workflow, or API layer:
1. **Do NOT open a public GitHub issue.**
2. Email the core engineering team directly with full details, proof-of-concept steps, and environment specifics.
3. Include your GPG public key if you require encrypted communication.
4. The team will acknowledge receipt within 24 hours and provide an estimated timeline for remediation.

---

## 📜 Compliance Auditing

All code committed to this repository is subjected to:
- Static Application Security Testing (SAST).
- Dependency vulnerability scans (`pip-audit`, `npm audit`).
- Zero-leakage regex scans for credentials and private key material.
- 142 automated regression and fuzzing tests verifying boundary limits and mathematical integrity.
