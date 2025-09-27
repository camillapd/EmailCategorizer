import "./App.css";
import EmailForm from "./components/EmailForm";
import React from "react";

function App() {
  const handleEmailSubmit = (data) => {
    console.log("Email enviado:", data);
    // Aqui você chamaria o backend para classificar o email
  };

  return (
    <div>
      <EmailForm onSubmit={handleEmailSubmit} />
    </div>
  );
}

export default App;
