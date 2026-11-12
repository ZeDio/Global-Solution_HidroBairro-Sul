from pathlib import Path
import re
from urllib.parse import quote, unquote
import mistune
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from config import MATERIAL_DIR


router = APIRouter(prefix="/api", tags=["Materiais"])

# Base de conhecimento do HidroBairro Sul.
MATERIAL_DIR = MATERIAL_DIR.resolve()

# Conversor de Markdown para HTML.
# HTML escrito dentro dos documentos será escapado por segurança.
markdown = mistune.create_markdown(
    escape=True,
    plugins=["strikethrough", "table"],
)


CATEGORIAS = {
    "defesa-civil": ("Defesa Civil", "defesa-civil"),
    "informacoes-locais": ("Informações locais", "informacoes-locais"),
    "pontos-monitorados": ("Pontos de monitoramento", "pontos-monitorados"),
    "emergencias": ("Emergências", "emergencias"),
    "perguntas-frequentes": ("Perguntas frequentes", "perguntas-frequentes"),
}


def safe_material_path(relative_path: str) -> Path:
    """Resolve caminhos sem permitir acesso fora da base documental."""

    relative_path = unquote(relative_path).replace("\\", "/").lstrip("/")

    candidate = (MATERIAL_DIR / relative_path).resolve()

    try:
        candidate.relative_to(MATERIAL_DIR)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Caminho de arquivo inválido.",
        )

    return candidate


def clean_text(text: str) -> str:
    """Remove elementos Markdown para gerar textos de prévia."""

    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#*_>`~|-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def title_from_markdown(text: str, path: Path) -> str:
    """Identifica o título do documento."""

    for line in text.splitlines():
        match = re.match(r"^\s*#{1,6}\s+(.+?)\s*$", line)

        if match:
            title = clean_text(match.group(1))

            if title and title.lower() != "index":
                return title

    if path.stem.lower() in {"index", "readme"}:
        parent = path.parent.name.replace("_", " ").replace("-", " ")

        if parent:
            return parent.title()

    return path.stem.replace("_", " ").replace("-", " ").title()


def category_from_path(path: Path) -> tuple[str, str]:
    """Identifica a categoria pela pasta do documento."""

    relative = path.relative_to(MATERIAL_DIR)

    if not relative.parts:
        return "Outros", "outros"

    folder = relative.parts[0].lower()

    return CATEGORIAS.get(folder, ("Outros", "outros"))


def preview_from_markdown(text: str) -> str:
    """Gera uma prévia curta do documento."""

    lines = text.splitlines()
    paragraph = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if paragraph:
                break
            continue

        if (
            stripped.startswith("#")
            or stripped.startswith("!")
            or stripped.startswith("```")
        ):
            if paragraph:
                break
            continue

        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ")

        paragraph.append(stripped)

    result = clean_text(" ".join(paragraph))

    if len(result) < 20:
        result = clean_text(text)

    return result[:190].rstrip() + (
        "…" if len(result) > 190 else ""
    )


def rewrite_local_links(source: str, source_path: Path) -> str:
    """Adapta links relativos para as rotas da API."""

    source_dir = source_path.parent.relative_to(MATERIAL_DIR).as_posix()

    def resolve_target(target: str) -> str:
        target = target.strip().strip("<>")

        if not target or target.startswith(
            ("http://", "https://", "data:", "#", "mailto:", "/")
        ):
            return target

        match = re.match(r"([^?#]*)(.*)$", target)

        if not match:
            return target

        raw_path, suffix = match.groups()

        joined = Path(source_dir, raw_path).as_posix()

        if raw_path.lower().endswith(".md"):
            return (
                f"/api/material?arquivo={quote(joined, safe='/._-~')}"
                f"{suffix}"
            )

        return (
            f"/api/arquivo?arquivo={quote(joined, safe='/._-~')}"
            f"{suffix}"
        )

    def image_repl(match):
        alt, target = match.groups()
        return f"![{alt}]({resolve_target(target)})"

    def link_repl(match):
        label, target = match.groups()
        return f"[{label}]({resolve_target(target)})"

    source = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        image_repl,
        source,
    )

    source = re.sub(
        r"(?<!!)\[([^\]]+)\]\(([^)]+)\)",
        link_repl,
        source,
    )

    return source


def material_record(path: Path) -> dict:
    """Monta os dados públicos de um documento."""

    relative = path.relative_to(MATERIAL_DIR).as_posix()

    source = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    category, category_id = category_from_path(path)

    return {
        "arquivo": relative,
        "titulo": title_from_markdown(source, path),
        "previa": preview_from_markdown(source),
        "categoria": category,
        "categoria_id": category_id,
        "url": (
            f"/api/material?arquivo={quote(relative, safe='/._-~')}"
        ),
    }


@router.get("/materials")
def list_materials():
    """Lista os documentos Markdown da base de conhecimento."""

    if not MATERIAL_DIR.is_dir():
        return {
            "total": 0,
            "materiais": [],
        }

    files = [
        path
        for path in MATERIAL_DIR.rglob("*.md")
        if path.is_file()
    ]

    records = [
        material_record(path)
        for path in files
    ]

    records.sort(
        key=lambda item: (
            item["categoria"],
            item["titulo"].lower(),
            item["arquivo"],
        )
    )

    return {
        "projeto": "HidroBairro Sul",
        "total": len(records),
        "materiais": records,
    }


@router.get("/material")
def get_material(arquivo: str):
    """Retorna um documento Markdown convertido para HTML."""

    path = safe_material_path(arquivo)

    if not path.is_file() or path.suffix.lower() != ".md":
        raise HTTPException(
            status_code=404,
            detail="Documento Markdown não encontrado.",
        )

    source = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    prepared = rewrite_local_links(source, path)
    rendered = markdown(prepared)

    record = material_record(path)

    return {
        **record,
        "conteudo": rendered,
    }


@router.get("/arquivo")
def get_file(arquivo: str):
    """Disponibiliza imagens e arquivos auxiliares da base."""

    path = safe_material_path(arquivo)

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Arquivo não encontrado.",
        )

    if path.suffix.lower() == ".md":
        raise HTTPException(
            status_code=400,
            detail="Utilize a rota /api/material para documentos Markdown.",
        )

    return FileResponse(path)