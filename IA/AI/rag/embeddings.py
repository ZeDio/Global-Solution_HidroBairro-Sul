import numpy as np
from config import client, EMBEDDING_MODEL


def preparar_pergunta(pergunta: str) -> str:
    """Prepara uma consulta para recuperação semântica assimétrica."""
    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")
    # Prefixo recomendado para tarefas de pergunta e resposta no Gemini Embedding 2.
    return f"task: question answering | query: {pergunta.strip()}"


def preparar_documento(titulo: str, conteudo: str) -> str:
    """Prepara o conteúdo documental para indexação."""
    if not isinstance(conteudo, str) or not conteudo.strip():
        raise ValueError("O conteúdo do documento está vazio.")
    titulo = titulo.strip() if isinstance(titulo, str) and titulo.strip() else "Sem título"
    return f"title: {titulo} | text: {conteudo.strip()}"


def gerar_embedding(texto: str) -> np.ndarray:
    """Gera e valida um vetor usando o Gemini Embedding 2."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Não é possível gerar embedding de texto vazio.")

    resultado = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texto,
    )
    if not resultado.embeddings or not resultado.embeddings[0].values:
        raise RuntimeError("O Gemini não retornou um embedding válido.")

    vetor = np.asarray(resultado.embeddings[0].values, dtype=np.float32)
    if vetor.ndim != 1 or vetor.size == 0 or not np.all(np.isfinite(vetor)):
        raise RuntimeError("O Gemini retornou um vetor inválido.")
    return vetor


if __name__ == "__main__":
    texto = preparar_pergunta("Como evitar acidentes durante um alagamento?")
    vetor = gerar_embedding(texto)
    print("\nHIDROBAIRRO SUL — TESTE DE EMBEDDING")
    print("=" * 50)
    print(f"Modelo: {EMBEDDING_MODEL}")
    print(f"Dimensões: {vetor.shape[0]}")
    print(f"Tipo: {vetor.dtype}")
    print(f"Primeiros valores: {vetor[:8]}")
