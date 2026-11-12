# Classificação de Risco (HidroBairro Sul)

## 1. Objetivo e status

Este documento descreve uma **proposta de classificação futura** para apoiar o projeto. Os níveis abaixo não estão ativos e não representam alertas reais. A aplicação depende de sensores instalados e calibrados, critérios definidos com dados de campo, integração operacional com a API Java e validação técnica.

## 2. Categorias propostas

### Nível 1: Normalidade (Verde)

Categoria planejada para condições dentro dos parâmetros de referência validados. Não deve ser inferida apenas pela ausência de uma leitura crítica.

### Nível 2: Atenção (Amarelo)

Categoria planejada para condições que indiquem necessidade de cautela, considerando leituras consistentes, histórico local e informações meteorológicas confiáveis.

### Nível 3: Alerta (Laranja)

Categoria planejada para condições que exijam evitar a área potencialmente afetada e acompanhar orientações oficiais. Os limites deverão ser definidos e validados para cada instalação.

### Nível 4: Risco elevado (Vermelho)

Categoria planejada para situações graves confirmadas por critérios técnicos e fontes confiáveis. A resposta deve priorizar orientações oficiais de emergência.

## 3. Regras de interpretação

- O HC-SR04 mede distância física até uma superfície; não mede diretamente chuva, vazão ou risco de inundação.
- A conversão de distância em altura de água depende de referência fixa e calibração local.
- Não definir limites numéricos sem medições e validação em campo.
- Cada dado deve possuir identificação do sensor, horário, unidade, validade e estado de comunicação.
- A IA só pode informar um nível atual quando receber uma resposta válida e recente de uma fonte operacional identificada.
- A IA nunca deve garantir que uma rua ou trajeto está seguro.

## 4. Fontes e referências

- [CGE SP](https://www.cgesp.org) — informações meteorológicas e monitoramento da cidade de São Paulo.
- [Defesa Civil do Estado de São Paulo](https://www.defesacivil.sp.gov.br) — orientações e alertas oficiais.
- [CEMADEN](https://www.gov.br/cemaden) — informações sobre monitoramento e alertas de desastres naturais.
