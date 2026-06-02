class DiagnosticoOperacional:
    def __init__(self, telemetria):
        self.telemetria = telemetria

    def classificar(self):
        leitura = self.telemetria.ultima_leitura()
        bateria = leitura.energia["bateria_percentual"]
        radiacao = leitura.ambiente["radiacao_msv"]
        comunicacao = leitura.modulos["comunicacao"]
        suporte_vida = leitura.modulos["suporte_vida"]
        sensor_oxigenio = leitura.ambiente["sensor_oxigenio"]

        if (bateria < 20 and comunicacao == 0) or suporte_vida == 0 or radiacao > 90:
            return "CRITICO"
        elif bateria < 40 or radiacao > 70 or not sensor_oxigenio:
            return "ALERTA"
        else:
            return "NORMAL"

    def detectar_inconsistencias(self):
        inconsistencias = []

        for leitura in self.telemetria.leituras:
            suporte_vida_ativo = leitura.modulos["suporte_vida"] == 1
            sensor_oxigenio_desligado = leitura.ambiente["sensor_oxigenio"] == 0

            if suporte_vida_ativo and sensor_oxigenio_desligado:
                inconsistencias.append(
                    {
                        "timestamp": leitura.timestamp,
                        "descricao": "Suporte a vida ativo com sensor de oxigenio desligado.",
                    }
                )

        return inconsistencias
