# 💧 HidroBairro Sul — IoT & Inteligência Artificial

Sistema acadêmico de apoio à prevenção e à orientação sobre alagamentos na Zona Sul de São Paulo, com foco nas regiões de **Campo Limpo, Capão Redondo e M’Boi Mirim**.

O projeto integra tecnologias de **Internet das Coisas (IoT)** e **Inteligência Artificial (IA)** para desenvolver uma solução capaz de coletar informações por sensores, disponibilizar dados por APIs e oferecer orientações inteligentes aos moradores.

A solução utiliza um ESP32 com sensor ultrassônico HC-SR04, uma API IoT, uma camada de Inteligência Artificial desenvolvida em Python e uma arquitetura de integração com uma API Java.

> **Status atual:** o protótipo IoT está em simulação no Wokwi. A API de IA foi publicada no Render com índice RAG gerado e integração com Gemini funcionando, além de contar com uma interface web de testes publicada na Vercel. A API Java está em desenvolvimento.

---

## 🔗 Links do Projeto

- **Interface Web / Front-end (Vercel):** https://hidrobairro-sul.vercel.app/
- **API de Inteligência Artificial (Render):** https://global-solution-hidrobairro-sul.onrender.com/
- **Simulação IoT (Wokwi):** https://wokwi.com/projects/480341974696549377
- **Repositório no GitHub:** https://github.com/ZeDio/Global-Solution_HidroBairro-Sul

---

## 📌 Sobre o projeto

O HidroBairro Sul busca utilizar tecnologias IoT e Inteligência Artificial para auxiliar na prevenção de alagamentos e na disseminação de informações relevantes para moradores da Zona Sul de São Paulo.

A proposta é conectar dispositivos IoT a uma aplicação capaz de receber, processar e interpretar informações, oferecendo orientações e apoiando a tomada de decisão.

O projeto está dividido em três componentes principais:

- **IoT:** responsável pela coleta experimental de dados utilizando sensores conectados ao ESP32.
- **API Java:** responsável pela integração entre os componentes e pelas regras da aplicação.
- **Inteligência Artificial:** responsável por responder perguntas utilizando uma base documental especializada e, futuramente, informações dinâmicas disponibilizadas pela API Java.

### Objetivos

- Desenvolver um protótipo IoT utilizando ESP32 e sensor ultrassônico HC-SR04.
- Disponibilizar as informações coletadas por meio de uma API HTTP.
- Permitir que a aplicação Java consulte os dados do dispositivo.
- Desenvolver uma API de Inteligência Artificial especializada em prevenção de alagamentos.
- Implementar uma arquitetura RAG para consultar documentos do projeto.
- Integrar o Gemini para geração de embeddings e respostas.
- Disponibilizar a API de IA no Render e uma interface web de testes na Vercel.
- Preparar a comunicação entre IoT, API Java e Inteligência Artificial.

---

## 🗺️ Regiões atendidas

O projeto tem como foco três regiões da Zona Sul de São Paulo:

- Campo Limpo.
- Capão Redondo.
- M’Boi Mirim.

A documentação da IA reúne informações relacionadas às regiões, orientações preventivas, procedimentos de emergência e informações de interesse dos moradores.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| C++ | Programação do ESP32 |
| ESP32 | Microcontrolador do protótipo IoT |
| HC-SR04 | Sensor ultrassônico para medição de distância |
| Wi-Fi | Comunicação de rede |
| HTTP | Comunicação entre aplicações |
| JSON | Formato de troca de informações |
| Wokwi | Simulação do circuito IoT |
| Python | Desenvolvimento da camada de IA |
| FastAPI | Construção da API de Inteligência Artificial |
| Uvicorn | Servidor para execução da API |
| Google Gemini | Geração de respostas e embeddings |
| RAG | Recuperação de informações da base documental |
| NumPy | Operações numéricas |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| HTML / CSS / JS | Interface web de testes do assistente (`Front_End_Test`) |
| Vercel | Hospedagem do front-end de testes |
| Render | Hospedagem da API de IA |
| Java | Backend de integração, em desenvolvimento |
| Oracle Database | Banco de dados previsto para o projeto |

---

# 🔌 Parte 1 — Internet das Coisas (IoT)

## Hardware e componentes

O protótipo IoT utiliza:

- 1 ESP32.
- 1 sensor ultrassônico HC-SR04.
- Conexões por GPIO.

![Circuito ESP32 com sensor HC-SR04](Esp32.png)

### Ligações do circuito

| HC-SR04 | ESP32 |
|---|---|
| VCC | 5V |
| TRIG | GPIO 5 |
| ECHO | GPIO 18 |
| GND | GND |

O circuito é desenvolvido e testado utilizando o simulador Wokwi: https://wokwi.com/projects/480341974696549377.

**Atenção:** antes de uma montagem física, é necessário verificar a compatibilidade elétrica dos sinais do HC-SR04 com o ESP32, especialmente o nível lógico do pino ECHO.

## ⚙️ Funcionamento do sistema IoT

O ESP32 estabelece conexão com a rede Wi-Fi, realiza leituras periódicas do sensor ultrassônico e disponibiliza os dados por meio de um servidor HTTP.

Nesta arquitetura, o dispositivo funciona como um servidor: a API Java realiza uma requisição para consultar as informações disponibilizadas pelo ESP32.

### Fluxo de comunicação

1. O ESP32 estabelece conexão com a rede Wi-Fi.
2. O sensor HC-SR04 realiza a medição da distância.
3. O ESP32 atualiza os valores coletados.
4. O servidor HTTP disponibiliza os dados em JSON.
5. A API Java realiza uma requisição GET para consultar as informações.
6. Os dados podem ser utilizados pelas funcionalidades da aplicação.

## 🌐 API IoT — ESP32

O ESP32 possui um servidor HTTP que disponibiliza os dados coletados pelo sensor.

### Endpoints documentados

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verifica se o servidor IoT está ativo |
| GET | `/status` | Retorna os dados atuais do sensor em JSON |

### Exemplo de requisição

```http
GET /status
```

### Exemplo de resposta JSON

```json
{
  "distanciaCm": 45.50,
  "data": "2026-11-10",
  "horario": "19:22:00",
  "leituraValida": true
}
```

| Campo | Descrição |
|---|---|
| `distanciaCm` | Distância medida pelo sensor, em centímetros |
| `data` | Data da leitura |
| `horario` | Horário da leitura |
| `leituraValida` | Indica se a medição foi realizada corretamente |

O exemplo é ilustrativo. Os valores reais dependem da simulação ou da implementação em execução.

## Limitações do protótipo IoT

O HC-SR04 mede a distância até uma superfície. Ele não mede diretamente chuva, vazão de córregos ou risco de alagamento.

Para utilizar essas medições na estimativa de nível de água, será necessário:

- Instalar corretamente os sensores.
- Definir uma referência física de medição.
- Realizar calibração.
- Validar os dados em campo.
- Estabelecer critérios técnicos para interpretação das leituras.

Atualmente, o protótipo está em simulação no Wokwi. Portanto, não representa sensores instalados nas ruas.

---

# 🤖 Parte 2 — Inteligência Artificial

## Sobre a IA do HidroBairro Sul

A camada de Inteligência Artificial foi desenvolvida em Python e utiliza FastAPI para disponibilizar os recursos por meio de uma API HTTP.

O sistema utiliza o Google Gemini para gerar embeddings e respostas, enquanto a arquitetura RAG permite recuperar informações relevantes da base documental antes da geração de uma resposta.

O assistente conta com instruções de sistema (`SYSTEM_PROMPT.py`) ajustadas para priorizar respostas diretas, objetivas e sem saudações longas, além de filtrar e limitar a exibição de até 3 fontes únicas consultadas por resposta na API (`api.py`).

## 🧠 Arquitetura RAG

RAG significa *Retrieval-Augmented Generation*, ou geração aumentada por recuperação.

Essa arquitetura permite que a IA consulte uma base documental própria antes de formular uma resposta.

### Funcionamento do RAG

1. Os documentos Markdown da base de conhecimento são lidos pelo indexador.
2. O conteúdo é dividido em pequenos trechos chamados *chunks*.
3. São gerados embeddings para representar semanticamente cada trecho.
4. Os embeddings e seus metadados são armazenados no índice.
5. Quando uma pergunta é recebida, um embedding também é gerado para ela.
6. O recuperador compara a pergunta com os documentos indexados.
7. Os trechos mais relevantes são selecionados.
8. O pipeline envia a pergunta e o contexto recuperado ao Gemini.
9. A API retorna a resposta e as fontes utilizadas (limitadas às principais referências únicas).

### Fluxo de processamento

```text
       Documentos Markdown
                |
                v
          rag/indexer.py
                |
                v
          Divisão em chunks
                |
                v
         Google Embeddings
                |
                v
            index.json
                |
                |
          Pergunta do usuário
                |
                v
          rag/retriever.py
                |
                v
       Recuperação de contexto
                |
                v
          rag/pipeline.py
                |
                v
          Google Gemini
                |
                v
        Resposta + Fontes
                |
                v
            FastAPI
```

## 📚 Base de conhecimento

A base documental está localizada em:

```text
IA/base_de_dados/
```

Ela contém documentos Markdown organizados por categorias.

### Categorias documentais

| Categoria | Conteúdo |
|---|---|
| `defesa-civil/` | Orientações antes, durante e depois de alagamentos |
| `emergencias/` | Contatos, procedimentos de evacuação e locais seguros |
| `informacoes-locais/` | Informações sobre Campo Limpo, Capão Redondo e M’Boi Mirim |
| `perguntas-frequentes/` | Perguntas e respostas voltadas aos moradores |
| `pontos-monitorados/` | Classificação proposta de risco e pontos conceituais de monitoramento |

A base documental é utilizada como fonte de conhecimento para a IA.

**Importante:** o RAG contém informações documentais e orientações. Ele não contém medições em tempo real dos sensores.

## Modelos utilizados

Os modelos configurados na implementação são:

| Finalidade | Modelo |
|---|---|
| Geração de respostas | `gemini-3.1-flash-lite` |
| Geração de embeddings | `gemini-embedding-2` |

O acesso aos modelos depende da disponibilidade e das permissões da API Google Gemini.

## 🔎 Recuperação de informações

O módulo `rag/retriever.py` é responsável por localizar os trechos mais relevantes para uma pergunta.

A recuperação utiliza embeddings e similaridade de cosseno para comparar semanticamente a pergunta com os documentos indexados.

O parâmetro `k` permite definir a quantidade de trechos recuperados. Na API (`api.py`), as fontes retornadas ao usuário passam por deduplicação e são limitadas a até 3 documentos de referência para manter a interface limpa.

## 📝 Geração do índice RAG

O indexador está localizado em:

```text
AI/rag/indexer.py
```

Ele realiza:

- Leitura dos documentos da base de conhecimento.
- Divisão do conteúdo em chunks.
- Geração de embeddings.
- Armazenamento dos registros.
- Reaproveitamento de chunks válidos, quando aplicável.
- Persistência do índice para consultas futuras.

O índice gerado fica em:

```text
AI/rag/data/index.json
```

Na execução realizada durante o desenvolvimento, foram processados **24 chunks**, concluindo a geração do índice com sucesso.

O índice deve ser atualizado quando os documentos da base de conhecimento forem alterados.

---

# 🌐 Parte 3 — API de Inteligência Artificial

## FastAPI

A camada de IA disponibiliza seus recursos por meio de uma API desenvolvida com FastAPI.

O servidor é executado utilizando Uvicorn e está publicado em: https://global-solution-hidrobairro-sul.onrender.com/

### Endpoints principais

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Retorna informações gerais da API e do RAG |
| GET | `/health` | Verifica se o serviço está funcionando |
| GET | `/rag/status` | Consulta o estado do índice RAG |
| POST | `/ask` | Recebe uma pergunta e retorna a resposta da IA |

O projeto também possui um router de conteúdo em `content_api.py`, com rotas relacionadas à disponibilização de materiais.

Consulte `/docs` para visualizar todos os métodos e caminhos registrados.

## Endpoint `/health`

Verifica se a API está respondendo.

### Requisição

```http
GET /health
```

### Resposta esperada

```json
{
  "status": "online",
  "servico": "hidrobairro-sul-ai"
}
```

## Endpoint `/rag/status`

Verifica a disponibilidade do índice RAG.

### Requisição

```http
GET /rag/status
```

### Exemplo de resposta

```json
{
  "status": "online",
  "indice_existe": true,
  "mensagem": "Índice válido com 24 chunks.",
  "arquivo": "caminho/local/para/index.json"
}
```

A quantidade de chunks depende dos documentos indexados.

## Endpoint `/ask`

Recebe uma pergunta, recupera informações relevantes do RAG e utiliza o Gemini para produzir uma resposta.

### Requisição

```http
POST /ask
Content-Type: application/json
```

### Corpo da requisição

```json
{
  "pergunta": "Quais cuidados devo tomar antes de um possível alagamento?",
  "k": 5
}
```

| Campo | Descrição |
|---|---|
| `pergunta` | Pergunta enviada pelo usuário |
| `k` | Quantidade de trechos relevantes solicitados ao recuperador |

### Exemplo de resposta

```json
{
  "projeto": "HidroBairro Sul",
  "resposta": "Resposta gerada com base na pergunta e no contexto recuperado.",
  "fontes": [
    {
      "titulo": "Perguntas Frequentes (FAQ) - Moradores",
      "fonte": "perguntas-frequentes/perguntas-moradores.md",
      "similaridade": 0.7305
    }
  ]
}
```

O conteúdo acima representa apenas o formato da resposta. Os textos e valores reais dependem da pergunta e dos documentos recuperados.

## 📖 Documentação Swagger

A API disponibiliza uma documentação interativa por meio do Swagger.

- **Ambiente publicado:** https://global-solution-hidrobairro-sul.onrender.com/docs
- **Ambiente local:** `http://127.0.0.1:8000/docs`

Pelo Swagger é possível visualizar os endpoints, enviar requisições e consultar as respostas retornadas pela API.

# 🚀 Parte 4 — Como executar o projeto

## Pré-requisitos

- Python instalado.
- Visual Studio Code.
- Git.
- Acesso à API Google Gemini.
- Chave de API Gemini válida.
- Extensão Wokwi para VS Code, para executar a simulação IoT.

## Estrutura da camada de IA

A estrutura relevante da implementação é:

```text
IA/
│
├── .venv/
│
├── base_de_dados/
│   ├── defesa-civil/
│   ├── emergencias/
│   ├── informacoes-locais/
│   ├── perguntas-frequentes/
│   └── pontos-monitorados/
│
└── AI/
    ├── .env
    ├── api.py
    ├── config.py
    ├── content_api.py
    ├── main.py
    ├── requirements.txt
    ├── schemas.py
    ├── SYSTEM_PROMPT.py
    ├── tools.py
    │
    └── rag/
        ├── embeddings.py
        ├── indexer.py
        ├── pipeline.py
        ├── retriever.py
        ├── README.md
        └── data/
            └── index.json
```

## 1. Clonar o repositório

```bash
git clone [https://github.com/ZeDio/Global-Solution_HidroBairro-Sul.git](https://github.com/ZeDio/Global-Solution_HidroBairro-Sul.git)
```

Entre na pasta principal do projeto:

```bash
cd Global-Solution_HidroBairro-Sul
```

Entre na pasta `IA`, onde está a implementação Python:

```bash
cd IA
```

## 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

## 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativo, o terminal apresentará:

```text
(.venv)
```

Caso o PowerShell bloqueie a ativação, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, tente ativar novamente.

## 4. Instalar as dependências

Com o terminal na pasta principal `IA` e o ambiente virtual ativado:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências:

```powershell
python -m pip install -r AI/requirements.txt
```

## 5. Configurar a chave Gemini

Crie um arquivo chamado `.env` dentro da pasta:

```text
IA/AI/.env
```

Adicione a variável:

```env
API_KEY=sua_chave_aqui
```

Substitua `sua_chave_aqui` pela chave da sua conta Google Gemini.

**Segurança:**
- Não compartilhe sua chave.
- Não publique o arquivo `.env`.
- Não envie o arquivo com credenciais para o GitHub.
- Utilize um `.env.example` sem valores secretos para documentar as variáveis necessárias.

## 6. Gerar o índice RAG

Entre na pasta `AI`:

```powershell
cd AI
```

Execute o indexador:

```powershell
python -m rag.indexer
```

O processo irá:

1. Ler os documentos Markdown de `IA/base_de_dados`.
2. Dividir os documentos em chunks.
3. Gerar embeddings utilizando o Gemini.
4. Criar ou atualizar o índice RAG.

O arquivo será salvo em:

```text
AI/rag/data/index.json
```

A geração do índice consome chamadas da API Gemini.

**Importante:** não é necessário executar o indexador toda vez que iniciar a API. Execute novamente quando houver alterações na base documental ou quando precisar reconstruir o índice.

## 7. Testar a recuperação RAG

Ainda dentro da pasta `AI`, execute:

```powershell
python -m rag.retriever
```

Digite uma pergunta quando solicitado.

O programa deverá apresentar os trechos mais relevantes encontrados na base documental e suas respectivas similaridades.

Essa operação também utiliza a API Gemini para gerar o embedding da pergunta.

## 8. Iniciar a API

Ainda dentro da pasta `AI`, execute:

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Quando aparecer:

```text
Application startup complete.
```

A API estará em execução.

### Endereços locais

| Serviço | Endereço |
|---|---|
| API | http://127.0.0.1:8000 |
| Swagger | http://127.0.0.1:8000/docs |
| Health | http://127.0.0.1:8000/health |
| Status RAG | http://127.0.0.1:8000/rag/status |

Para encerrar o servidor:

```text
Ctrl + C
```

## 9. Testar a IA pelo Swagger

1. Acesse `http://127.0.0.1:8000/docs` (ou `https://global-solution-hidrobairro-sul.onrender.com/docs`).
2. Localize `POST /ask`.
3. Clique em **Try it out**.
4. Insira:

```json
{
  "pergunta": "Sobre o que é o projeto HidroBairro Sul e como funciona?",
  "k": 5
}
```

5. Clique em **Execute**.
6. Verifique a resposta e as fontes retornadas.

## 10. Reiniciar o projeto em outra sessão

Se o ambiente virtual, as dependências e o índice RAG já estiverem configurados, não é necessário reinstalar tudo ou gerar os embeddings novamente.

No PowerShell:

```powershell
cd "C:\caminho\para\Global-Solution_HidroBairro-Sul\IA"
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Entre na pasta da API:

```powershell
cd AI
```

Inicie o servidor:

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

---

# ☁️ Parte 6 — Publicação da API no Render e Front-end na Vercel

A publicação da API de Inteligência Artificial no Render e da interface web de testes na Vercel já foi concluída e está ativa.

### Ambientes publicados

- **Interface Web (Vercel):** https://hidrobairro-sul.vercel.app/
- **API de Inteligência Artificial (Render):** https://global-solution-hidrobairro-sul.onrender.com/
- **Documentação Swagger (Render):** https://global-solution-hidrobairro-sul.onrender.com/docs

### Detalhes da implantação

1. Configuração da variável de ambiente `GEMINI_API_KEY` diretamente no painel do Render (sem expor credenciais no repositório).
2. Disponibilização do índice RAG (`AI/rag/data/index.json`) no ambiente de produção.
3. Configuração de CORS na API FastAPI para permitir requisições vindas do front-end hospedado na Vercel.
4. Criação de interface web (`Front_End_Test/index.html`) conectada à API do Render para testes em tempo real com o assistente.

---

# 📁 Parte 7 — Estrutura do repositório

Estrutura principal documentada:

```text
Global-Solution_HidroBairro-Sul/
│
├── Front_End_Test/
│   └── index.html
│
├── IA/
│   │
│   ├── base_de_dados/
│   │   ├── defesa-civil/
│   │   ├── emergencias/
│   │   ├── informacoes-locais/
│   │   ├── perguntas-frequentes/
│   │   └── pontos-monitorados/
│   │
│   └── AI/
│       ├── api.py
│       ├── config.py
│       ├── content_api.py
│       ├── main.py
│       ├── requirements.txt
│       ├── schemas.py
│       ├── SYSTEM_PROMPT.py
│       ├── tools.py
│       │
│       └── rag/
│           ├── embeddings.py
│           ├── indexer.py
│           ├── pipeline.py
│           ├── retriever.py
│           ├── README.md
│           └── data/
│               └── index.json
│
└── IoT/
    ├── sketch.ino
    ├── diagram.json
    ├── libraries.txt
    ├── wokwi-project.txt
    └── wokwi.toml
```

### Principais arquivos da IA

| Arquivo | Responsabilidade |
|---|---|
| `api.py` | Define a aplicação FastAPI, seus endpoints e o filtro de fontes únicas |
| `config.py` | Centraliza configurações, caminhos e modelos |
| `schemas.py` | Define os modelos de dados da API |
| `content_api.py` | Implementa as rotas de disponibilização de materiais |
| `tools.py` | Reúne ferramentas utilizadas pela IA |
| `SYSTEM_PROMPT.py` | Define as instruções de comportamento, concisão e segurança do assistente |
| `main.py` | Permite executar a interação pelo terminal |
| `rag/indexer.py` | Lê documentos e constrói o índice |
| `rag/embeddings.py` | Responsável pela geração de embeddings |
| `rag/retriever.py` | Recupera os trechos mais relevantes |
| `rag/pipeline.py` | Coordena recuperação de contexto e geração de respostas |
| `rag/data/index.json` | Armazena o índice gerado pelo processo RAG |

---

# 🧪 Parte 8 — Testes realizados

Durante o desenvolvimento, foram realizados testes locais e em produção para validar a camada de Inteligência Artificial.

### Resultados obtidos

| Teste | Resultado |
|---|---|
| Criação do ambiente virtual Python | Concluída |
| Instalação das dependências | Concluída |
| Verificação com `pip check` | Sem dependências quebradas |
| Geração do índice RAG | Concluída |
| Chunks encontrados | 24 |
| Embeddings processados | 24 |
| Teste de recuperação documental | Sucesso |
| Inicialização da API FastAPI | Sucesso |
| Endpoint `GET /health` | HTTP 200 |
| Endpoint `GET /rag/status` | HTTP 200 |
| Endpoint `POST /ask` | HTTP 200 |
| Resposta do Gemini | Sucesso |
| Retorno das fontes documentais (deduplicadas e limitadas a 3) | Sucesso |
| Deploy da API no Render | Concluído e online |
| Deploy da interface de testes na Vercel | Concluído e integrado à API |

### Resultado da geração do índice

```text
Chunks encontrados: 24
Chunks reaproveitados: 0
Chunks restantes: 24

ÍNDICE DO HIDROBAIRRO SUL CONCLUÍDO!

Total de chunks: 24
```

### Resultado da API

A API respondeu corretamente às requisições realizadas pelo Swagger e pela interface web na Vercel.

O endpoint `POST /ask` retornou:

- Nome do projeto.
- Resposta gerada pelo Gemini (com instruções de objetividade e tratamento de saudações).
- Fontes documentais consultadas (sem duplicatas, limitadas às 3 mais relevantes).
- Similaridade dos trechos recuperados.

O endpoint `/rag/status` confirmou:

```json
{
  "status": "online",
  "indice_existe": true,
  "mensagem": "Índice válido com 24 chunks."
}
```

Os resultados representam os testes realizados durante o desenvolvimento. Alterações posteriores no código ou na base documental exigem novas validações.

---

# ⚠️ Considerações importantes

O HidroBairro Sul é um projeto em desenvolvimento. Algumas funcionalidades são experimentais ou ainda dependem de integração e validação.

- O protótipo IoT utiliza ESP32 e HC-SR04 em simulação no Wokwi.
- O sensor ultrassônico mede distância, não prevê alagamentos diretamente.
- Ainda não existem sensores físicos instalados nas regiões monitoradas por este protótipo.
- O RAG trabalha com informações documentais, não com medições em tempo real.
- Os códigos de pontos de monitoramento são referências conceituais, não endereços confirmados.
- Locais seguros e pontos de apoio não devem ser apresentados como abrigos oficiais sem validação dos órgãos responsáveis.
- A IA não deve inventar medições, alertas, endereços, abrigos ou rotas seguras.
- A integração com a API Java ainda está em desenvolvimento.

Para situações reais de emergência, os moradores devem acompanhar os alertas e orientações dos órgãos oficiais, especialmente a Defesa Civil e os serviços de emergência.

---

# 👨‍💻 Desenvolvimento

Projeto desenvolvido como parte da iniciativa **Global Solution HidroBairro Sul**, utilizando tecnologias de Internet das Coisas e Inteligência Artificial.

### Responsabilidades desta implementação

- Desenvolvimento do firmware do ESP32.
- Configuração e integração do sensor HC-SR04.
- Desenvolvimento do protótipo IoT no Wokwi.
- Implementação do servidor HTTP.
- Desenvolvimento da API de Inteligência Artificial.
- Organização da base documental do projeto.
- Implementação da indexação e recuperação RAG.
- Integração com o Google Gemini e ajuste do `SYSTEM_PROMPT.py` para respostas concisas.
- Criação da interface web de testes (`Front_End_Test`) e publicação na Vercel.
- Publicação da API de IA no Render e integração com o front-end.
- Preparação da integração com Java.

---

# 👥 Equipe

Projeto desenvolvido por:

- José Diogo — ZeDio: https://github.com/ZeDio
- Arthur Dos Santos — Arth.pv: https://github.com/ArthurCPV
- Mariana Xavier — Marixavq: https://github.com/Marixavq
- Júlia Tiziotto — JúliaB: https://github.com/JuliaTButtler
- Bruno Martins — Taikawaititi: https://github.com/Taikawaititi