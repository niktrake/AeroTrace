import React from "react";

function CaseDashboard({ caseData }) {
  return (
    <div style={{ padding: "30px" }}>
      <h2>Case Dashboard</h2>
      <p><strong>Case Name:</strong> {caseData.caseName}</p>
      <p><strong>Examiner:</strong> {caseData.examiner}</p>

      <hr />

      <h3>Upload Drone Data</h3>
      <input type="file" multiple />

      <hr />

      <h3>Analysis Results</h3>
      <p>Flight Path: Pending</p>
      <p>Restricted Airspace Violations: Pending</p>
      <p>Operator Identity: Pending</p>
    </div>
  );
}

export default CaseDashboard;