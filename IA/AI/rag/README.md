# RAG do HidroBairro Sul

## Fluxo

```text
IA/base_de_dados/*.md
    ↓
rag/indexer.py
    ↓
chunks + embeddings Gemini
    ↓
rag/data/index.json
    ↓
rag/retriever.py
    ↓
Top K por similaridade de cosseno
    ↓
rag/pipeline.py
    ↓
Gemini + contexto + fontes
    ↓
resposta
```

## Configuração

Na pasta `IA/AI`, crie um arquivo `.env` com `GEMINI_API_KEY=sua_chave`. Não compartilhe esse arquivo nem o envie ao Git.

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Gerar o índice

Na pasta `IA/AI`, execute:

```bash
python -m rag.indexer
```

O indexador lê os Markdown de `IA/base_de_dados` e grava `IA/AI/rag/data/index.json`. A geração consome chamadas da API Gemini. O processo salva o progresso e pode ser retomado após uma falha. Registros antigos de outros projetos são descartados.

## Testar a recuperação

```bash
python -m rag.retriever
```

Essa etapa também gera um embedding para a pergunta e, portanto, consome uma chamada da API Gemini.

## Iniciar a API

```bash
python -m uvicorn api:app --reload
```

Rotas principais: `GET /health`, `GET /rag/status`, `POST /ask`, `GET /api/materials`.

## Importante sobre os dados

O RAG contém conhecimento documental e orientações. Ele não contém medições em tempo real. Os códigos CL-01, CR-01 e MM-01 são identificadores conceituais do projeto, não endereços ou sensores confirmados. A integração com a API Java e a implantação física dos sensores precisam estar concluídas antes de apresentar dados atuais aos moradores.
