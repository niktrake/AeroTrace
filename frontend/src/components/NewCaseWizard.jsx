import React, { useState } from "react";

function NewCaseWizard({ onFinish }) {
  const [caseName, setCaseName] = useState("");
  const [examiner, setExaminer] = useState("");

  return (
    <div style={{ padding: "50px" }}>
      <h2>Create New Case</h2>

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
      

      <button onClick={async () => {
        const result = await window.electronAPI.createCase({
            caseName,
            examiner
        });

        if (result.success) {
            onFinish({ caseName, examiner, casePath: result.casePath });
        } else {
            alert(result.error);
        }
    }}
    >
            Finish
        </button>
    </div>
  );
}

export default NewCaseWizard;