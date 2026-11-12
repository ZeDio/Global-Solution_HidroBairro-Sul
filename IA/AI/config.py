import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# CONFIGURACOES GERAIS
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega as credenciais
load_dotenv(Path(__file__).resolve().parent / ".env")

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError(
        "API_KEY nao encontrada. "
        "Configure a chave no arquivo .env."
    )

# Cliente Gemini
client = genai.Client(api_key=API_KEY)

# Modelos
MODEL_NAME = "gemini-3.1-flash-lite"
EMBEDDING_MODEL = "gemini-embedding-2"

# BASE DE CONHECIMENTO
MATERIAL_DIR = BASE_DIR / "base_de_dados"

# INDICE RAG
RAG_DIR = Path(__file__).resolve().parent / "rag"
RAG_DATA_DIR = RAG_DIR / "data"
RAG_INDEX_PATH = RAG_DATA_DIR / "index.json"