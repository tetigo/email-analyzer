"""
Classifier module.

Treina um modelo simples de machine learning (TF-IDF + Regressão Logística)
para classificar emails em 'Produtivo' ou 'Improdutivo'.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# dataset pequeno para inicializar (melhore com mais exemplos)
SAMPLES = [
    ("Preciso da atualização do pedido #123", "Produtivo"),
    ("Envio em anexo os contratos assinados", "Produtivo"),
    ("Olá, tudo bem? Só passando para desejar boas festas", "Improdutivo"),
    ("Obrigado pelo suporte até agora", "Improdutivo"),
    ("Solicito análise do saldo e estorno", "Produtivo"),
    ("Parabéns pela equipe, excelente trabalho", "Improdutivo"),
    ("Favor confirmar o recebimento do relatório", "Produtivo"),
    ("Segue planilha atualizada com os valores corretos", "Produtivo"),
    ("Bom dia, só passando para avisar que chegarei atrasado", "Improdutivo"),
    ("Obrigado pelo café de ontem, estava ótimo", "Improdutivo"),
    ("Preciso que seja liberado o acesso ao sistema hoje", "Produtivo"),
    ("Segue minuta revisada do contrato para conferência", "Produtivo"),
    ("Adorei a palestra de hoje, muito inspiradora", "Improdutivo"),
    ("Solicito confirmação de presença na reunião de amanhã", "Produtivo"),
    ("Segue print da tela com o erro encontrado", "Produtivo"),
    ("Oi! Como você está? Faz tempo que não nos falamos", "Improdutivo"),
    ("Excelente trabalho no projeto X, parabéns a todos", "Improdutivo"),
    ("Favor atualizar os dados cadastrais do cliente", "Produtivo"),
    ("Só passando para desejar um ótimo fim de semana", "Improdutivo"),
]


texts = [x for x, _ in SAMPLES]
labels = [y for _, y in SAMPLES]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = LogisticRegression()
model.fit(X, labels)


def predict_with_confidence(preprocessed_text: str):
    """
    Prediz a categoria de um texto já pré-processado e retorna
    a classe mais provável e sua confiança (probabilidade).

    Args:
        preprocessed_text (str): Texto limpo após pré-processamento.

    Returns:
        tuple[str, float]: Categoria prevista e confiança associada.
    """

    x_new = vectorizer.transform([preprocessed_text])
    probs = model.predict_proba(x_new)[0]
    idx = probs.argmax()
    return model.classes_[idx], float(probs[idx])
