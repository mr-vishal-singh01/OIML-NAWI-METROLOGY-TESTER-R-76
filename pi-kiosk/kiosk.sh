#!/usr/bin/env bash
# ==============================================================================
# SIH26035: Raspberry Pi Kiosk Auto-Start Session
# Runs full-screen touch interface on official Raspberry Pi 7" or 10.1" Display
# ==============================================================================

# Disable screen blanking and power management
xset s noblank
xset s off
xset -dpms

# Hide mouse cursor after 3 seconds of inactivity
unclutter -idle 3 -root &

# Wait for local metrology backend service to report healthy
echo "[*] Waiting for Legal Metrology backend..."
until curl -s http://127.0.0.1:8000/api/session > /dev/null; do
    sleep 0.5
done

# Launch Chromium in dedicated full-screen kiosk mode
chromium-browser \
    --noerrdialogs \
    --disable-infobars \
    --kiosk \
    --check-for-update-interval=31536000 \
    --disable-pinch \
    --overscroll-history-navigation=0 \
    --enable-features=OverlayScrollbar \
    http://127.0.0.1:8000
