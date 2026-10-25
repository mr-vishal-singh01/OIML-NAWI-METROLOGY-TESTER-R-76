#!/usr/bin/env bash
# ==============================================================================
# SIH26035: Android & Mobile Field Inspector PWA Runner
# Team PrecisionX — Smart India Hackathon
# ==============================================================================

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

PORT=8000

# 1. Clean up port 8000 if occupied by dead process
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    if ! curl -s -f "http://127.0.0.1:$PORT/api/session" >/dev/null 2>&1; then
        echo "[*] Cleaning up stale process on port $PORT..."
        fuser -k $PORT/tcp 2>/dev/null || true
        sleep 1
    fi
fi

# 2. Virtual environment resolution
VENV_PYTHON="$APP_DIR/.venv/bin/python"
if [ ! -x "$VENV_PYTHON" ] && [ -x "$APP_DIR/../SIH HACKATHON/.venv/bin/python" ]; then
    VENV_PYTHON="$APP_DIR/../SIH HACKATHON/.venv/bin/python"
fi
if [ ! -x "$VENV_PYTHON" ]; then
    VENV_PYTHON="python3"
fi

# 3. Synchronize newest Bauhaus icons to mobile and www bundles
mkdir -p "$APP_DIR/mobile/www/icons"
cp -f "$APP_DIR/mobile/icons/"* "$APP_DIR/mobile/www/icons/" 2>/dev/null || true
cp -f "$APP_DIR/mobile/scanner.html" "$APP_DIR/mobile/www/index.html" 2>/dev/null || true
cp -f "$APP_DIR/mobile/manifest.json" "$APP_DIR/mobile/www/manifest.json" 2>/dev/null || true
cp -f "$APP_DIR/mobile/service-worker.js" "$APP_DIR/mobile/www/service-worker.js" 2>/dev/null || true

# 4. Detect Local Network IP (for Android phone connection)
LOCAL_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7}' | tr -d '\n' || true)
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")
fi

PWA_URL="http://${LOCAL_IP}:${PORT}/mobile/scanner.html"
WORKBENCH_URL="http://${LOCAL_IP}:${PORT}"

echo "================================================================================"
echo "   📱 ANDROID / MOBILE FIELD INSPECTOR & PWA RUNNER"
echo "   Team PrecisionX — OIML R-76 Certificate Scanner & Field Testing"
echo "================================================================================"
echo ""
echo "   [✓] Server listening on:  0.0.0.0:${PORT}"
echo "   [✓] Mobile Scanner URL:   ${PWA_URL}"
echo "   [✓] Full Workbench URL:   ${WORKBENCH_URL}"
echo ""
echo "   -------------------------------------------------------------------------"
echo "   HOW TO RUN ON ANY ANDROID DEVICE (PHONE / TABLET):"
echo "   1. Ensure your Android phone is on the SAME Wi-Fi or Hotspot."
echo "   2. Point your phone camera at the QR code below to open the app instantly."
echo "   3. In Chrome on Android: Tap '⋮' -> 'Install app' or 'Add to Home Screen'."
echo "   4. The PrecisionX app installs as a native-feel offline Android app!"
echo "   -------------------------------------------------------------------------"
echo ""

# Render QR code in terminal for mobile scanning
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
echo "[+] Starting server for Android clients (Press Ctrl+C to stop)..."

APP_SUBDIR="backend"
if [ ! -d "$APP_DIR/backend" ] && [ -d "$APP_DIR/src" ]; then
    APP_SUBDIR="src"
fi

export PYTHONPATH="$APP_DIR/backend:$APP_DIR/src:$PYTHONPATH"
exec "$VENV_PYTHON" -m uvicorn api.main:app --app-dir "$APP_SUBDIR" --host 0.0.0.0 --port "$PORT" --reload
