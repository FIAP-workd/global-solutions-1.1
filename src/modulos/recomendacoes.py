class RecomendadorOperacional:
    def recomendar(self, status, leitura, consumo_previsto, geracao_prevista):
        recomendacoes = []
        energia = leitura.energia
        ambiente = leitura.ambiente
        modulos = leitura.modulos

        if status == "CRITICO":
            recomendacoes.append("Acionar protocolo critico da missao.")

        if energia["bateria_percentual"] < 40 or consumo_previsto > geracao_prevista:
            recomendacoes.append("Ativar modo economia e desligar laboratorio temporariamente.")

        if modulos["comunicacao"] == 0 or ambiente["qualidade_comunicacao"] < 40:
            recomendacoes.append("Ativar comunicacao de emergencia.")

        if ambiente["radiacao_msv"] > 70:
            recomendacoes.append("Suspender atividades externas.")

        if modulos["suporte_vida"] == 0 or ambiente["sensor_oxigenio"] == 0:
            recomendacoes.append("Priorizar suporte a vida e auditar sensores de oxigenio.")

        if not recomendacoes:
            recomendacoes.append("Manter operacao normal e monitoramento horario.")

        return recomendacoes
