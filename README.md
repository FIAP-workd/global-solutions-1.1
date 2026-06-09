# Global Solution 2026 - Monitoramento de Missao Espacial

Sistema orientado a objetos para monitorar uma missao espacial experimental a partir de dados horarios de telemetria. O projeto interpreta leituras de energia, ambiente, comunicacao e modulos criticos, identifica riscos operacionais, gera alertas, calcula previsoes simples e recomenda acoes para manter a missao segura.

## Nome da equipe e integrantes

Equipe: Pendente de preenchimento

Integrantes:

| Nome | RM |
| --- | --- |
Luis Gustavo Ribeiro Andrade | RM569147
João Victor Viana Feitosa | RM573217
Kaio Abreu Briegas | RM572792
Pedro César Fernandes de Brito | RM573965
Gabriel Coutinho Barcelos | RM573211

## Resumo do problema e cenario analisado

O problema analisado e o monitoramento de uma colonia ou habitat espacial experimental chamado **Ares Habitat Experimental**. Em um ambiente isolado, qualquer falha em suporte a vida, energia, comunicacao ou sensores ambientais pode comprometer a operacao da missao.

O sistema le um arquivo externo de telemetria em `data/telemetria.json`, com 1200 leituras horarias. Cada leitura contem status dos modulos criticos, dados energeticos, variaveis ambientais, subsistemas e eventos operacionais. A partir desses dados, o programa classifica o estado da missao como `NORMAL`, `ALERTA` ou `CRITICO`.

## Estruturas de dados usadas

| Estrutura | Uso no sistema | Motivo |
| --- | --- | --- |
| Lista | Armazena consumo energetico, geracao energetica, temperaturas e leituras horarias. | Permite percorrer historicos e calcular previsoes com os ultimos valores. |
| Fila | Armazena alertas pendentes em `fila_alertas`. | Garante processamento por ordem de chegada. |
| Pilha | Armazena os ultimos eventos criticos em `pilha_eventos_criticos`. | Facilita consultar rapidamente os eventos criticos mais recentes. |
| Dicionario | Armazena modulos por nome, energia, ambiente e subsistemas. | Permite acesso direto a valores como `comunicacao`, `suporte_vida` e `bateria_percentual`. |
| Hierarquia | Representa os subsistemas da missao. | Organiza componentes relacionados, como energia, habitat e comunicacao. |
| Matriz | Representa leituras energeticas no formato `[geracao, consumo, bateria]`. | Agrupa dados numericos de energia ao longo do tempo para analise. |

## Regras logicas principais do diagnostico

O diagnostico usa estruturas condicionais `if`, `elif` e `else`, combinadas com operadores logicos `and`, `or` e `not`.

Expressao booleana principal:

```text
CRITICO =
(bateria < 20 AND comunicacao == 0)
OR
(suporte_vida == 0)
OR
(radiacao > 90)
```

Regras implementadas:

- `CRITICO`: ocorre quando a bateria esta abaixo de 20% e a comunicacao falhou, ou quando o suporte a vida falhou, ou quando a radiacao passa de 90 mSv.
- `ALERTA`: ocorre quando a bateria esta abaixo de 40%, ou a radiacao passa de 70 mSv, ou o sensor de oxigenio esta desligado.
- `NORMAL`: ocorre quando nenhuma das condicoes de risco acima e identificada.
- Inconsistencia proposital: o sistema detecta quando o suporte a vida esta ativo, mas o sensor de oxigenio esta desligado.

## Tecnica de previsao utilizada e resultado

A tecnica utilizada foi **media movel simples**, com janela de 3 valores.

Formula:

```text
Previsao = soma dos ultimos N valores / N
```

No sistema, a previsao e aplicada ao consumo energetico e a geracao energetica. Na execucao atual do projeto, o resultado foi:

| Variavel | Resultado |
| --- | --- |
| Consumo previsto | 59.18 kWh |
| Geracao prevista | 15.53 kWh |

Como o consumo previsto ficou maior que a geracao prevista, o sistema recomendou ativar modo economia e desligar temporariamente o laboratorio.

## Como executar

Execute o comando abaixo na raiz do projeto:

```bash
Python src/sistema.py
```

Tambem e possivel executar como modulo:

```bash
python -m src.sistema
```

Se `data/telemetria.json` nao existir, o sistema gera automaticamente uma base com 1200 leituras horarias.

## Exemplo de entrada

Exemplo simplificado de uma leitura do arquivo `data/telemetria.json`:

```json
{
  "timestamp": "2026-02-19T23",
  "modulos": {
    "suporte_vida": 1,
    "energia": 1,
    "comunicacao": 1,
    "habitat": 1,
    "laboratorio": 1,
    "armazenamento": 1
  },
  "energia": {
    "geracao_kwh": 15.53,
    "consumo_kwh": 59.18,
    "bateria_percentual": 18.5
  },
  "ambiente": {
    "temperatura_c": 23.4,
    "radiacao_msv": 65.0,
    "qualidade_comunicacao": 82,
    "sensor_oxigenio": 1
  }
}
```

## Exemplo de saida do sistema

Trecho de uma execucao real:

```text
========================================================================
Relatorio final - Ares Habitat Experimental
========================================================================
Leituras analisadas: 1200
Ultima leitura: 2026-02-19T23
Status da missao: ALERTA

Previsao por media movel simples:
- Consumo previsto: 59.18 kWh
- Geracao prevista: 15.53 kWh

Inconsistencias detectadas: 1
- 2026-01-14T21: Suporte a vida ativo com sensor de oxigenio desligado.

Alertas:
[CRITICO] 2026-02-19T23
Energia abaixo de 20%.
Recomendacao: Desligar sistemas nao essenciais.

[ALERTA] 2026-01-14T21
Suporte a vida ativo com sensor de oxigenio desligado.
Recomendacao: Auditar sensores relacionados antes da proxima decisao operacional.

Recomendacoes:
- Ativar modo economia e desligar laboratorio temporariamente.
```

## Recomendacoes geradas pelo sistema

O sistema pode gerar as seguintes recomendacoes automaticas:

- Acionar protocolo critico da missao.
- Ativar modo economia e desligar laboratorio temporariamente.
- Ativar comunicacao de emergencia.
- Suspender atividades externas.
- Priorizar suporte a vida e auditar sensores de oxigenio.
- Manter operacao normal e monitoramento horario.

Tambem ha recomendacoes vinculadas aos alertas:

- Priorizar energia e acionar protocolo de contingencia em caso de falha no suporte a vida.
- Reiniciar modulo e ativar comunicacao de emergencia quando a comunicacao esta instavel.
- Desligar sistemas nao essenciais quando a energia fica abaixo de 20%.
- Reduzir consumo nao essencial quando a energia fica abaixo de 40%.
- Suspender atividades externas e mover equipe para area protegida quando a radiacao passa de 90 mSv.
- Auditar sensores quando inconsistencias sao detectadas.

## Link do video no YouTube

[Link do Youtube](https://youtu.be/DV2pMl7_dq8)

## Conclusoes e aprendizados

O projeto demonstrou como estruturas de dados e regras logicas podem ser combinadas para criar um sistema simples de apoio a decisao. A leitura de telemetria permitiu transformar dados brutos em diagnostico operacional, alertas e recomendacoes praticas.

Os principais aprendizados foram:

- Organizar dados de diferentes tipos em estruturas adequadas melhora a clareza do sistema.
- Regras booleanas ajudam a transformar condicoes tecnicas em classificacoes operacionais.
- A media movel simples e uma tecnica acessivel para estimar tendencias de consumo e geracao.
- A deteccao de inconsistencias e essencial em sistemas criticos, pois sensores podem indicar estados contraditorios.
- Recomendacoes automaticas tornam o diagnostico mais util para tomada de decisao.
