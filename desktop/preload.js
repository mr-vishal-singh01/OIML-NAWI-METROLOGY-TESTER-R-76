// Preload Script for Legal Metrology Workbench Desktop App
// Provides secure, isolated IPC bridges between Electron main and renderer processes

const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  getAppVersion: () => ipcRenderer.invoke("app:get-version"),
  getPlatform: () => ipcRenderer.invoke("app:get-platform"),
  openExternal: (url) => ipcRenderer.invoke("app:open-external", url),
  printToPdf: () => ipcRenderer.invoke("app:print-pdf"),
  scanSerialPorts: () => ipcRenderer.invoke("scale:scan-ports"),
  onBackendStatusChange: (callback) => ipcRenderer.on("backend:status", (event, status) => callback(status))
});
