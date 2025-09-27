import os
import requests

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise ValueError(
        "Token não encontrado! Configure HUGGINGFACEHUB_API_TOKEN antes de rodar o script."
    )


def categorize_email_with_reply(text):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["produtivo", "improdutivo"]}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(
            f"Erro na API: {response.status_code} - {response.text}")

    result = response.json()
    labels = result.get("labels", [])
    scores = result.get("scores", [])
    if not labels or not scores:
        raise Exception("Resposta inesperada da API: " + str(result))

    classification = labels[0]

    # Sugestão de resposta baseada na classificação
    if classification == "produtivo":
        suggested_reply = "Obrigado pelo seu email. Vamos tomar as providências necessárias."
    else:
        suggested_reply = "Obrigado pelo seu email. Encaminharemos caso seja necessário."

    return {
        "classification": classification,
        "suggested_reply": suggested_reply
    }
