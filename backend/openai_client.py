"""
Cliente para integração com OpenAI.

Este módulo gera respostas automáticas a emails
usando a API da OpenAI (se disponível). Caso a chave
não esteja configurada, retorna respostas por templates.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

openai = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_KEY,
)


def generate_suggestion(original_text: str, category: str):
    """
    Gera uma sugestão de resposta a partir de um texto de email.

    Args:
        original_text (str): Texto original do email.
        category (str): Categoria detectada ("Produtivo" ou "Improdutivo").

    Returns:
        str: Resposta sugerida, vinda da API da OpenAI ou de templates locais.
    """

    # fallback templates
    if not OPENAI_KEY:
        if category == "Produtivo":
            return (
                "Olá,\n\nObrigado pelo contato. Recebemos sua solicitação e "
                "já estamos analisando. Em até 2 dias úteis retornaremos com "
                "uma posição mais detalhada.\n\nAtenciosamente,\nEquipe"
                "posição mais detalhada.\n\nAtenciosamente,\nEquipe"
            )
        return (
            "Olá,\n\nAgradecemos sua mensagem. Caso precise de algo "
            "específico, por favor nos informe.\n\nAtenciosamente,\nEquipe"
        )

    # prompt para o LLM
    prompt = (
        "Você é um assistente que gera uma resposta profissional e "
        "sucinta em português para um email. "
        f"Categoria detectada: {category}.\n\n"
        f"Email:\n{original_text}\n\n"
        "Resposta (máx 180 palavras):"
    )

    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente profissional que responde "
                        "emails em português."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=400,
        )
        text = resp.choices[0].message.content
        return text
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("Erro OpenAI:", e)
        return "Erro ao gerar com LLM. Use templates:\n\n" + (
            "(Produtivo) Obrigado, recebemos e responderemos em breve."
            if category == "Produtivo"
            else "(Improdutivo) Obrigado pela mensagem."
        )
