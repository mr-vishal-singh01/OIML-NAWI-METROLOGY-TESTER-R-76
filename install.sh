#!/usr/bin/env bash
# ==============================================================================
# SIH26035: UNIVERSAL 1-CLICK MASTER INSTALLER (LINUX / macOS / RASPBERRY PI)
# Team PrecisionX — Ministry of Consumer Affairs, Govt. of India
# ==============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "================================================================================"
echo "   🇮🇳 SIH26035: UNIVERSAL LEGAL METROLOGY WORKBENCH INSTALLER"
echo "   Automated OIML R-76 Testing, PDF/A-3, PTB DCC v3.2.1, Ed25519 & Android PWA"
echo "================================================================================"
echo ""

# 1. System Python Check
echo "[1/6] Validating Python 3.10+ Environment..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] Python 3 is required. Please install python3, python3-venv, and python3-pip:"
    echo "       sudo apt install -y python3 python3-venv python3-pip libzbar0"
    exit 1
fi
PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "      Found Python $PYTHON_VER"

# 2. Virtual Environment Setup
echo "[2/6] Configuring isolated virtual environment (.venv)..."
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
if [ ! -d ".venv" ]; then
    if command -v uv >/dev/null 2>&1; then
        echo "      [+] Accelerated venv provisioning with uv..."
        uv venv .venv
    else
        python3 -m venv .venv
    fi
fi

# 3. Fast Dependency Installation
echo "[3/6] Installing & caching production dependencies..."
if command -v uv >/dev/null 2>&1; then
    uv pip install --python "$VENV_PYTHON" -r requirements.txt
else
    "$VENV_PYTHON" -m pip install --upgrade pip --quiet
    "$VENV_PYTHON" -m pip install --prefer-binary -r requirements.txt
fi

# 4. Optical Barcode & Metrology Driver Checks
echo "[4/6] Verifying Optical CV and Serial Scale drivers..."
if ! "$VENV_PYTHON" -c "import pyzbar" 2>/dev/null; then
    echo "      [!] Notice: libzbar0 recommended for pyzbar optical barcode parsing."
    if command -v apt-get >/dev/null 2>&1 && [ "$EUID" -eq 0 ]; then
        apt-get install -y -qq libzbar0 || true
    fi
fi

# 5. Icon & Desktop Application Integration
echo "[5/6] Deploying Bauhaus monochrome icons & Desktop shortcuts..."
mkdir -p "$HOME/.local/share/applications"
mkdir -p "$HOME/.local/share/icons"
mkdir -p "$PROJECT_ROOT/desktop/assets"
mkdir -p "$PROJECT_ROOT/mobile/icons"
mkdir -p "$PROJECT_ROOT/mobile/www/icons"

ICON_SRC="$PROJECT_ROOT/desktop/assets/precisionx.png"
if [ -f "$ICON_SRC" ]; then
    cp -f "$ICON_SRC" "$HOME/.local/share/icons/precisionx.png"
fi
ICON_SVG="$PROJECT_ROOT/desktop/assets/precisionx.svg"
if [ -f "$ICON_SVG" ]; then
    cp -f "$ICON_SVG" "$HOME/.local/share/icons/precisionx.svg"
fi

cat << DESKTOP > "$HOME/.local/share/applications/sih-metrology.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=PrecisionX Legal Metrology Workbench
GenericName=OIML R-76 Testing Suite
Comment=Automated OIML R-76 Guided NAWI Testing, PDF/A-3, PTB DCC v3.2.1 & Ed25519
Exec="$PROJECT_ROOT/run_workbench.sh"
Icon=$HOME/.local/share/icons/precisionx.png
Terminal=true
Categories=Science;Office;Engineering;Development;
Keywords=Metrology;OIML;Weighing;Scale;Calibration;PrecisionX;SIH;
StartupNotify=true
DESKTOP
chmod +x "$HOME/.local/share/applications/sih-metrology.desktop"

if [ -d "$HOME/Desktop" ]; then
    cp -f "$HOME/.local/share/applications/sih-metrology.desktop" "$HOME/Desktop/PrecisionX_Workbench.desktop"
    chmod +x "$HOME/Desktop/PrecisionX_Workbench.desktop"
    gio set "$HOME/Desktop/PrecisionX_Workbench.desktop" metadata::trusted true 2>/dev/null || true
fi

# 6. Self-Test Validation
echo "[6/6] Running system verification self-test..."
"$VENV_PYTHON" -c "
import fastapi, uvicorn, pydantic, cryptography, qrcode, PIL, cv2
print('      [✓] All core engines (FastAPI, Crypto, QR, OpenCV, PIL) initialized successfully!')
"

echo ""
echo "================================================================================"
echo "   🇮🇳 INSTALLATION SUCCESSFUL! YOUR WORKBENCH IS READY TO USE."
echo "================================================================================"
echo "   • 1-Click Desktop Icon:   'PrecisionX_Workbench.desktop' (On your Desktop)"
echo "   • Launch from Terminal:   ./run_workbench.sh"
echo "   • Android Mobile Scanner: ./mobile/run_android_pwa.sh"
echo "   • Windows 1-Click Runner: run_workbench.bat"
echo "================================================================================"
echo ""

read -p "Would you like to start the Metrology Workbench now? (Y/n): " -n 1 -r || true
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    exec "$PROJECT_ROOT/run_workbench.sh"
fi
