#!/usr/bin/env bash
# ==============================================================================
# SIH26035: Automated OIML R-76 Guided NAWI Testing Suite
# Universal High-Performance Runner for Linux, macOS & Android PWA Server
# Team PrecisionX — Ministry of Consumer Affairs, Govt. of India
# ==============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

PORT=8000
HOST="0.0.0.0"

echo "================================================================================"
echo "   🇮🇳 SMART INDIA HACKATHON (SIH26035) — LEGAL METROLOGY WORKBENCH"
echo "   Automated OIML R-76 Guided Testing, PDF/A-3, PTB DCC v3.2.1 & Ed25519"
echo "================================================================================"

# 1. Clean up any stale process on Port 8000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "[*] Port $PORT is occupied. Checking service responsiveness..."
    if curl -s -f "http://127.0.0.1:$PORT/api/session" >/dev/null 2>&1; then
        echo "[✓] Legal Metrology Workbench is already running on http://127.0.0.1:$PORT"
        xdg-open "http://127.0.0.1:$PORT" 2>/dev/null || open "http://127.0.0.1:$PORT" 2>/dev/null || true
        exit 0
    else
        echo "[*] Cleaning up stale process on port $PORT..."
        fuser -k $PORT/tcp 2>/dev/null || true
        sleep 1
    fi
fi

# 2. Virtual Environment Setup
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "[+] Initializing Python virtual environment..."
    if command -v uv >/dev/null 2>&1; then
        echo "[+] Using uv for lightning-fast environment setup..."
        uv venv "$PROJECT_ROOT/.venv"
        uv pip install --python "$VENV_PYTHON" -r "$PROJECT_ROOT/requirements.txt"
    else
        python3 -m venv "$PROJECT_ROOT/.venv"
        "$VENV_PYTHON" -m pip install --upgrade pip
        "$VENV_PYTHON" -m pip install --prefer-binary -r "$PROJECT_ROOT/requirements.txt"
    fi
fi

# 3. Verify Dependencies
if ! "$VENV_PYTHON" -c "import fastapi, uvicorn, pydantic, cryptography, qrcode" 2>/dev/null; then
    echo "[+] Installing missing packages..."
    if command -v uv >/dev/null 2>&1; then
        uv pip install --python "$VENV_PYTHON" -r "$PROJECT_ROOT/requirements.txt"
    else
        "$VENV_PYTHON" -m pip install --prefer-binary -r "$PROJECT_ROOT/requirements.txt"
    fi
fi

# 4. Resolve Local IP for Android / Mobile access
LOCAL_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7}' | tr -d '\n' || true)
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")
fi

PWA_URL="http://${LOCAL_IP}:${PORT}/mobile/scanner.html"
WORKBENCH_URL="http://127.0.0.1:${PORT}"

echo ""
echo "   [✓] Server listening on:       http://${HOST}:${PORT}"
echo "   [✓] Desktop Workbench UI:      ${WORKBENCH_URL}"
echo "   [✓] Android Mobile Scanner:    ${PWA_URL}"
echo "   [✓] OpenAPI Documentation:     ${WORKBENCH_URL}/docs"
echo ""
echo "   -------------------------------------------------------------------------"
echo "   📱 ANDROID INSTANT CONNECT (PHONE / TABLET):"
echo "   Scan this terminal QR code with your mobile camera or barcode scanner:"
echo "   -------------------------------------------------------------------------"

"$VENV_PYTHON" -c "
import qrcode
qr = qrcode.QRCode(border=1)
qr.add_data('${PWA_URL}')
qr.make(fit=True)
try:
    qr.print_ascii(invert=True)
except Exception:
    pass
" 2>/dev/null || true

echo ""
echo "[+] Launching desktop interface..."

# 5. Open Desktop Browser in background after server is up
(
    for i in {1..20}; do
        if curl -s -f "http://127.0.0.1:$PORT/api/session" >/dev/null 2>&1; then
            xdg-open "$WORKBENCH_URL" 2>/dev/null || open "$WORKBENCH_URL" 2>/dev/null || true
            break
        fi
        sleep 0.3
    done
) &

# 6. Ensure Python package resolution
export PYTHONPATH="$PROJECT_ROOT/backend:$PROJECT_ROOT/src:$PYTHONPATH"

# 7. Start ASGI Server with optimal workers & reload
APP_DIR="backend"
if [ ! -d "$PROJECT_ROOT/backend" ] && [ -d "$PROJECT_ROOT/src" ]; then
    APP_DIR="src"
fi

exec "$VENV_PYTHON" -m uvicorn api.main:app --app-dir "$PROJECT_ROOT/$APP_DIR" --host "$HOST" --port "$PORT" --reload
