import json
import random
from datetime import datetime, timedelta
from pathlib import Path


class GeradorTelemetria:
    def __init__(self, total_horas=1200, seed=42):
        self.total_horas = total_horas
        self.random = random.Random(seed)
        self.inicio = datetime(2026, 1, 1, 0, 0, 0)

    def gerar(self):
        leituras = []
        bateria = 82.0

        for hora in range(self.total_horas):
            timestamp = self.inicio + timedelta(hours=hora)
            hora_do_dia = timestamp.hour

            geracao = self._gerar_geracao(hora_do_dia)
            consumo = self._gerar_consumo(hora_do_dia)
            bateria = max(5.0, min(100.0, bateria + ((geracao - consumo) / 18)))

            modulos = self._gerar_modulos(hora)
            ambiente = self._gerar_ambiente(hora_do_dia, hora)
            subsistemas = self._gerar_subsistemas(modulos, ambiente)
            eventos = self._gerar_eventos(hora, modulos, ambiente, bateria)

            leituras.append(
                {
                    "timestamp": timestamp.isoformat(timespec="hours"),
                    "modulos": modulos,
                    "energia": {
                        "geracao_kwh": round(geracao, 2),
                        "consumo_kwh": round(consumo, 2),
                        "bateria_percentual": round(bateria, 2),
                    },
                    "ambiente": ambiente,
                    "subsistemas": subsistemas,
                    "eventos": eventos,
                }
            )

        return {
            "missao": "Ares Habitat Experimental",
            "descricao": "Telemetria horaria sintetica para diagnostico da missao.",
            "total_leituras": len(leituras),
            "leituras": leituras,
        }

    def salvar(self, caminho):
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        dados = self.gerar()
        caminho.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")
        return caminho

    def _gerar_geracao(self, hora_do_dia):
        if 6 <= hora_do_dia <= 18:
            fator_solar = 1 - abs(12 - hora_do_dia) / 6
            solar = 52 + (55 * max(0, fator_solar))
        else:
            solar = 0

        eolica = self.random.uniform(8, 26)
        return max(0, solar + eolica + self.random.uniform(-5, 5))

    def _gerar_consumo(self, hora_do_dia):
        base = 62 if 7 <= hora_do_dia <= 22 else 48
        pico_operacional = 14 if hora_do_dia in (9, 10, 15, 16) else 0
        return max(35, base + pico_operacional + self.random.uniform(-7, 9))

    def _gerar_modulos(self, hora):
        modulos = {
            "suporte_vida": 1,
            "energia": 1,
            "comunicacao": 1,
            "habitat": 1,
            "laboratorio": 1,
            "armazenamento": 1,
        }

        falhas_programadas = {
            180: "comunicacao",
            333: "suporte_vida",
            520: "energia",
            760: "laboratorio",
            980: "armazenamento",
        }

        if hora in falhas_programadas:
            modulos[falhas_programadas[hora]] = 0

        if self.random.random() < 0.015:
            modulo = self.random.choice(list(modulos.keys()))
            modulos[modulo] = 0

        if hora == 333:
            modulos["suporte_vida"] = 1

        return modulos

    def _gerar_ambiente(self, hora_do_dia, hora):
        temperatura = -34 + (8 if 10 <= hora_do_dia <= 16 else -6) + self.random.uniform(-4, 4)
        radiacao = self.random.uniform(22, 58)
        qualidade_comunicacao = self.random.uniform(72, 99)
        velocidade_vento = self.random.uniform(8, 42)
        sensor_oxigenio = 1

        if hora in (180, 181, 182):
            qualidade_comunicacao = self.random.uniform(18, 35)

        if hora in (420, 421, 422, 423):
            radiacao = self.random.uniform(91, 108)

        if hora == 333:
            sensor_oxigenio = 0

        return {
            "temperatura_c": round(temperatura, 2),
            "radiacao_msv": round(radiacao, 2),
            "qualidade_comunicacao": round(qualidade_comunicacao, 2),
            "velocidade_vento_kmh": round(velocidade_vento, 2),
            "sensor_oxigenio": sensor_oxigenio,
        }

    def _gerar_subsistemas(self, modulos, ambiente):
        return {
            "energia": {
                "paineis_solares": modulos["energia"] == 1,
                "baterias": modulos["energia"] == 1,
            },
            "habitat": {
                "oxigenio": ambiente["sensor_oxigenio"] == 1,
                "temperatura": -55 <= ambiente["temperatura_c"] <= 5,
                "comunicacao": modulos["comunicacao"] == 1,
            },
            "pesquisa": {
                "laboratorio": modulos["laboratorio"] == 1,
                "armazenamento": modulos["armazenamento"] == 1,
            },
        }

    def _criar_evento(self, tipo, descricao, detalhes, acao_recomendada):
        return {
            "tipo": tipo,
            "descricao": descricao,
            "detalhes": detalhes,
            "acao_recomendada": acao_recomendada,
        }

    def _gerar_eventos(self, hora, modulos, ambiente, bateria):
        eventos = []

        if hora % 168 == 0:
            eventos.append(
                self._criar_evento(
                    "reinicializacao",
                    "Reinicializacao preventiva semanal",
                    "Rotina programada para limpar estados temporarios e validar servicos essenciais.",
                    "Confirmar retorno dos modulos criticos e registrar qualquer falha pos-reinicializacao.",
                )
            )
        if bateria < 25:
            eventos.append(
                self._criar_evento(
                    "alerta",
                    "Bateria em nivel baixo",
                    f"Nivel atual da bateria: {bateria:.2f}%.",
                    "Reduzir consumo nao essencial e priorizar suporte a vida, comunicacao e energia.",
                )
            )
        if ambiente["radiacao_msv"] > 90:
            eventos.append(
                self._criar_evento(
                    "alerta",
                    "Radiacao elevada",
                    f"Radiacao medida: {ambiente['radiacao_msv']:.2f} mSv.",
                    "Suspender atividades externas e mover equipe para areas protegidas.",
                )
            )
        if ambiente["qualidade_comunicacao"] < 40:
            eventos.append(
                self._criar_evento(
                    "falha",
                    "Falha de comunicacao",
                    f"Qualidade do sinal caiu para {ambiente['qualidade_comunicacao']:.2f}%.",
                    "Ativar canal de emergencia e reiniciar o modulo de comunicacao.",
                )
            )
            eventos.append(
                self._criar_evento(
                    "falha_sensor",
                    "Falha no sensor de comunicacao",
                    "Leitura de comunicacao abaixo do limite minimo de confiabilidade.",
                    "Comparar com sensores redundantes e recalibrar o sensor principal.",
                )
            )
        if ambiente["sensor_oxigenio"] == 0:
            eventos.append(
                self._criar_evento(
                    "falha_sensor",
                    "Falha no sensor de oxigenio",
                    "Sensor de oxigenio retornou desligado enquanto o suporte a vida estava ativo.",
                    "Auditar sensor de oxigenio e validar leitura com sensor reserva.",
                )
            )

        for nome, status in modulos.items():
            if status == 0:
                eventos.append(self._evento_falha_modulo(nome))

        if hora == 333:
            eventos.append(
                self._criar_evento(
                    "inconsistencia",
                    "Inconsistencia entre suporte a vida e sensor de oxigenio",
                    "Suporte a vida marcado como operacional, mas sensor de oxigenio esta desligado.",
                    "Bloquear decisao automatica baseada nesse sensor ate concluir auditoria.",
                )
            )
        if hora in (250, 500, 750, 1000):
            eventos.append(self._evento_mudanca_prioridade(hora, bateria))
        if bateria < 35:
            eventos.append(
                self._criar_evento(
                    "modo_economico",
                    "Ativacao de modo economico",
                    f"Bateria em {bateria:.2f}%, abaixo do limite operacional de 35%.",
                    "Desligar laboratorio temporariamente e reduzir ciclos de processamento nao essenciais.",
                )
            )

        return eventos

    def _evento_falha_modulo(self, nome):
        detalhes_por_modulo = {
            "energia": (
                "Modulo de energia indisponivel ou operando fora do esperado. "
                "A geracao pode nao acompanhar o consumo e a bateria tende a cair."
            ),
            "comunicacao": "Modulo de comunicacao falhou, comprometendo envio de telemetria e comandos remotos.",
            "suporte_vida": "Modulo de suporte a vida falhou, colocando a seguranca da tripulacao em risco.",
            "habitat": "Modulo de habitat falhou, afetando controle ambiental interno.",
            "laboratorio": "Modulo de laboratorio falhou, exigindo pausa nas atividades cientificas.",
            "armazenamento": "Modulo de armazenamento falhou, podendo afetar persistencia de dados da missao.",
        }
        acoes_por_modulo = {
            "energia": "Ativar modo economia, verificar baterias e priorizar energia para suporte a vida.",
            "comunicacao": "Ativar canal de emergencia e reinicializar o modulo de comunicacao.",
            "suporte_vida": "Executar protocolo critico e redirecionar energia para suporte a vida.",
            "habitat": "Verificar temperatura, oxigenio e pressurizacao do habitat.",
            "laboratorio": "Suspender experimentos e isolar o laboratorio ate diagnostico.",
            "armazenamento": "Criar backup dos dados criticos e trocar para armazenamento redundante.",
        }
        return self._criar_evento(
            "falha_modulo",
            f"Falha no modulo {nome}",
            detalhes_por_modulo.get(nome, "Modulo critico apresentou falha operacional."),
            acoes_por_modulo.get(nome, "Isolar modulo e executar diagnostico manual."),
        )

    def _evento_mudanca_prioridade(self, hora, bateria):
        prioridades = {
            250: (
                "Prioridade alterada de pesquisa cientifica para comunicacao.",
                "Janela de transmissao com a base exigiu mais banda e estabilidade de sinal.",
                "Reduzir tarefas do laboratorio e reservar capacidade para envio de telemetria.",
            ),
            500: (
                "Prioridade alterada de operacao normal para conservacao de energia.",
                f"Bateria em {bateria:.2f}% e consumo projetado acima da geracao.",
                "Adiar tarefas nao essenciais e manter apenas suporte a vida, comunicacao e energia.",
            ),
            750: (
                "Prioridade alterada de pesquisa para protecao ambiental.",
                "Historico recente indicou maior risco ambiental para atividades externas.",
                "Suspender atividades externas e acompanhar radiacao nas proximas leituras.",
            ),
            1000: (
                "Prioridade alterada de manutencao rotineira para recuperacao operacional.",
                "Eventos acumulados indicaram necessidade de estabilizar sistemas antes de novas tarefas.",
                "Revisar modulos com falha, confirmar sensores e manter modo conservador.",
            ),
        }
        descricao, detalhes, acao = prioridades[hora]
        return self._criar_evento("mudanca_prioridade", descricao, detalhes, acao)


if __name__ == "__main__":
    caminho_saida = Path("data") / "telemetria.json"
    GeradorTelemetria(total_horas=1200).salvar(caminho_saida)
    print(f"Arquivo gerado: {caminho_saida}")
