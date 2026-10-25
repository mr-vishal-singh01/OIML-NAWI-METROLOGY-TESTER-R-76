@echo off
setlocal enabledelayedexpansion

echo ================================================================================
echo    [INDIA] SIH26035: UNIVERSAL LEGAL METROLOGY WORKBENCH INSTALLER
echo    Windows 1-Click Complete System Setup
echo    Team PrecisionX - Ministry of Consumer Affairs, Govt. of India
echo ================================================================================
echo.

cd /d "%~dp0"

:: 1. Check Python 3.10+
echo [1/4] Validating Python 3.10+ Environment...
set PYTHON_CMD=
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
    ) else (
        if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        ) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
            set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        ) else (
            echo [!] Python 3.10+ is not detected on your system.
            echo [+] Attempting automatic installation via Windows Package Manager (winget)...
            winget install --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
            if %errorlevel% neq 0 (
                echo [ERROR] Winget installation failed.
                echo Please download and install Python 3.11 from https://www.python.org/downloads/
                echo IMPORTANT: Check "Add Python to PATH" during installation.
                pause
                exit /b 1
            )
            set PYTHON_CMD=python
        )
    )
)

echo [✓] Using Python: %PYTHON_CMD%

:: 2. Setup Virtual Environment
echo [2/4] Initializing isolated virtual environment (.venv)...
set VENV_PYTHON=.venv\Scripts\python.exe
if not exist "%VENV_PYTHON%" (
    where uv >nul 2>nul
    if %errorlevel% equ 0 (
        echo      [+] Fast setup with uv...
        uv venv .venv
        uv pip install --python "%VENV_PYTHON%" -r requirements.txt
    ) else (
        %PYTHON_CMD% -m venv .venv
        call .venv\Scripts\activate.bat
        python -m pip install --upgrade pip
        python -m pip install --prefer-binary -r requirements.txt
    )
) else (
    echo [✓] Virtual environment ready.
)

:: 3. Verify Dependencies
echo [3/4] Verifying dependencies...
call .venv\Scripts\activate.bat
"%VENV_PYTHON%" -c "import fastapi, uvicorn, pydantic, cryptography, qrcode" >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Installing dependencies from requirements.txt...
    pip install --prefer-binary -r requirements.txt
)

:: 4. Desktop Shortcut Creation with Bauhaus Monochrome Icon
echo [4/4] Creating Windows Desktop Shortcut with Bauhaus Icon...
set SCRIPT="%TEMP%\create_metrology_shortcut.vbs"
set ICON_PATH="%CD%\desktop\assets\icon.ico"

echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\PrecisionX Legal Metrology Workbench.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CD%\run_workbench.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CD%" >> %SCRIPT%
echo oLink.Description = "Automated OIML R-76 Guided NAWI Testing Suite (SIH26035)" >> %SCRIPT%
if exist %ICON_PATH% (
    echo oLink.IconLocation = %ICON_PATH% >> %SCRIPT%
)
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo ================================================================================
echo    [✓] WINDOWS INSTALLATION COMPLETE!
echo    • 1-Click Desktop Shortcut: "PrecisionX Legal Metrology Workbench"
echo    • Run anytime by double clicking the shortcut or running run_workbench.bat
echo ================================================================================
echo.

set /p START_NOW="Would you like to launch the workbench now? (Y/N): "
if /i "%START_NOW%"=="Y" (
    call run_workbench.bat
)
