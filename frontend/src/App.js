import React, { useState } from "react";
import StartupScreen from "./components/StartupScreen";
import NewCaseWizard from "./components/NewCaseWizard";
import CaseDashboard from "./components/CaseDashboard";

function App() {
  const [screen, setScreen] = useState("startup");
  const [caseData, setCaseData] = useState(null);

  return (
    <>
      {screen === "startup" && (
        <StartupScreen onNewCase={() => setScreen("newcase")} />
      )}

      {screen === "newcase" && (
        <NewCaseWizard
          onFinish={(data) => {
            setCaseData(data);
            setScreen("dashboard");
          }}
        />
      )}

      {screen === "dashboard" && (
        <CaseDashboard caseData={caseData} />
      )}
    </>
  );
}

export default App;