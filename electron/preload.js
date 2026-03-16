const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  createCase: (data) => ipcRenderer.invoke("create-case", data),
  openCase: () => ipcRenderer.invoke("open-case"),
  selectCaseDirectory: () => ipcRenderer.invoke("select-case-directory"),
   importDroneFolder: () => ipcRenderer.invoke("import-drone-folder")
});