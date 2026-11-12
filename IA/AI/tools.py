"""
Ferramentas auxiliares do HidroBairro Sul.

Este módulo disponibiliza funções de consulta à base
documental do projeto.

A recuperação principal do RAG continua sendo realizada
diretamente pelo pipeline.
"""

from rag.retriever import buscar_trechos


def buscar_material(pergunta: str, quantidade: int = 5) -> dict:
    """
    Busca informações na base documental do HidroBairro Sul.

    Args:
        pergunta: Pergunta ou assunto que será pesquisado.
        quantidade: Número máximo de trechos retornados.

    Returns:
        Dicionário com os trechos encontrados e suas fontes.
    """

    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if not isinstance(quantidade, int) or not 1 <= quantidade <= 10:
        raise ValueError(
            "A quantidade deve ser um número inteiro entre 1 e 10."
        )

    trechos = buscar_trechos(
        pergunta=pergunta.strip(),
        k=quantidade,
    )

    return {
        "projeto": "HidroBairro Sul",
        "total_resultados": len(trechos),
        "resultados": [
            {
                "id": item["id"],
                "titulo": item["titulo"],
                "fonte": item["fonte"],
                "texto": item["texto"],
                "similaridade": round(item["similaridade"], 4),
            }
            for item in trechos
        ],
    }


# Funções disponibilizadas neste módulo.
tools_list = [
    buscar_material,
]