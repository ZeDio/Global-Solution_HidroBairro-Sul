from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import RAG_INDEX_PATH
from rag.pipeline import responder_com_rag
from rag.retriever import indice_disponivel
from schemas import PerguntaRequest, AskResponse, RagStatusResponse, HealthResponse
from content_api import router as content_router

app = FastAPI(
    title="HidroBairro Sul API",
    description="API do assistente inteligente de prevenção e orientação sobre alagamentos.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(content_router)


@app.post("/ask", response_model=AskResponse)
def ask(dados: PerguntaRequest):
    pergunta = dados.pergunta.strip()
    if not pergunta:
        raise HTTPException(status_code=422, detail="A pergunta não pode estar vazia.")

    disponivel, mensagem, _ = indice_disponivel()
    if not disponivel:
        raise HTTPException(status_code=503, detail=mensagem or "Índice RAG indisponível.")

    try:
        resposta, trechos = responder_com_rag(pergunta, k=dados.k)
        
        fontes = []
        vistos = set()
        for t in trechos:
            if t["fonte"] not in vistos:
                vistos.add(t["fonte"])
                fontes.append({
                    "titulo": t["titulo"], 
                    "fonte": t["fonte"], 
                    "similaridade": round(t["similaridade"], 4)
                })
            if len(fontes) == 3: # Limita a no máximo 3 referências (mude para 2 se preferir)
                break
                
        return {"projeto": "HidroBairro Sul", "resposta": resposta, "fontes": fontes}
    except Exception as erro:
        print(f"Erro no endpoint /ask: {type(erro).__name__}: {erro}")
        raise HTTPException(status_code=500, detail="Não foi possível processar sua pergunta.") from erro


@app.get("/rag/status", response_model=RagStatusResponse)
def rag_status():
    disponivel, mensagem, quantidade = indice_disponivel()
    return {
        "status": "online" if disponivel else "offline",
        "indice_existe": disponivel,
        "mensagem": mensagem or f"Índice válido com {quantidade} chunks." ,
        "arquivo": str(RAG_INDEX_PATH) if disponivel else None,
    }


@app.get("/")
def home():
    disponivel, mensagem, quantidade = indice_disponivel()
    return {
        "projeto": "HidroBairro Sul",
        "status": "online",
        "mensagem": "API do HidroBairro Sul funcionando!",
        "rag": disponivel,
        "chunks_rag": quantidade,
        "mensagem_rag": mensagem,
    }


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "online", "servico": "hidrobairro-sul-ai"}
