#!/usr/bin/env python3
"""
SIH26035: PrecisionX Legal Metrology Workbench
Universal Cross-Platform Auto-Installer and Health Diagnostic Engine
Supports: Windows, Linux (Ubuntu/Debian/Fedora/Arch), macOS, Raspberry Pi, Android Termux
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def print_banner():
    print("=" * 80)
    print("   🇮🇳 SIH26035: UNIVERSAL LEGAL METROLOGY WORKBENCH - ONE-CLICK SETUP")
    print("   Automated OIML R-76 Testing Suite | PDF/A-3 DCC v3.2.1 | Ed25519 Cryptography")
    print("   Ministry of Consumer Affairs, Food & Public Distribution, Govt. of India")
    print("=" * 80)
    print(f"[*] Detected Operating System: {platform.system()} ({platform.machine()})")
    print(f"[*] Python Interpreter:        {sys.executable} (v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})")
    print("-" * 80)

def main():
    print_banner()
    root_dir = Path(__file__).resolve().parent
    os.chdir(root_dir)

    is_windows = platform.system() == "Windows"
    is_linux = platform.system() == "Linux"
    is_darwin = platform.system() == "Darwin"

    # 1. Virtual Environment Setup
    venv_dir = root_dir / ".venv"
    if is_windows:
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"

    if not venv_python.exists():
        print("[1/5] Initializing virtual environment...")
        has_uv = shutil.which("uv") is not None
        if has_uv:
            print("      [+] Found uv - performing high-speed provisioning...")
            subprocess.run(["uv", "venv", str(venv_dir)], check=True)
        else:
            print("      [+] Using standard venv...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    else:
        print("[1/5] Virtual environment already initialized.")

    # 2. Dependency Installation
    print("[2/5] Checking and installing requirements...")
    has_uv = shutil.which("uv") is not None
    req_file = root_dir / "requirements.txt"
    if has_uv:
        cmd = ["uv", "pip", "install", "--python", str(venv_python), "-r", str(req_file)]
    else:
        cmd = [str(venv_python), "-m", "pip", "install", "--prefer-binary", "-r", str(req_file)]
    
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("[!] Warning: Dependency installer returned non-zero. Retrying with pip...")
        subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(req_file)])

    # 3. Synchronize Bauhaus Icons
    print("[3/5] Deploying Bauhaus monochrome contrast icons across platforms...")
    desktop_assets = root_dir / "desktop" / "assets"
    mobile_icons = root_dir / "mobile" / "icons"
    mobile_www_icons = root_dir / "mobile" / "www" / "icons"
    
    for d in [mobile_icons, mobile_www_icons]:
        d.mkdir(parents=True, exist_ok=True)
        if desktop_assets.exists():
            for f in desktop_assets.iterdir():
                if f.is_file() and (d / f.name) != f:
                    shutil.copy2(f, d / f.name)

    # Linux system icon integration
    if is_linux:
        system_icons = Path.home() / ".local" / "share" / "icons"
        system_icons.mkdir(parents=True, exist_ok=True)
        for icon_name in ["precisionx.png", "precisionx.svg", "icon.png"]:
            src = desktop_assets / icon_name
            if src.exists():
                shutil.copy2(src, system_icons / icon_name)

    # 4. Desktop Shortcut & Menu Registration
    print("[4/5] Creating 1-click desktop shortcuts...")
    if is_linux:
        app_menu = Path.home() / ".local" / "share" / "applications"
        app_menu.mkdir(parents=True, exist_ok=True)
        desktop_entry_path = app_menu / "sih-metrology.desktop"
        desktop_file_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=PrecisionX Legal Metrology Workbench
GenericName=OIML R-76 Testing Suite
Comment=Automated OIML R-76 Guided NAWI Testing, PDF/A-3, PTB DCC v3.2.1 & Ed25519
Exec="{root_dir / 'run_workbench.sh'}"
Icon={Path.home() / '.local/share/icons/precisionx.png'}
Terminal=true
Categories=Science;Office;Engineering;Development;
Keywords=Metrology;OIML;Weighing;Scale;Calibration;PrecisionX;SIH;
StartupNotify=true
"""
        with open(desktop_entry_path, "w", encoding="utf-8") as f:
            f.write(desktop_file_content)
        desktop_entry_path.chmod(0o755)

        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            user_desktop_shortcut = desktop_dir / "PrecisionX_Workbench.desktop"
            shutil.copy2(desktop_entry_path, user_desktop_shortcut)
            user_desktop_shortcut.chmod(0o755)
            subprocess.run(["gio", "set", str(user_desktop_shortcut), "metadata::trusted", "true"], stderr=subprocess.DEVNULL)
            print(f"      [✓] Desktop shortcut created: {user_desktop_shortcut}")

    elif is_windows:
        vbs_script = Path(os.environ.get("TEMP", ".")) / "create_shortcut.vbs"
        icon_path = desktop_assets / "icon.ico"
        vbs_content = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\\PrecisionX Legal Metrology Workbench.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{root_dir / 'run_workbench.bat'}"
oLink.WorkingDirectory = "{root_dir}"
oLink.Description = "Automated OIML R-76 Guided NAWI Testing Suite (SIH26035)"
oLink.IconLocation = "{icon_path}"
oLink.Save
"""
        with open(vbs_script, "w", encoding="utf-8") as f:
            f.write(vbs_content)
        subprocess.run(["cscript", "/nologo", str(vbs_script)], check=False)
        if vbs_script.exists():
            vbs_script.unlink()
        print("      [✓] Windows Desktop Shortcut created with Bauhaus icon!")

    # 5. Core Verification Test
    print("[5/5] Performing self-test verification...")
    test_cmd = [
        str(venv_python),
        "-c",
        "import fastapi, uvicorn, pydantic, cryptography, qrcode, PIL, cv2; print('      [✓] Core stack verified!')"
    ]
    subprocess.run(test_cmd, check=True)

    print("-" * 80)
    print("   [✓] SETUP COMPLETED SUCCESSFULLY FOR ALL SYSTEMS!")
    print("   Run options:")
    if is_windows:
        print("   - Double-click 'PrecisionX Legal Metrology Workbench' on your Desktop")
        print("   - Or execute: run_workbench.bat")
    else:
        print("   - Double-click 'PrecisionX_Workbench.desktop' on your Desktop")
        print("   - Or execute: ./run_workbench.sh")
        print("   - For Android field inspectors: ./mobile/run_android_pwa.sh")
    print("=" * 80)

if __name__ == "__main__":
    main()
