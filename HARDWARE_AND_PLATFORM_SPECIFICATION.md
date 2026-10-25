# 🇮🇳 SIH26035: Cross-Platform Deployment & Hardware Engineering Specification
## Standalone Installable Application for Windows, Linux, Android, and Raspberry Pi

---

## 1. Executive Hardware Architecture Overview

The **SIH26035 Legal Metrology Workbench** is engineered as an **offline-first, zero-trust metrology station**. It operates across four distinct operational tiers:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    OPERATIONAL DEPLOYMENT TIERS                                             │
├───────────────────────┬───────────────────────┬──────────────────────────────┬──────────────────────────────┤
│ 🪟 Windows PC / Laptop│ 🐧 Linux Workstation  │ 🍓 Raspberry Pi 4/5 Kiosk    │ 📱 Android Mobile / Tablet   │
├───────────────────────┼───────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ RRSL Office & Mobile  │ Accredited Calibration│ Dedicated Benchtop Station   │ Mobile Field Inspector       │
│ Pattern Evaluation    │ Metrology Testing Labs│ Bolted beside Scale Pan      │ On-site Verification         │
│ (.exe / Native App)   │ (.AppImage / .deb)    │ (Auto-boot Touch Kiosk)      │ (Offline APK / PWA)          │
└───────────────────────┴───────────────────────┴──────────────────────────────┴──────────────────────────────┘
```

---

## 2. Comprehensive Hardware Requirements Matrix

### 2.1 Minimum vs. Recommended Specifications

| Hardware Attribute | Minimum Specification (Budget / Legacy) | Recommended Specification (Lab Standard) | High-Throughput Station (RRSL Master) |
| :--- | :--- | :--- | :--- |
| **Processor (CPU)** | Dual-Core 1.8 GHz (Intel Celeron / ARM Cortex-A72) | Quad-Core 2.4 GHz (Intel Core i3/i5 / Apple M / ARM Cortex-A76) | Octa-Core 3.0+ GHz (Intel Core i7/AMD Ryzen 7) |
| **RAM (Memory)** | **2 GB RAM** (Runs comfortably in low-memory environments) | **4 GB to 8 GB RAM** | **16 GB RAM** |
| **Internal Storage** | **500 MB** free disk space | **2 GB SSD** (for local SQLite WAL & PDF/A-3 archives) | **10 GB+ NVMe SSD** (decade-long audit history) |
| **Display Resolution**| $1024 \times 600$ (7" touch display) | $1920 \times 1080$ (Full HD 1080p) | $2560 \times 1440$ or $3840 \times 2160$ (4K) |
| **I/O Ports** | 1x USB 2.0 (for RS-232 adapter or scale direct USB) | 2x USB 3.0 + 1x USB Type-C + Ethernet LAN | Multiple isolated USB-UART ports + Dual Display |
| **Networking** | **Zero Internet Required** (100% Offline Capable) | Optional Local LAN (for lab printer / network DCC push)| Isolated Metrology VLAN (OIML-CS gateway) |
| **Camera (for QR)** | 2.0 MP fixed focus (with OpenCV recovery pipeline) | 5.0 MP autofocus with LED torch/illumination ring | Industrial barcode scanner / 12 MP camera |

---

## 3. Platform-by-Platform Hardware Selection Guide

### Tier 1: Dedicated Laboratory Bench Station (Raspberry Pi 4 / 5)
*This is the most cost-effective, tamper-resistant deployment for Regional Reference Standard Laboratories (RRSLs) to place directly beside calibration scale pans.*

* **Recommended Single Board Computer:**
  - **Raspberry Pi 5 (4 GB or 8 GB RAM)** or **Raspberry Pi 4 Model B (4 GB RAM)**.
* **Recommended Official Accessories:**
  1. **Official 7" or 10.1" Raspberry Pi Touchscreen Display:** (DSI ribbon cable connection or HDMI).
  2. **Official Raspberry Pi 27W USB-C Power Supply:** Ensures stable 5.1V / 5A power under heavy USB serial load.
  3. **Industrial Passive Aluminum Cooling Case:** Fanless, dust-tight enclosure suited for grain mandis, coal yards, and chemical labs.
  4. **SanDisk Extreme Pro 32GB/64GB MicroSD (A2 V30 class):** High random write endurance for SQLite WAL logs.
* **Total Hardware Cost per Lab Bench:** $\approx \$90 - \$140$ (₹7,500 – ₹11,500 INR).

---

### Tier 2: Office & Laboratory Laptops (Windows 10 / 11)
*Used by Pattern Approval Officers and Lead Metrologists.*
* Any modern laptop or desktop running Windows 10 (Build 19041+) or Windows 11 (64-bit).
* USB-to-RS232 adapter connected to COM1 / COM3.

---

### Tier 3: Mobile Field Inspector Terminals (Android)
*Used by Legal Metrology Officers during surprise market inspections, petrol pump checks, and highway weighbridges.*
* **Device Form Factors:**
  1. **Commercial Android Smartphones:** Android 10.0 (API 29) to Android 15+.
  2. **Rugged Industrial Tablets:** Zebra, Honeywell, or Samsung Galaxy Tab Active series with IP68 dust/waterproofing.
* **Camera Sensor:** Rear camera $\ge 8\,\text{MP}$ with autofocus and flashlight torch support.
* **USB-OTG:** Supports USB Type-C OTG adapters for connecting portable Class II jewelry balances.

---

## 4. Hardware Scale Interfaces & Serial Wiring Guide

### 4.1 Supported RS-232 / USB Chipsets
When purchasing USB-to-Serial adapters for connecting scales, always select adapters featuring genuine, verified industrial chipsets:

| Chipset Manufacturer | Model | Linux Driver | Windows Driver | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **FTDI (Future Technology Devices)** | **FT232RL / FT232R** | Kernel native (`ftdi_sio`) | Auto-installed via Windows Update | ⭐ **Gold Standard (Highest Stability)** |
| **Silicon Labs** | **CP2102 / CP2104** | Kernel native (`cp210x`) | Auto-installed | ⭐ **Excellent (Low Latency)** |
| **WCH** | **CH340 / CH341** | Kernel native (`ch341`) | Included in installer | ✅ Good (Cost-Effective) |
| **Prolific** | **PL2303 (Revision HXD/GC)**| Kernel native (`pl2303`) | Auto-installed | ✅ Good (Standard) |

### 4.2 Standard DB9 RS-232 Weighing Scale Pinout

```
Scale DB9 Connector                         PC / Raspberry Pi USB Adapter
┌─────────────────┐                               ┌─────────────────┐
│ Pin 2: TX (Data)├───────────────────────────────┤ Pin 2: RX (Data)│
│ Pin 3: RX (Cmd) ├───────────────────────────────┤ Pin 3: TX (Cmd) │
│ Pin 5: GND      ├───────────────────────────────┤ Pin 5: GND      │
└─────────────────┘                               └─────────────────┘
```
* **Default Communication Parameters:**
  - **Baud Rate:** `9600` bps (configurable: 2400, 4800, 9600, 19200, 38400).
  - **Data Bits:** `8` bits.
  - **Parity:** `None` (`N`).
  - **Stop Bits:** `1` bit.
  - **Flow Control:** `None` / `XON/XOFF`.

---

## 5. Software Stack Bundled with the Application

When you run our installation packages, **all required software libraries and runtimes are installed automatically**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          BUNDLED RUNTIME STACK                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Component                      │ Purpose & Sourced Standard                 │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Python 3.11 Runtime Core       │ Metrological calculation engine            │
│ FastAPI & Starlette            │ High-speed local REST API framework        │
│ Uvicorn (ASGI Server)          │ Embedded web application server            │
│ SQLite 3 (WAL Mode Enabled)    │ ACID local persistence & revision storage  │
│ Cryptography (PureEdDSA)       │ RFC 8032 Ed25519 digital signature seal    │
│ PyPDF & Chromium Headless      │ ISO 19005-3 PDF/A-3 archival generator    │
│ OpenCV & NumPy Engine          │ Damaged QR code recovery & computer vision │
│ PyZBar & Pillow                │ Level H optical QR decode engine           │
│ Electron Framework             │ Native Desktop Windowing & App Chrome      │
│ Service Worker & Web Crypto    │ Android offline inspection shell           │
└────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 6. How to Install & Run on Each Platform

### 🪟 1. Windows (1-Click Install)
1. Open the project folder in File Explorer.
2. Navigate to `installer\windows\` and double-click **`install_windows.bat`**.
3. *What it does:* Checks Python, sets up `.venv`, installs `requirements.txt`, and generates a **"SIH Legal Metrology Workbench"** shortcut directly on your Windows Desktop.
4. Double-click the desktop shortcut anytime to launch the workbench.

---

### 🐧 2. Linux (Ubuntu, Debian, Fedora)
1. Open terminal in the project directory.
2. Run the Linux installer:
   ```bash
   ./installer/linux/install_linux.sh
   ```
3. *What it does:* Configures serial scale permissions (`/etc/udev/rules.d/`), sets up dependencies, and installs an application launcher into your desktop menu.
4. Launch directly via `./run_workbench.sh` or from your system **Applications Menu**.

---

### 🍓 3. Raspberry Pi 4 / 5 (Bench Kiosk)
1. Flash official **Raspberry Pi OS (64-bit with desktop)** onto an SD card.
2. Boot Raspberry Pi, copy this project folder to `/home/pi/sih-metrology`.
3. Open terminal and run:
   ```bash
   sudo ./pi-kiosk/install_pi_kiosk.sh
   ```
4. Reboot the Raspberry Pi:
   ```bash
   sudo reboot
   ```
5. **Result:** On boot, the Pi launches directly into full-screen touch mode on `http://127.0.0.1:8000`, automatically reading scale data from `/dev/ttyUSB0`!

---

### 📱 4. Android (Mobile Field Inspector App)
* **Method A (Instant PWA Install — Recommended for Inspectors):**
  1. Open Chrome or Edge on your Android phone/tablet.
  2. Navigate to your workstation's local IP or hotspot: `http://<LAPTOP_IP>:8000`.
  3. Chrome will display a banner: **"Add Legal Metrology NAWI to Home Screen"** (or tap ⋮ $\to$ "Install app").
  4. The app installs as a standalone Android application with its own launcher icon, full offline caching, and camera scanner access!
* **Method B (Compile Standalone APK via Capacitor):**
  ```bash
  cd mobile
  npm install @capacitor/core @capacitor/cli @capacitor/android
  npx cap add android
  npx cap build android
  ```

---

## 7. Summary for Hackathon Presentation

When the jury asks: *"Can this run on a physical scale bench or mobile device?"*
* **Show them the Raspberry Pi Kiosk script:** Auto-boots into full-screen touchscreen mode beside the scale pan.
* **Show them the Android Scanner:** Opens camera viewfinder with real-time laser scan for instant Ed25519 verification.
* **Show them the Windows/Linux One-Click Installers:** Creates a native desktop shortcut requiring zero terminal knowledge from inspectors.
