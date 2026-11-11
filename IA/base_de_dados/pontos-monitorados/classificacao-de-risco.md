# Classificação de Risco (HidroBairro Sul)

## 1. Objetivo da Classificação
Estabelecer critérios padronizados para categorizar as leituras dos sensores IoT e os boletins meteorológicos, permitindo que o chatbot com RAG e a API Java diferenciem situações de normalidade, atenção, alerta e risco iminente de alagamento.

## 2. Níveis de Alerta e Critérios de Criticidade

### Nível 1: Normalidade (Verde)
* **Condição do Sensor:** Leituras dentro da normalidade, com nível de água abaixo dos limites críticos de segurança.
* **Condição Climática:** Sem chuvas expressivas ou previsões de temporais severos na região.
* **Orientação da IA:** Informar que o monitoramento está estável e orientar sobre práticas preventivas cotidianas.

### Nível 2: Atenção (Amarelo)
* **Condição do Sensor:** Início de elevação no nível de escoamento captado pelo sensor (redução significativa da distância medida em relação à referência).
* **Condição Climática:** Chuvas moderadas a fortes registradas na região ou alertas de precipitação emitidos pelos órgãos competentes.
* **Orientação da IA:** Recomendar cautela aos moradores próximos ao ponto monitorado e lembrá-los de evitar descartar lixo em locais inadequados que possam entupir bueiros.

### Nível 3: Alerta (Laranja)
* **Condição do Sensor:** Nível de água próximo ao limite de transbordo ou lâmina d'água significativa detectada na via/fundo de vale monitorado.
* **Condição Climática:** Tempestades intensas com acumulados elevados em curto período de tempo.
* **Orientação da IA:** Alertar sobre o risco iminente de alagamento no trecho, desaconselhar transitar pela via afetada e sugerir rotas alternativas seguras.

### Nível 4: Risco Elevado / Alagamento Iminente (Vermelho)
* **Condição do Sensor:** Leitura indicando transbordo do curso d'água ou acúmulo crítico de água na via monitorada.
* **Condição Climática:** Temporais severos contínuos.
* **Orientação da IA:** Acionar protocolos de emergência, orientar o morador a buscar locais elevados imediatamente, não tentar cruzar áreas alagadas a pé ou de carro e fornecer contatos da Defesa Civil e Bombeiros.

## 3. Diretrizes para a Resposta do Chatbot
* **Transparência:** A IA deve sempre esclarecer qual é o nível de alerta atual do ponto monitorado consultado na API Java.
* **Segurança em Primeiro Lugar:** A IA nunca deve garantir que um trajeto está totalmente seguro caso haja dados de alerta ativos ou incertezas nas vias.

## 4. Fontes e Referências Oficiais
* **Centro de Gerenciamento de Emergências Climáticas (CGE):** [CGE SP](https://www.cgesp.org) — Parâmetros de criticidade e classificação de índices pluviométricos e alagamentos na capital.
* **Defesa Civil do Estado de São Paulo:** [Defesa Civil SP](https://www.defesacivil.sp.gov.br) — Protocolos de emissão de alertas e gestão de desastres.
* **Centro Nacional de Monitoramento e Alertas de Desastres Naturais (CEMADEN):** [CEMADEN](https://www.gov.br/cemaden) — Metodologias de monitoramento e alertas de risco hidrológico.