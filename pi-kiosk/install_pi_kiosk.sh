#!/usr/bin/env bash
# ==============================================================================
# SIH26035: 1-Click Automated Raspberry Pi Kiosk Installer
# Configures a Raspberry Pi 4 or 5 into a dedicated benchtop metrology station
# ==============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run with sudo: sudo ./install_pi_kiosk.sh"
  exit 1
fi

PI_USER="${SUDO_USER:-pi}"
INSTALL_DIR="/home/$PI_USER/sih-metrology"

echo "================================================================================"
echo "   [IN] SIH26035: RASPBERRY PI LEGAL METROLOGY BENCH STATION INSTALLER"
echo "================================================================================"

echo "[1/6] Updating apt packages and installing system prerequisites..."
apt-get update
apt-get install -y python3-pip python3-venv chromium-browser unclutter libzbar0 libgl1-mesa-glx udev

echo "[2/6] Configuring hardware serial permissions (RS-232 / USB scales)..."
usermod -a -G dialout,tty,video "$PI_USER"

# Install udev rules for FTDI, Prolific, CH340, CP2102 serial adapters
cat << 'UDEV' > /etc/udev/rules.d/99-legal-metrology-scales.rules
# FTDI FT232 USB-Serial
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", MODE="0666", GROUP="dialout"
# Silicon Labs CP210x
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", MODE="0666", GROUP="dialout"
# Prolific PL2303
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", MODE="0666", GROUP="dialout"
# WCH CH340
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", MODE="0666", GROUP="dialout"
UDEV
udevadm control --reload-rules && udevadm trigger

echo "[3/6] Setting up application files in $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp -r ../backend "$INSTALL_DIR/"
cp -r ../data "$INSTALL_DIR/"
cp -r ../schemas "$INSTALL_DIR/"
cp ../requirements.txt "$INSTALL_DIR/"

echo "[4/6] Initializing Python virtual environment..."
sudo -u "$PI_USER" python3 -m venv "$INSTALL_DIR/.venv"
sudo -u "$PI_USER" "$INSTALL_DIR/.venv/bin/pip" install --upgrade pip
sudo -u "$PI_USER" "$INSTALL_DIR/.venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

echo "[5/6] Registering systemd background service..."
sed -i "s|/home/pi/sih-metrology|$INSTALL_DIR|g" sih-metrology.service
sed -i "s|User=pi|User=$PI_USER|g" sih-metrology.service
cp sih-metrology.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable sih-metrology.service
systemctl restart sih-metrology.service

echo "[6/6] Configuring autostart desktop kiosk session..."
AUTOSTART_DIR="/home/$PI_USER/.config/lxsession/LXDE-pi"
mkdir -p "$AUTOSTART_DIR"
cat << AUTOSTART > "$AUTOSTART_DIR/autostart"
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@$INSTALL_DIR/pi-kiosk/kiosk.sh
AUTOSTART
chown -R "$PI_USER:$PI_USER" "/home/$PI_USER/.config"
chown -R "$PI_USER:$PI_USER" "$INSTALL_DIR"

echo ""
echo "================================================================================"
echo "   [✓] RASPBERRY PI METROLOGY STATION INSTALLATION COMPLETE!"
echo "   On reboot, the Raspberry Pi will launch full-screen into the Legal Metrology UI."
echo "   To start manually now: systemctl start sih-metrology && $INSTALL_DIR/pi-kiosk/kiosk.sh"
echo "================================================================================"
