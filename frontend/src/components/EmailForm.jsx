import React, { useState, useRef } from "react";
import EmailResult from "./EmailResult";
import "./EmailForm.css";

const EmailForm = ({ onSubmit }) => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [result, setResult] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);

    const droppedFile = e.dataTransfer.files && e.dataTransfer.files[0];
    if (droppedFile) {
      if (!/\.pdf$|\.txt$/i.test(droppedFile.name)) {
        setError("Formato inválido. Use .pdf ou .txt");
        return;
      }
      setFile(droppedFile);
      setError("");
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file && !text.trim()) {
      setError("Envie um arquivo ou digite o texto do email.");
      return;
    }

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (text.trim()) formData.append("my_text", text);

    try {
      const response = await fetch("https://emailcategorizer-i9fv.onrender.com/categorize", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.my_result);
        setError("");
      } else {
        setError(data.error || "Erro ao enviar email");
      }
    } catch (err) {
      setError("Não foi possível conectar ao servidor.");
    }
  };

  return (
    <div className="email-form-container">
      <h3>
        Adicione o seu email para classificação em uma das duas formas abaixo
      </h3>

      <form onSubmit={handleSubmit} className="email-form">
        <div className={`form-group ${error ? "error" : ""}`}>
          <label>Upload de email</label>

          {/* Drop Zone */}
          <div
            className={`file-upload-wrapper drop-zone ${
              dragOver ? "dragover" : ""
            }`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
          >
            <input
              ref={fileInputRef}
              type="file"
              id="fileUpload"
              accept=".pdf,.txt"
              onChange={handleFileChange}
            />
            <label
              htmlFor="fileUpload"
              className={`custom-file-button ${error ? "error" : ""}`}
            >
              {file ? file.name : "Escolher ou arrastar arquivo"}
            </label>
          </div>

          <small className="file-info">
            Aceita arquivo em formato .pdf ou .txt
          </small>
        </div>

        <div className={`form-group ${error ? "error" : ""}`}>
          <label>Digite o texto do email</label>
          <textarea
            rows="15"
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              if (e.target.value.trim()) setError("");
            }}
            placeholder="Digite o seu texto aqui..."
          ></textarea>
        </div>

        {error && <small className="error-text">{error}</small>}

        <button type="submit" className="submit-button">
          Enviar
        </button>
      </form>

      <EmailResult result={result} onClose={() => setResult(null)} />
    </div>
  );
};

export default EmailForm;
