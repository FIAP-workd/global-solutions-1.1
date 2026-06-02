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

    def _gerar_eventos(self, hora, modulos, ambiente, bateria):
        eventos = []

        if hora % 168 == 0:
            eventos.append("reinicializacao preventiva semanal")
        if bateria < 25:
            eventos.append("alerta de bateria baixa")
        if ambiente["radiacao_msv"] > 90:
            eventos.append("alerta de radiacao elevada")
        if ambiente["qualidade_comunicacao"] < 40:
            eventos.append("falha de comunicacao")

        for nome, status in modulos.items():
            if status == 0:
                eventos.append(f"falha no modulo {nome}")

        if hora == 333:
            eventos.append("inconsistencia proposital: suporte de vida ativo com sensor de oxigenio desligado")
        if hora in (250, 500, 750, 1000):
            eventos.append("mudanca de prioridade operacional")
        if bateria < 35:
            eventos.append("ativacao de modo economico")

        return eventos


if __name__ == "__main__":
    caminho_saida = Path("data") / "telemetria.json"
    GeradorTelemetria(total_horas=1200).salvar(caminho_saida)
    print(f"Arquivo gerado: {caminho_saida}")
