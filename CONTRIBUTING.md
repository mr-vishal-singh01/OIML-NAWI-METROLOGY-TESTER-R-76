# 🤝 Contributing to PrecisionX (OIML-NAWI-METROLOGY-TESTER-R-76)

Thank you for your interest in contributing to **PrecisionX**! This repository provides the statutory Non-Automatic Weighing Instrument (NAWI) verification software developed for the **Smart India Hackathon 2026 (Problem Statement ID: SIH26035)** under the aegis of the **Legal Metrology Division, Ministry of Consumer Affairs, Food & Public Distribution, Govt. of India**.

---

## 🏛️ Engineering & Metrological Principles

Contributors must preserve the following principles:
1. **Mathematical Precision**: All turning point ($P = I + 0.5e - \Delta L$) and error calculations ($E_c = E - E_0$) must follow OIML R 76-1:2006 (E) without approximation or floating-point rounding errors.
2. **ISO/IEC 17025 Compliance**: Audit integrity, immutable change tracking, and anti-rollback rules must never be bypassed.
3. **WELMEC 7.2 Software Examination**: Any UI or firmware alteration must conform to WELMEC 7.2 software separation principles (Form 15 requirements).
4. **Zero-Trust & Privacy**: Never commit private keys (`.pem`, `.key`), credentials, or raw SQLite database binaries.

---

## 🛠️ Development Setup

### 1. Clone & Environment Setup
```bash
git clone https://github.com/mr-vishal-singh01/OIML-NAWI-METROLOGY-TESTER-R-76.git
cd OIML-NAWI-METROLOGY-TESTER-R-76

# Create Python 3.11 virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run the Verification Test Suite
Before proposing any code change, verify that all 142 automated tests pass:
```bash
PYTHONPATH=src:. python3 -m unittest discover tests
```

Expected output:
```text
Ran 142 tests in 111.433s
OK
```

### 3. Launching the Local Development Servers
* **Backend API (FastAPI)**:
  ```bash
  cd src/api
  uvicorn main:app --reload --port 8000
  ```
  Swagger UI will be available at `http://127.0.0.1:8000/docs`.

* **Desktop Application (Electron)**:
  ```bash
  cd desktop
  pnpm install
  pnpm start
  ```

---

## 🌿 Branching & Commit Conventions

We follow Conventional Commits:
- `feat(metrology): ...` — New metrological test procedures or calculations.
- `feat(reporting): ...` — PDF/A-3 or PTB DCC XML generator enhancements.
- `fix(engine): ...` — Bug fixes in tolerance evaluation or formula derivation.
- `test(security): ...` — New unit tests, property tests, or fuzzing checks.
- `docs(...)`: — Documentation, user manuals, and specifications.

---

## 📋 Pull Request Checklist

When submitting a Pull Request:
- [ ] Added or updated unit tests covering all new logic.
- [ ] Confirmed all 142 tests pass cleanly (`python3 -m unittest discover tests`).
- [ ] Validated that no secret keys (`*.pem`, `*.key`) or sqlite databases (`*.db`) are tracked.
- [ ] Verified that mathematical error calculations comply with Table 6 MPE limits.
- [ ] Ensured code adheres to Python PEP8 standards and clean architectural patterns.
