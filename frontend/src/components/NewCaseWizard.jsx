import React, { useState } from "react";

function NewCaseWizard({ onFinish }) {
  const [caseName, setCaseName] = useState("");
  const [examiner, setExaminer] = useState("");
  const [basePath, setBasePath] = useState("");
  const [step, setStep] = useState(1);

  return (
    <div style={{ padding: "50px" }}>
            {step === 1 && (
  <div>
    <h2>Step 1 — Case Information</h2>

    <input
      placeholder="Case Name"
      value={caseName}
      onChange={(e) => setCaseName(e.target.value)}
    />
    <br /><br />

    <input
      placeholder="Examiner Name (Optional)"
      value={examiner}
      onChange={(e) => setExaminer(e.target.value)}
    />
    <br /><br />

    <button
      onClick={() => {
        if (!caseName) {
          alert("Case name required");
          return;
        }
        setStep(2);
      }}
    >
      Next →
    </button>
  </div>
)}

        {step === 2 && (
  <div>
    <h2>Step 2 — Select Case Location</h2>

    <button
      onClick={async () => {
        const result = await window.electronAPI.selectCaseDirectory();

        if (result.success) {
          setBasePath(result.path);
        }
      }}
    >
      Select Case Directory
    </button>

    <br /><br />

    {basePath && <p>Selected: {basePath}</p>}

    <br />

    <button onClick={() => setStep(1)}>
      ← Back
    </button>

    <button
      onClick={() => {
        if (!basePath) {
          alert("Please select a directory");
          return;
        }
        setStep(3);
      }}
    >
      Next →
    </button>
  </div>
)}


          {step === 3 && (
  <div>
    <h2>Step 3 — Confirm Case</h2>

    <p><strong>Case Name:</strong> {caseName}</p>
    <p><strong>Examiner:</strong> {examiner || "Not specified"}</p>
    <p><strong>Directory:</strong> {basePath}</p>

    <br />

    <button onClick={() => setStep(2)}>
      ← Back
    </button>

    <button
      onClick={async () => {
        const result = await window.electronAPI.createCase({
          caseName,
          examiner,
          basePath
        });

        if (result.success) {
          onFinish({
            caseName,
            examiner,
            casePath: result.casePath
          });
        } else {
          alert(result.error);
        }
      }}
    >
      Finish
    </button>
  </div>
)}
      
    </div>
  );
}

export default NewCaseWizard;