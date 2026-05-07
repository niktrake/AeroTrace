import React, { useState, useEffect } from "react";

function CaseDashboard({ caseData }) {

  const [uploadProgress, setUploadProgress] = useState(0);

  const [currentFile, setCurrentFile] = useState("");

  const [isUploading, setIsUploading] = useState(false);
  useEffect(() => {

  window.electronAPI.onUploadProgress((data) => {

    setUploadProgress(data.progress);

    setCurrentFile(data.currentFile);

  });

}, []);
  return (
    <div style={{ padding: "30px" }}>
      <h2>Case Dashboard</h2>
      <p><strong>Case Name:</strong> {caseData.caseName}</p>
      <p><strong>Examiner:</strong> {caseData.examiner}</p>

      <hr />
      <button
  onClick={async () => {

    setIsUploading(true);

    setUploadProgress(0);

    const result = await window.electronAPI.importDroneFolder();

    setIsUploading(false);

    if (result.success) {
      alert("Drone data imported successfully");
    } else {
      alert("Import cancelled");
    }
  }}
>
Import Drone Data
</button>
    {isUploading && (

  <div style={{ marginTop: "20px", width: "400px" }}>

    <div
      style={{
        width: "100%",
        height: "25px",
        backgroundColor: "#ddd",
        borderRadius: "10px",
        overflow: "hidden"
      }}
    >

      <div
        style={{
          width: `${uploadProgress}%`,
          height: "100%",
          backgroundColor: "#4caf50",
          transition: "0.3s"
        }}
      />

    </div>

    <p>{uploadProgress}% Uploading...</p>

    <small>{currentFile}</small>

  </div>

)}

     

      <hr />

      <h3>Analysis Results</h3>
      <p>Flight Path: Pending</p>
      <p>Restricted Airspace Violations: Pending</p>
      <p>Operator Identity: Pending</p>
    </div>
  );
}

export default CaseDashboard;