# Pontos de Monitoramento (HidroBairro Sul)

## 1. Objetivo e situação atual

O HidroBairro Sul propõe estudar pontos vulneráveis a alagamentos nas regiões de Campo Limpo, Capão Redondo e M’Boi Mirim, na Zona Sul de São Paulo. Os pontos identificados por códigos neste documento são **referências conceituais de planejamento**. Não são endereços confirmados nem comprovam a existência de sensores instalados em campo.

O protótipo IoT atual utiliza um ESP32 e um sensor ultrassônico HC-SR04 no simulador Wokwi. A simulação demonstra a comunicação e a leitura do sensor, mas não representa monitoramento físico das ruas.

## 2. Tecnologia e limites da medição

O HC-SR04 emite ondas ultrassônicas e calcula a distância até uma superfície a partir do tempo de retorno do eco. Por si só, ele **não mede diretamente o volume de água, a vazão, a chuva ou a probabilidade de alagamento**.

Para estimar a altura da água, seria necessário instalar o sensor em posição fixa, conhecer a distância de referência até o fundo ou nível de referência, calibrar a instalação e validar as leituras em condições reais. Também seriam necessários proteção adequada contra intempéries, avaliação de segurança elétrica e manutenção.

Na arquitetura planejada, o ESP32 disponibiliza a leitura por HTTP e a API Java consulta esse endpoint. A integração completa com a API Java e a implantação física ainda precisam ser realizadas e validadas antes de divulgar medições como dados reais.

## 3. Códigos conceituais de estudo

Os códigos abaixo organizam a proposta de levantamento. Não devem ser apresentados ao morador como locais monitorados nem associados a ruas específicas sem validação.

- **Campo Limpo:** CL-01 e CL-02.
- **Capão Redondo:** CR-01 e CR-02.
- **M’Boi Mirim:** MM-01 e MM-02.

A definição de cada ponto real exige pesquisa em bases oficiais, histórico de ocorrências, visita técnica, coordenadas verificadas e autorização para instalação.

## 4. Cuidados para interpretação futura

- Uma leitura isolada de distância não confirma risco de alagamento.
- Leituras inválidas, obstruções, turbulência, reflexos e deslocamento do sensor podem produzir valores incorretos.
- Os limites de alerta precisam ser definidos após calibração e validação local; não devem ser inventados ou tratados como universais.
- Dados meteorológicos e alertas oficiais podem complementar a análise, mas precisam ter fonte e horário de atualização identificáveis.
- A IA não deve afirmar que uma rua ou rota está segura apenas com base em um sensor pontual.

## 5. Fontes e referências técnicas

- Documentação técnica do ESP32 e do sensor ultrassônico HC-SR04.
- [CEMADEN](https://www.gov.br/cemaden) — informações institucionais sobre monitoramento e alertas de desastres naturais.
- [GeoSampa](https://geosampa.prefeitura.sp.gov.br) — base geográfica do município de São Paulo.
