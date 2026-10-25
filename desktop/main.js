// ==============================================================================
// SIH26035: Automated OIML R-76 Guided NAWI Testing Suite
// Electron Native Desktop Main Process (Windows, Linux, Raspberry Pi, macOS)
// Team PrecisionX — Ministry of Consumer Affairs
// ==============================================================================

const { app, BrowserWindow, ipcMain, shell, dialog } = require("electron");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");
const http = require("http");

// Disable Linux SUID sandbox restriction for seamless operation across modern Linux distributions (Ubuntu 24.04 / Debian 12)
if (process.platform === "linux") {
  app.commandLine.appendSwitch("no-sandbox");
  app.commandLine.appendSwitch("disable-gpu-sandbox");
}

let mainWindow = null;
let backendProcess = null;
const BACKEND_PORT = process.env.PORT || 8000;
const BACKEND_HOST = "127.0.0.1";
const BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

// Resolve backend directory (packaged extraResources vs local development)
function getBackendDirectory() {
  const packagedBackend = path.join(process.resourcesPath || "", "backend");
  if (fs.existsSync(packagedBackend)) return packagedBackend;

  const devBackend = path.join(__dirname, "..", "backend");
  if (fs.existsSync(devBackend)) return devBackend;

  const devSrc = path.join(__dirname, "..", "src");
  if (fs.existsSync(devSrc)) return devSrc;

  return devBackend;
}

// Determine python binary path across platforms without hardcoded paths
function getPythonCommand() {
  if (process.env.PYTHON_PATH && fs.existsSync(process.env.PYTHON_PATH)) {
    return process.env.PYTHON_PATH;
  }

  const baseDir = path.join(__dirname, "..");
  const parentDir = path.join(__dirname, "..", "..");

  if (process.platform === "win32") {
    // Windows check
    const candidates = [
      path.join(baseDir, ".venv", "Scripts", "python.exe"),
      path.join(parentDir, "SIH HACKATHON", ".venv", "Scripts", "python.exe"),
      path.join(parentDir, "SIH APP", ".venv", "Scripts", "python.exe")
    ];
    for (const p of candidates) {
      if (fs.existsSync(p)) return p;
    }
    return "python";
  } else {
    // Linux / macOS / Raspberry Pi check
    const candidates = [
      path.join(baseDir, ".venv", "bin", "python"),
      path.join(baseDir, ".venv", "bin", "python3"),
      path.join(parentDir, "SIH HACKATHON", ".venv", "bin", "python"),
      path.join(parentDir, "SIH APP", ".venv", "bin", "python")
    ];
    for (const p of candidates) {
      if (fs.existsSync(p)) return p;
    }
    return "python3";
  }
}

// Ping backend to check when it is ready
function waitForBackend(callback, retries = 40) {
  if (retries <= 0) {
    dialog.showErrorBox(
      "Backend Startup Timeout",
      "The Legal Metrology calculation engine did not respond in time.\nPlease ensure Python 3.10+ and requirements are installed."
    );
    return;
  }

  const req = http.get(`${BACKEND_URL}/api/session`, (res) => {
    if (res.statusCode === 200) {
      callback();
    } else {
      setTimeout(() => waitForBackend(callback, retries - 1), 400);
    }
  });

  req.on("error", () => {
    setTimeout(() => waitForBackend(callback, retries - 1), 400);
  });
}

// Spawn Python backend process
function startBackendService() {
  const pythonCmd = getPythonCommand();
  const backendDir = getBackendDirectory();

  console.log(`[+] Starting Python backend with: ${pythonCmd}`);
  console.log(`[+] Backend directory: ${backendDir}`);

  backendProcess = spawn(
    pythonCmd,
    [
      "-m",
      "uvicorn",
      "api.main:app",
      "--app-dir",
      backendDir,
      "--host",
      BACKEND_HOST,
      "--port",
      BACKEND_PORT.toString()
    ],
    {
      cwd: path.join(__dirname, ".."),
      env: {
        ...process.env,
        PYTHONPATH: `${backendDir}${path.delimiter}${process.env.PYTHONPATH || ""}`
      }
    }
  );

  backendProcess.stdout.on("data", (data) => {
    console.log(`[Backend] ${data.toString().trim()}`);
  });

  backendProcess.stderr.on("data", (data) => {
    console.error(`[Backend ERR] ${data.toString().trim()}`);
  });

  backendProcess.on("close", (code) => {
    console.log(`[Backend] Process exited with code ${code}`);
  });
}

function createMainWindow() {
  const oimlIcon = path.join(__dirname, "assets", "OIML_R76_Tester_Badge.png");
  const iconPath = fs.existsSync(oimlIcon)
    ? oimlIcon
    : (process.platform === "win32"
      ? path.join(__dirname, "assets", "icon.ico")
      : path.join(__dirname, "assets", "icon.png"));

  mainWindow = new BrowserWindow({
    width: 1360,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    title: "PrecisionX — OIML R-76 Legal Metrology Workbench (SIH26035)",
    icon: fs.existsSync(iconPath) ? iconPath : undefined,
    backgroundColor: "#020617",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });

  mainWindow.loadURL(BACKEND_URL);

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

// Native IPC Handlers
ipcMain.handle("app:get-version", () => app.getVersion());
ipcMain.handle("app:get-platform", () => process.platform);
ipcMain.handle("app:open-external", (event, url) => shell.openExternal(url));

app.whenReady().then(() => {
  // Check if server is already running (e.g. from background or external process)
  const probe = http.get(`${BACKEND_URL}/api/session`, (res) => {
    if (res.statusCode === 200) {
      console.log("[*] Backend service already running. Connecting directly...");
      createMainWindow();
    } else {
      startBackendService();
      waitForBackend(createMainWindow);
    }
  });

  probe.on("error", () => {
    startBackendService();
    waitForBackend(createMainWindow);
  });

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createMainWindow();
  });
});

// Clean up child process on exit
app.on("before-quit", () => {
  if (backendProcess) {
    console.log("[*] Terminating backend process...");
    backendProcess.kill();
    backendProcess = null;
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
