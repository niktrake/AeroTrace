const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");
const fs = require("fs");
let currentCasePath = null;
const crypto = require("crypto");


const isDev = require("electron-is-dev")

function createWindow() {
  const win = new BrowserWindow({
    
    width: 1200,
    height: 800,
    backgroundColor: "#5678d4",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

 win.loadURL("http://localhost:3000"); // React dev server
//   win.loadURL(
//     isDev
//       ? 'http://localhost:3000'
//       : `file://${path.join(__dirname, '../build/index.html')}`
//   )
}

app.whenReady().then(createWindow);

//handle case creation
ipcMain.handle("create-case", async (event, caseData) => {
    try{
        const basePath = caseData.basePath || path.join(__dirname, "..", "cases");

        // Create cases folder if not exists
        if (!fs.existsSync(basePath)) {
        fs.mkdirSync(basePath);
        }

        //now create folder with casename and in same folder create other 3 dirs 
        const casePath = path.join(basePath, caseData.caseName);
        //if case already exists
        if (fs.existsSync(casePath)) {
            return { success: false, error: "Case already exists" };
        }

        fs.mkdirSync(casePath);
        fs.mkdirSync(path.join(casePath, "evidence"));
        fs.mkdirSync(path.join(casePath, "analysis"));
        fs.mkdirSync(path.join(casePath, "reports"));
        
        //added for import drone folder 
        currentCasePath = casePath;

        //creating a metadata.json file, containing metadata about the case
        const metadata = {
        caseName: caseData.caseName,
        examiner: caseData.examiner,
        createdAt: new Date().toISOString(),
        status: "Open"
        };

        fs.writeFileSync(
            path.join(casePath, "case_metadata.json"),
            JSON.stringify(metadata, null, 2)
        );

        //return success
        return { success: true, casePath };


    }
    catch(error){
        return { success: false, error: error.message}
    }
})

//handling open case event
ipcMain.handle("open-case", async () => {
  try {
    const result = await dialog.showOpenDialog({
      properties: ["openDirectory"]
    });

    if (result.canceled) {
      return { success: false };
    }

    const selectedPath = result.filePaths[0];
    const metadataPath = path.join(selectedPath, "case_metadata.json");

    if (!fs.existsSync(metadataPath)) {
      return { success: false, error: "Invalid case folder" };
    }

    const metadata = JSON.parse(
      fs.readFileSync(metadataPath, "utf-8")
    );

    return {
      success: true,
      caseData: metadata,
      casePath: selectedPath
    };

  } catch (error) {
    return { success: false, error: error.message };
  }
});


//user selecting the case directory
ipcMain.handle("select-case-directory", async () => {

  const result = await dialog.showOpenDialog({
    properties: ["openDirectory"]
  });

  if (result.canceled) {
    return { success: false };
  }

  return {
    success: true,
    path: result.filePaths[0]
  };
});


//ipc handler for uploading drone data 

function scanDirectory(dirPath) {

  let files = [];

  const items = fs.readdirSync(dirPath);

  for (const item of items) {

    const fullPath = path.join(dirPath, item);

    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      files = files.concat(scanDirectory(fullPath));
    } 
    else {
      files.push(fullPath);
    }

  }

  return files;
}

function ensureEvidenceFolder(casePath) {

  const evidencePath = path.join(casePath, "evidence", "original");

  if (!fs.existsSync(evidencePath)) {
    fs.mkdirSync(evidencePath, { recursive: true });
  }

  return evidencePath;
}

function classifyFile(filePath) {

  const ext = path.extname(filePath).toLowerCase();

  if ([".mp4", ".mov"].includes(ext)) return "video";

  if ([".jpg", ".jpeg", ".dng"].includes(ext)) return "image";

  if ([".csv"].includes(ext)) return "telemetry";

  if ([".dat"].includes(ext)) return "flight_log";

  if ([".json", ".cfg"].includes(ext)) return "config";

  return "unknown";
}



function generateHash(filePath) {

  const buffer = fs.readFileSync(filePath);

  return crypto
    .createHash("sha256")
    .update(buffer)
    .digest("hex");

}


function createEvidenceObject(filePath) {

  const stat = fs.statSync(filePath);

  return {

    id: crypto.randomUUID(),

    filename: path.basename(filePath),

    path: filePath,

    size: stat.size,

    type: classifyFile(filePath),

    hash: generateHash(filePath),

    importedAt: new Date().toISOString()

  };

}

ipcMain.handle("import-drone-folder", async () => {

  const result = await dialog.showOpenDialog({
    properties: ["openDirectory"]
  });

  if (result.canceled) return { success: false };

  const folderPath = result.filePaths[0];

  const files = scanDirectory(folderPath);

  const evidenceDir = ensureEvidenceFolder(currentCasePath);

  const evidenceList = [];

  for (const file of files) {

    const filename = path.basename(file);

    const destination = path.join(evidenceDir, filename);

    fs.copyFileSync(file, destination);

    const evidence = createEvidenceObject(destination);

    evidenceList.push(evidence);

  }

  fs.writeFileSync(
    path.join(currentCasePath, "analysis", "evidence_index.json"),
    JSON.stringify(evidenceList, null, 2)
  );

  return { success: true };

});