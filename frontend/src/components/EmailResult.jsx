import React from "react";
import "./EmailResult.css";

const EmailResult = ({ result, onClose }) => {
  if (!result) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-btn" onClick={onClose}>
          ×
        </button>
        <div className="modal-text">
          <h3>Classificação: {result.classification}</h3>
          <p>
            <strong>Sugestão de resposta:</strong> {result.suggested_reply}
          </p>
        </div>
      </div>
    </div>
  );
};

export default EmailResult;
