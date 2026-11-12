from pydantic import BaseModel, Field

class PerguntaRequest(BaseModel):
    """Dados enviados pelo usuário ao consultar a IA."""

    pergunta: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Pergunta feita pelo morador.",
    )

    k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Quantidade de trechos recuperados pelo RAG.",
    )


class FonteResponse(BaseModel):
    """Fonte documental utilizada na resposta."""

    titulo: str
    fonte: str
    similaridade: float


class AskResponse(BaseModel):
    """Resposta produzida pela IA."""

    projeto: str = "HidroBairro Sul"
    resposta: str
    fontes: list[FonteResponse]


class RagStatusResponse(BaseModel):
    """Estado da base de conhecimento."""

    status: str
    indice_existe: bool
    mensagem: str | None = None
    arquivo: str | None = None


class HealthResponse(BaseModel):
    """Estado geral do serviço."""

    status: str
    servico: str