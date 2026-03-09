import React from "react";

function StartupScreen({ onNewCase }) {
  return (
    <div style={{ textAlign: "center", marginTop: "150px" }}>
      <h1>Drone Forensics Tool</h1>
      <button onClick={onNewCase}>New Case</button>
      <br /><br />
      <button 
        onClick={ async () => {
          const result = await window.electronAPI.openCase();
          if(result.success){
            onNewCase(result.caseData, result.casePath);
          }else if(result.error){
            alert(result.error);
          }
        }}
      >Open Case</button>
    </div>
  );
}

export default StartupScreen;