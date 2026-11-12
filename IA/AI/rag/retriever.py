import json
import numpy as np
from config import RAG_INDEX_PATH
from .embeddings import gerar_embedding, preparar_pergunta

PROJECT_PREFIX = "hidrobairro::"


def similaridade_cosseno(vetor_a: np.ndarray, vetor_b: np.ndarray) -> float:
    denominador = np.linalg.norm(vetor_a) * np.linalg.norm(vetor_b)
    if denominador == 0:
        return 0.0
    return float(np.dot(vetor_a, vetor_b) / denominador)


def carregar_indice() -> list[dict]:
    if not RAG_INDEX_PATH.is_file():
        raise FileNotFoundError("Índice RAG não encontrado. Execute: python -m rag.indexer")
    try:
        indice = json.loads(RAG_INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as erro:
        raise ValueError("O arquivo index.json está inválido ou não pôde ser lido.") from erro
    if not isinstance(indice, list):
        raise ValueError("O arquivo index.json não contém uma lista válida.")

    registros = []
    dimensao = None
    for item in indice:
        if not isinstance(item, dict):
            continue
        if not isinstance(item.get("id"), str) or not item["id"].startswith(PROJECT_PREFIX):
            continue
        if not all(isinstance(item.get(campo), str) and item[campo].strip() for campo in ("texto", "fonte", "titulo")):
            continue
        embedding = item.get("embedding")
        if not isinstance(embedding, list) or not embedding:
            continue
        try:
            vetor = np.asarray(embedding, dtype=np.float32)
        except (TypeError, ValueError):
            continue
        if vetor.ndim != 1 or not np.all(np.isfinite(vetor)):
            continue
        if dimensao is None:
            dimensao = vetor.shape
        if vetor.shape != dimensao:
            continue
        registros.append(item)

    if not registros:
        raise ValueError("Nenhum embedding válido do HidroBairro Sul foi encontrado. Gere o índice com 'python -m rag.indexer'.")
    return registros


def indice_disponivel() -> tuple[bool, str | None, int]:
    """Verifica o índice sem chamar a API Gemini."""
    try:
        indice = carregar_indice()
        return True, None, len(indice)
    except (FileNotFoundError, ValueError) as erro:
        return False, str(erro), 0


def buscar_trechos(pergunta: str, k: int = 5) -> list[dict]:
    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")
    if not isinstance(k, int) or isinstance(k, bool) or not 1 <= k <= 10:
        raise ValueError("O parâmetro k precisa ser um inteiro entre 1 e 10.")

    indice = carregar_indice()
    vetor_pergunta = gerar_embedding(preparar_pergunta(pergunta.strip()))
    resultados = []
    for item in indice:
        vetor_documento = np.asarray(item["embedding"], dtype=np.float32)
        if vetor_documento.shape != vetor_pergunta.shape:
            continue
        score = similaridade_cosseno(vetor_pergunta, vetor_documento)
        resultados.append({
            "id": item["id"], "fonte": item["fonte"],
            "titulo": item["titulo"], "texto": item["texto"],
            "similaridade": score,
        })
    resultados.sort(key=lambda item: item["similaridade"], reverse=True)
    return resultados[:k]


if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ").strip()
    if not pergunta:
        raise SystemExit("Digite uma pergunta válida.")
    for item in buscar_trechos(pergunta, k=5):
        print(f"\n[{item['fonte']}] — similaridade: {item['similaridade']:.4f}")
        print(item["texto"][:500])
