const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  createCase: (data) => ipcRenderer.invoke("create-case", data)
});