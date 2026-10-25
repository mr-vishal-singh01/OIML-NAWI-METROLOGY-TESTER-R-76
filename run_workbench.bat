@echo off
setlocal enabledelayedexpansion

echo ================================================================================
echo    [INDIA] SMART INDIA HACKATHON (SIH26035) - LEGAL METROLOGY WORKBENCH
echo    Automated OIML R-76 Guided Testing, PDF/A-3, PTB DCC v3.2.1 ^& Ed25519
echo    Team PrecisionX - Ministry of Consumer Affairs, Govt. of India
echo ================================================================================
echo.

cd /d "%~dp0"

:: 1. Detect Python executable
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
            echo [ERROR] Python 3.10+ was not found on your system!
            echo [+] Attempting automatic installation via winget...
            winget install --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
            if %errorlevel% neq 0 (
                echo Please install Python 3.11 manually from https://www.python.org/downloads/
                echo IMPORTANT: Ensure you check "Add Python to PATH" during installation.
                pause
                exit /b 1
            )
            set PYTHON_CMD=python
        )
    )
)

echo [*] Detected Python Engine: %PYTHON_CMD%

:: 2. Check Port 8000 & Existing Instance
netstat -ano | findstr /R /C:":8000 .*LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Port 8000 is active. Checking service responsiveness...
    curl -s -f http://127.0.0.1:8000/api/session >nul 2>nul
    if %errorlevel% equ 0 (
        echo [✓] Legal Metrology Workbench is already active! Opening browser...
        start http://127.0.0.1:8000
        exit /b 0
    )
)

:: 3. Check / Create Virtual Environment
set VENV_PYTHON=.venv\Scripts\python.exe
if not exist "%VENV_PYTHON%" (
    echo [+] Creating Python virtual environment in .venv...
    where uv >nul 2>nul
    if %errorlevel% equ 0 (
        uv venv .venv
        uv pip install --python "%VENV_PYTHON%" -r requirements.txt
    ) else (
        %PYTHON_CMD% -m venv .venv
        call .venv\Scripts\activate.bat
        python -m pip install --upgrade pip
        python -m pip install --prefer-binary -r requirements.txt
    )
) else (
    call .venv\Scripts\activate.bat
)

:: 4. Verify Dependencies
"%VENV_PYTHON%" -c "import fastapi, uvicorn, pydantic, cryptography, qrcode" >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Installing / updating required dependencies...
    pip install --prefer-binary -r requirements.txt
)

:: 5. Resolve Source Directory
set APP_DIR_TARGET=backend
if not exist "backend\api" (
    if exist "src\api" (
        set APP_DIR_TARGET=src
    )
)

set PYTHONPATH=%CD%\backend;%CD%\src;%PYTHONPATH%

echo.
echo [✓] System Environment Verified!
echo [+] Starting Metrology Workbench on http://127.0.0.1:8000 (and LAN 0.0.0.0:8000)...
echo.

:: 6. Launch browser in background after 2 seconds
start "" cmd /c "timeout /t 2 >nul && start http://127.0.0.1:8000"

:: 7. Start ASGI Server
"%VENV_PYTHON%" -m uvicorn api.main:app --app-dir %APP_DIR_TARGET% --host 0.0.0.0 --port 8000 --reload

pause
