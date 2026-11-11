# Pontos de Monitoramento (HidroBairro Sul)

## 1. Visão Geral do Sistema de Monitoramento
* **Objetivo:** Acompanhar em tempo real as condições de escoamento e o nível de água em pontos críticos de drenagem urbana e fundos de vale na Zona Sul de São Paulo (Campo Limpo, Capão Redondo e M'Boi Mirim).
* **Tecnologia Utilizada:** Sensores IoT baseados em microcontroladores ESP32 e sensores ultrassônicos (ex: HC-SR04), instalados em locais estratégicos para aferir a distância até a lâmina d'água ou superfície de escoamento.

## 2. Metodologia de Medição e Leitura
* **Princípio de Funcionamento:** O sensor ultrassônico emite ondas sonoras e mede o tempo de retorno (eco) para calcular a distância vertical entre o ponto de instalação (referência fixa) e o nível atual da água.
* **Tratamento de Dados:** 
  * Os dados brutos de distância em centímetros são transmitidos via rede Wi-Fi/IoT para a API backend (desenvolvida em Java).
  * A API converte a distância medida em nível relativo de preenchimento do canal ou via pública com base na altura de referência previamente calibrada.

## 3. Mapeamento dos Pontos Estratégicos
* **Região de Campo Limpo:**
  * **Ponto CL-01:** Fundo de vale e trecho crítico de drenagem. Monitora a proximidade de transbordo do córrego local.
  * **Ponto CL-02:** Via inclinada de escoamento rápido. Acompanha o volume de fluxo pluvial durante tempestades severas.
* **Região de Capão Redondo:**
  * **Ponto CR-01:** Trecho sensível de drenagem urbana e fundo de vale.
  * **Ponto CR-02:** Cruzamento de via arterial com histórico de acúmulo de água.
* **Região de M'Boi Mirim:**
  * **Ponto MM-01:** Eixo principal de drenagem e planície aluvial.
  * **Ponto MM-02:** Ponto crítico de estrangulamento de galerias pluviais em via de grande circulação.

## 4. Limitações Técnicas e Cuidados de Interpretação
* O sensor mede **distância física**, não garantindo isoladamente a previsibilidade absoluta de alagamentos sem o cruzamento com dados meteorológicos e calibração local.
* Fatores como detritos flutuantes, turbulência intensa ou desvios de calibração podem influenciar leituras pontuais, exigindo filtragem de dados na API antes do envio para a IA.

## 5. Fontes e Referências Técnicas
* **Documentação Oficial de Hardware:** Manuais técnicos do ESP32 e do sensor ultrassônico HC-SR04.
* **Centro Nacional de Monitoramento e Alertas de Desastres Naturais (CEMADEN):** [CEMADEN](https://www.gov.br/cemaden) — Diretrizes sobre telemetria e monitoramento hidrológico.
* **Prefeitura de São Paulo (GeoSampa):** [GeoSampa](https://geosampa.prefeitura.sp.gov.br) — Mapeamento de bacias hidrográficas e infraestrutura de drenagem urbana.