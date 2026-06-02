from src.modulos.modelos import Alerta


class CentralAlertas:
    def __init__(self, telemetria):
        self.telemetria = telemetria

    def gerar(self, inconsistencias):
        leitura = self.telemetria.ultima_leitura()
        energia = leitura.energia
        ambiente = leitura.ambiente
        modulos = leitura.modulos

        if modulos["suporte_vida"] == 0:
            self._adicionar(
                "CRITICO",
                "Falha no suporte a vida.",
                "Priorizar energia e acionar protocolo de contingencia.",
                leitura.timestamp,
            )

        if modulos["comunicacao"] == 0 or ambiente["qualidade_comunicacao"] < 40:
            self._adicionar(
                "ALERTA",
                "Comunicacao instavel ou indisponivel.",
                "Ativar comunicacao de emergencia e reiniciar modulo.",
                leitura.timestamp,
            )

        if energia["bateria_percentual"] < 20:
            self._adicionar(
                "CRITICO",
                "Energia abaixo de 20%.",
                "Desligar sistemas nao essenciais.",
                leitura.timestamp,
            )
        elif energia["bateria_percentual"] < 40:
            self._adicionar(
                "ALERTA",
                "Energia abaixo de 40%.",
                "Reduzir consumo nao essencial.",
                leitura.timestamp,
            )

        if ambiente["radiacao_msv"] > 90:
            self._adicionar(
                "CRITICO",
                "Radiacao em nivel perigoso.",
                "Suspender atividades externas e mover equipe para area protegida.",
                leitura.timestamp,
            )

        for inconsistencia in inconsistencias[-3:]:
            self._adicionar(
                "ALERTA",
                inconsistencia["descricao"],
                "Auditar sensores relacionados antes da proxima decisao operacional.",
                inconsistencia["timestamp"],
            )

        return self.telemetria.processar_alertas()

    def _adicionar(self, severidade, mensagem, recomendacao, timestamp):
        self.telemetria.registrar_alerta(
            Alerta(
                severidade=severidade,
                mensagem=mensagem,
                recomendacao=recomendacao,
                timestamp=timestamp,
            )
        )
