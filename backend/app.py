from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import read_emails as re
import categorize_emails as ce
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app) 

load_dotenv() 

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise ValueError("Token não encontrado!")

@app.route("/categorize", methods=["POST"])
def categorize_email():
    content = ""

    if "file" in request.files:
        uploaded_file = request.files["file"]
        content = re.read_uploaded_file(uploaded_file)

    elif "my_text" in request.form:
        content = request.form["my_text"]

    else:
        return jsonify({"error": "Nenhum texto ou arquivo enviado"}), 400

    processed_text = re.preprocess_text(content)
    result = ce.categorize_email_with_reply(processed_text)

    return jsonify({"status": "ok", "my_result": result})

if __name__ == "__main__":
    # host=0.0.0.0 permite acesso externo (necessário no Render/Railway)
    app.run(host="0.0.0.0", port=5000, debug=False)
