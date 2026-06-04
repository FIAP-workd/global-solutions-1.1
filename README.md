# Global Solution 2026 - Monitoramento de Missao Espacial

Sistema orientado a objetos para monitorar uma missao espacial experimental a
partir de dados horarios de telemetria. Os dados simulam coletas de informações
de horas em horas de uma colônia

## Como executar

```bash
python -m src.sistema
```

Se `data/telemetria.json` nao existir, o sistema gera automaticamente uma base
com 1200 leituras horarias.

## Fluxo implementado

1. Leitura de arquivo externo JSON.
2. Organizacao dos dados em lista, fila, pilha, dicionario, hierarquia e matriz.
3. Deteccao de inconsistencia proposital.
4. Diagnostico operacional da missao.
5. Geracao de alertas.
6. Previsao por media movel simples.
7. Recomendacoes automaticas.
8. Exibicao de relatorio final.

## Expressao booleana principal

```text
CRITICO =
(bateria < 20 AND comunicacao == 0)
OR
(suporte_vida == 0)
OR
(radiacao > 90)
```

## Estruturas de dados

- Lista: consumo, geracao e temperatura.
- Fila: alertas pendentes, processados por ordem de chegada.
- Pilha: ultimos eventos criticos.
- Dicionario: consulta rapida dos modulos por nome.
- Hierarquia: subsistemas da missao.
- Matriz: leituras energeticas no formato `[geracao, consumo, bateria]`.
