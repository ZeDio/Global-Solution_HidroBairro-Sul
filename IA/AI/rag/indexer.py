import json
import re
from pathlib import Path

from config import MATERIAL_DIR, RAG_INDEX_PATH
from .embeddings import gerar_embedding, preparar_documento

CHUNK_SIZE = 1800
CHUNK_OVERLAP = 250
PROJECT_PREFIX = "hidrobairro::"


def limpar_markdown(texto: str) -> str:
    texto = re.sub(r"```[\s\S]*?```", " ", texto)
    texto = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", texto)
    texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)
    texto = re.sub(r"^#{1,6}\s*", "", texto, flags=re.MULTILINE)
    texto = re.sub(r"[*_`~]", "", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def titulo_do_markdown(texto: str, caminho: Path) -> str:
    match = re.search(r"^\s*#\s+(.+?)\s*$", texto, flags=re.MULTILINE)
    return match.group(1).strip() if match else caminho.stem.replace("-", " ").replace("_", " ").title()


def criar_chunks(texto: str, tamanho: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if tamanho <= 0 or overlap < 0 or overlap >= tamanho:
        raise ValueError("Configuração de chunks inválida.")
    texto = texto.strip()
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        chunk = texto[inicio:fim].strip()
        if chunk:
            chunks.append(chunk)
        if fim >= len(texto):
            break
        inicio = fim - overlap
    return chunks


def criar_documentos() -> list[dict]:
    if not MATERIAL_DIR.is_dir():
        raise FileNotFoundError(f"Base de conhecimento não encontrada: {MATERIAL_DIR}")
    arquivos = sorted(p for p in MATERIAL_DIR.rglob("*.md") if p.is_file())
    if not arquivos:
        raise FileNotFoundError(f"Nenhum Markdown encontrado em {MATERIAL_DIR}")

    documentos = []
    for caminho in arquivos:
        original = caminho.read_text(encoding="utf-8", errors="replace")
        titulo = titulo_do_markdown(original, caminho)
        texto = limpar_markdown(original)
        fonte = caminho.relative_to(MATERIAL_DIR).as_posix()
        for numero, chunk in enumerate(criar_chunks(texto)):
            documentos.append({
                "id": f"{PROJECT_PREFIX}{fonte}::chunk-{numero}",
                "fonte": fonte,
                "titulo": titulo,
                "chunk": numero,
                "texto": chunk,
            })
    return documentos


def carregar_indice_existente(ids_validos: set[str]) -> list[dict]:
    """Mantém somente embeddings válidos da versão atual da base."""
    if not RAG_INDEX_PATH.is_file():
        return []
    try:
        indice = json.loads(RAG_INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("Aviso: índice anterior inválido; será reconstruído.")
        return []
    if not isinstance(indice, list):
        print("Aviso: formato do índice anterior inválido; será reconstruído.")
        return []

    validos = []
    for item in indice:
        if not isinstance(item, dict) or item.get("id") not in ids_validos:
            continue
        embedding = item.get("embedding")
        if (isinstance(embedding, list) and embedding
                and all(isinstance(v, (int, float)) for v in embedding)):
            validos.append(item)
    return validos


def salvar_indice(indice: list[dict]) -> None:
    RAG_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporario = RAG_INDEX_PATH.with_name(RAG_INDEX_PATH.name + ".tmp")
    temporario.write_text(json.dumps(indice, ensure_ascii=False), encoding="utf-8")
    temporario.replace(RAG_INDEX_PATH)


def construir_indice() -> None:
    documentos = criar_documentos()
    ids_validos = {doc["id"] for doc in documentos}
    indice = carregar_indice_existente(ids_validos)
    existentes = {item["id"] for item in indice}
    restantes = [doc for doc in documentos if doc["id"] not in existentes]
    total = len(documentos)

    print("\n" + "=" * 65)
    print("CONSTRUÇÃO DO ÍNDICE — HIDROBAIRRO SUL")
    print("=" * 65)
    print(f"Chunks encontrados: {total}")
    print(f"Chunks reaproveitados: {len(existentes)}")
    print(f"Chunks restantes: {len(restantes)}\n")

    if not restantes:
        salvar_indice(indice)  # também remove registros antigos de outros projetos
        print("Índice já está atualizado.")
        return

    processados = len(existentes)
    for documento in restantes:
        print(f"[{processados + 1}/{total}] {documento['fonte']} — chunk {documento['chunk']}")
        try:
            texto = preparar_documento(documento["titulo"], documento["texto"])
            vetor = gerar_embedding(texto)
            indice.append({**documento, "embedding": vetor.tolist()})
            salvar_indice(indice)
            processados += 1
            print(f"  Salvo: {processados}/{total}\n")
        except Exception as erro:
            print("\nFalha ao gerar embedding. O índice parcial foi preservado.")
            print(f"{type(erro).__name__}: {erro}")
            print("Corrija o problema e execute novamente para continuar.")
            return

    # Garante ordem estável e descarta qualquer sobra obsoleta.
    ordem = {doc["id"]: pos for pos, doc in enumerate(documentos)}
    indice = [item for item in indice if item.get("id") in ids_validos]
    indice.sort(key=lambda item: ordem[item["id"]])
    salvar_indice(indice)
    print("\nÍNDICE DO HIDROBAIRRO SUL CONCLUÍDO!")
    print(f"Total de chunks: {len(indice)}")
    print(f"Arquivo: {RAG_INDEX_PATH}")


if __name__ == "__main__":
    construir_indice()
