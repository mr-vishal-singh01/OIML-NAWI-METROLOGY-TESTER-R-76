#!/usr/bin/env bash
# ==============================================================================
# SIH26035: Standalone Android APK Build Script (Capacitor + Gradle)
# Team PrecisionX — Smart India Hackathon
# ==============================================================================

set -e

MOBILE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$MOBILE_DIR"

echo "================================================================================"
echo "   🤖 STANDALONE ANDROID APK BUILDER (CAPACITOR)"
echo "   Package: gov.in.sih26035.metrology"
echo "================================================================================"

# Check Node.js and npm
if ! command -v npm >/dev/null 2>&1; then
    echo "[ERROR] Node.js & npm are required to build native Android APKs."
    echo "Please install Node.js (https://nodejs.org) or run: sudo apt install nodejs npm"
    exit 1
fi

echo "[1/4] Ensuring www bundle is synchronized with latest Bauhaus assets..."
mkdir -p www/icons
cp -f scanner.html www/index.html
cp -f manifest.json www/manifest.json
cp -f service-worker.js www/service-worker.js
cp -rf icons/* www/icons/ 2>/dev/null || true

echo "[2/4] Installing Capacitor dependencies..."
if [ ! -d "node_modules/@capacitor" ]; then
    npm install @capacitor/core @capacitor/cli @capacitor/android --silent
fi

echo "[3/4] Initializing / Syncing Android platform..."
if [ ! -d "android" ]; then
    npx cap add android
else
    npx cap sync android
fi

echo "[4/4] Building APK..."
if [ -d "android" ]; then
    cd android
    if [ -x "./gradlew" ]; then
        ./gradlew assembleDebug
        echo ""
        echo "================================================================================"
        echo "   [✓] ANDROID DEBUG APK BUILT SUCCESSFULLY!"
        echo "   APK Location: mobile/android/app/build/outputs/apk/debug/app-debug.apk"
        echo "   Install on phone: adb install mobile/android/app/build/outputs/apk/debug/app-debug.apk"
        echo "================================================================================"
    else
        echo "[*] Android Studio project ready. Run in Android Studio or connect device via ADB:"
        echo "    cd mobile && npx cap open android"
    fi
fi
