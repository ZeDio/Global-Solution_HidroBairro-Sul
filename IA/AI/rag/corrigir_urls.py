import json
from pathlib import Path
from urllib.parse import quote


INDEX_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "index.json"
)


indice = json.loads(
    INDEX_PATH.read_text(encoding="utf-8")
)


for item in indice:

    fonte = item["fonte"].replace("\\", "/")

    item["url"] = (
        "https://ultima-cp-disruptive-architectures.vercel.app/"
        "aula.html?arquivo="
        + quote(fonte)
    )


INDEX_PATH.write_text(
    json.dumps(
        indice,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)


print("========================================")
print("✅ URLs do RAG corrigidas")
print("========================================")
print(f"Chunks atualizados: {len(indice)}")