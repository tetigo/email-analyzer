"""
AutoU Backend - API de classificação de emails.

- Recebe texto ou arquivo (txt/pdf)
- Pré-processa com NLP
- Classifica (Produtivo / Improdutivo)
- Gera resposta automática (OpenAI ou template)
"""

from io import BytesIO

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pdfminer.high_level import extract_text

import classifier
import nlp_utils
import openai_client

app = FastAPI(title="AutoU Email Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/process-email")
async def process_email(file: UploadFile = File(None), text: str = Form(None)):
    """
    Endpoint principal da API.

    - Recebe texto ou arquivo (.txt/.pdf).
    - Extrai o conteúdo e pré-processa.
    - Classifica como Produtivo/Improdutivo.
    - Gera resposta automática (LLM ou template).
    - Retorna JSON com categoria, confiança e resposta sugerida.
    """
    if not file and not text:
        return JSONResponse(
            {"error": "Nenhum texto ou arquivo enviado."}, status_code=400
        )

    # extrair texto
    content = ""
    if file:
        contents = await file.read()
        if file.content_type == "application/pdf":
            content = extract_text(BytesIO(contents))
        else:
            try:
                content = contents.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                content = str(contents)
    elif text:
        content = text

    cleaned = nlp_utils.preprocess(content)
    category, confidence = classifier.predict_with_confidence(cleaned)

    # gerar sugestão via LLM (fallback para template se sem API)
    suggested = openai_client.generate_suggestion(content, category)

    return {
        "category": category,
        "confidence": confidence,
        "suggested_response": suggested,
        "excerpt": content[:300],
    }


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
