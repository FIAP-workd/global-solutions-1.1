import json
from collections import deque
from pathlib import Path

from src.modulos.modelos import LeituraHoraria


class TelemetriaMissao:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.nome_missao = ""
        self.leituras = []

        self.consumo_energetico = []
        self.geracao_energetica = []
        self.temperaturas = []
        self.fila_alertas = deque()
        self.pilha_eventos_criticos = []
        self.modulos_por_nome = {}
        self.hierarquia_subsistemas = {}
        self.matriz_energia = []

    def carregar(self):
        dados = json.loads(self.caminho_arquivo.read_text(encoding="utf-8"))
        self.nome_missao = dados["missao"]
        self.leituras = [LeituraHoraria(**leitura) for leitura in dados["leituras"]]
        self._organizar_estruturas()
        return self

    def ultima_leitura(self):
        return self.leituras[-1]

    def ultimas_leituras(self, quantidade):
        return self.leituras[-quantidade:]

    def registrar_alerta(self, alerta):
        self.fila_alertas.append(alerta)

    def registrar_evento_critico(self, evento):
        self.pilha_eventos_criticos.append(evento)

    def processar_alertas(self):
        processados = []
        while self.fila_alertas:
            processados.append(self.fila_alertas.popleft())
        return processados

    def _organizar_estruturas(self):
        for leitura in self.leituras:
            energia = leitura.energia
            ambiente = leitura.ambiente

            self.consumo_energetico.append(energia["consumo_kwh"])
            self.geracao_energetica.append(energia["geracao_kwh"])
            self.temperaturas.append(ambiente["temperatura_c"])
            self.matriz_energia.append(
                [
                    energia["geracao_kwh"],
                    energia["consumo_kwh"],
                    energia["bateria_percentual"],
                ]
            )

            for evento in leitura.eventos:
                if "falha" in evento or "alerta" in evento or "inconsistencia" in evento:
                    self.registrar_evento_critico(
                        {
                            "timestamp": leitura.timestamp,
                            "evento": evento,
                        }
                    )

        self.modulos_por_nome = self.ultima_leitura().modulos
        self.hierarquia_subsistemas = self.ultima_leitura().subsistemas
