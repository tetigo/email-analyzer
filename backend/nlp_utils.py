"""
Natural Language Processing (NLP) utilities.

Este módulo contém funções para pré-processamento de texto:
- limpeza de URLs e caracteres especiais
- tokenização
- remoção de stopwords (português)
- lematização
"""

import os
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

NLTK_DATA_DIR = os.getenv("NLTK_DATA", "/tmp/nltk_data")
nltk.data.path.append(NLTK_DATA_DIR)

# downloads só se necessário
for r in ["punkt", "punkt_tab", "stopwords", "wordnet"]:
    try:
        nltk.data.find(f"{r}")
    except LookupError:
        nltk.download(r, download_dir=NLTK_DATA_DIR)


STOPWORDS_PT = (
    set(stopwords.words("portuguese")) if "portuguese" in stopwords.fileids()
    else set()
)
lemmatizer = WordNetLemmatizer()


def preprocess(text: str) -> str:
    """
    Realiza o pré-processamento de um texto:
    - converte para minúsculas
    - remove URLs e caracteres especiais
    - tokeniza
    - remove stopwords
    - aplica lematização

    Args:
        text (str): Texto original.

    Returns:
        str: Texto pré-processado pronto para classificação.
    """

    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-záàâãéèêíïóôõöúçñ ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if len(t) > 2]
    tokens = [t for t in tokens if t not in STOPWORDS_PT]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)
