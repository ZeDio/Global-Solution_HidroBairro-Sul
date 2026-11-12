from config import client, MODEL_NAME
from SYSTEM_PROMPT import SYSTEM_PROMPT
from .retriever import buscar_trechos

SYSTEM_PROMPT_RAG = SYSTEM_PROMPT + """

### REGRAS DE UTILIZAÇÃO DO RAG

Você receberá um contexto recuperado da base de conhecimento
do HidroBairro Sul.

- Utilize o contexto para fundamentar informações sobre
  prevenção de alagamentos e regiões atendidas.
- Não invente informações que não estejam nos documentos.
- Não apresente hipóteses como fatos confirmados.
- Não invente endereços, abrigos ou pontos de monitoramento.
- Não confunda pontos hipotéticos com locais reais.
- Não trate a similaridade como certeza.
- Quando utilizar informações dos documentos, indique
  a fonte no formato [nome-do-arquivo.md].
- Se o contexto não for suficiente, informe a limitação.

### DADOS EM TEMPO REAL

A base RAG contém documentos de conhecimento e orientação.
Ela não representa a situação atual dos sensores.

Nunca invente:
- Medições dos sensores.
- Horários de atualização.
- Alertas ativos.
- Níveis atuais de água.
- Classificações atuais de risco.

Se não houver integração com a API Java para consultar
dados atuais, informe que não é possível confirmar
a situação em tempo real.

### SEGURANÇA

Em situações de alagamento:
- Oriente o morador a evitar áreas inundadas.
- Nunca recomende atravessar enxurradas a pé ou de carro.
- Priorize a segurança das pessoas.
- Recomende acompanhar os canais oficiais da Defesa Civil.
"""


def montar_contexto(trechos: list[dict]) -> str:
    """Organiza os documentos recuperados para o Gemini."""

    if not trechos:
        return "Nenhum documento relevante foi encontrado."

    blocos = []

    for trecho in trechos:
        blocos.append(
            f"FONTE: [{trecho['fonte']}]\n"
            f"TÍTULO: {trecho['titulo']}\n"
            f"CONTEÚDO: {trecho['texto']}"
        )

    return "\n\n---\n\n".join(blocos)


def responder_com_rag(
    pergunta: str,
    k: int = 5,
) -> tuple[str, list[dict]]:
    """
    Recupera documentos relevantes e gera uma resposta
    contextualizada pelo Gemini.
    """

    if not pergunta or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    pergunta = pergunta.strip()

    # Etapa 1: recuperação dos documentos.
    trechos = buscar_trechos(
        pergunta,
        k=k,
    )

    # Etapa 2: montagem do contexto.
    contexto = montar_contexto(trechos)

    # Etapa 3: geração da resposta.
    response = client.interactions.create(
        model=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT_RAG,
        input=(
            f"CONTEXTO RECUPERADO:\n"
            f"{contexto}\n\n"
            f"PERGUNTA DO MORADOR:\n"
            f"{pergunta}"
        ),
    )

    resposta = response.output_text

    if not resposta or not resposta.strip():
        raise RuntimeError(
            "O Gemini não retornou uma resposta em texto."
        )

    return resposta.strip(), trechos


if __name__ == "__main__":

    pergunta = input(
        "Digite sua pergunta: "
    ).strip()

    if not pergunta:
        raise SystemExit("Digite uma pergunta válida.")

    resposta, trechos = responder_com_rag(
        pergunta,
        k=5,
    )

    print("\n[HIDROBAIRRO SUL — RESPOSTA]\n")
    print(resposta)

    print("\n[FONTES CONSULTADAS]\n")

    for trecho in trechos:
        print(
            f"- {trecho['fonte']} "
            f"(similaridade: {trecho['similaridade']:.4f})"
        )