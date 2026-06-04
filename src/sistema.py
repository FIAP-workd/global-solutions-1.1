from pathlib import Path

from src.modulos.alertas import CentralAlertas
from src.modulos.diagnostico import DiagnosticoOperacional
from src.modulos.gerador_dados import GeradorTelemetria
from src.modulos.previsao import PrevisorMediaMovel
from src.modulos.recomendacoes import RecomendadorOperacional
from src.modulos.telemetria import TelemetriaMissao


CAMINHO_TELEMETRIA = Path("data") / "telemetria.json"


class SistemaMonitoramentoMissao:
    def __init__(self, caminho_telemetria=CAMINHO_TELEMETRIA):
        self.caminho_telemetria = Path(caminho_telemetria)

    def executar(self):
        if not self.caminho_telemetria.exists():
            GeradorTelemetria(total_horas=1200).salvar(self.caminho_telemetria)

        telemetria = TelemetriaMissao(self.caminho_telemetria).carregar()
        diagnostico = DiagnosticoOperacional(telemetria)
        previsor = PrevisorMediaMovel(janela=3)

        status = diagnostico.classificar()
        inconsistencias = diagnostico.detectar_inconsistencias()
        alertas = CentralAlertas(telemetria).gerar(inconsistencias)

        consumo_previsto = previsor.prever(telemetria.consumo_energetico)
        geracao_prevista = previsor.prever(telemetria.geracao_energetica)
        recomendacoes = RecomendadorOperacional().recomendar(
            status,
            telemetria.ultima_leitura(),
            consumo_previsto,
            geracao_prevista,
        )

        self._exibir_relatorio(
            telemetria=telemetria,
            status=status,
            inconsistencias=inconsistencias,
            alertas=alertas,
            consumo_previsto=consumo_previsto,
            geracao_prevista=geracao_prevista,
            recomendacoes=recomendacoes,
        )

    def _exibir_relatorio(
        self,
        telemetria,
        status,
        inconsistencias,
        alertas,
        consumo_previsto,
        geracao_prevista,
        recomendacoes,
    ):
        ultima = telemetria.ultima_leitura()

        print("=" * 72)
        print(f"Relatorio final - {telemetria.nome_missao}")
        print("=" * 72)
        print(f"Leituras analisadas: {len(telemetria.leituras)}")
        print(f"Ultima leitura: {ultima.timestamp}")
        print(f"Status da missao: {status}")
        print()

        print("Estruturas de dados usadas:")
        print(f"- Lista de consumo: {len(telemetria.consumo_energetico)} valores")
        print(f"- Fila de alertas processados: {len(alertas)} alertas")
        print(f"- Log de eventos: {len(telemetria.log_eventos)} registros")
        print(f"- Pilha de eventos criticos: {len(telemetria.pilha_eventos_criticos)} eventos")
        print(f"- Dicionario de modulos: {telemetria.modulos_por_nome}")
        print(f"- Hierarquia de subsistemas: {telemetria.hierarquia_subsistemas}")
        print(f"- Matriz energia [geracao, consumo, bateria]: {len(telemetria.matriz_energia)} linhas")
        print()

        print("Log de eventos - 8 registros selecionados:")
        for evento in telemetria.eventos_para_relatorio(8):
            print(f"- {evento['timestamp']} [{evento['tipo']}] {evento['descricao']}")
            print(f"  Detalhes: {evento['detalhes']}")
            print(f"  Acao recomendada: {evento['acao_recomendada']}")
        print()

        print("Previsao por media movel simples:")
        print(f"- Consumo previsto: {consumo_previsto} kWh")
        print(f"- Geracao prevista: {geracao_prevista} kWh")
        print()

        print(f"Inconsistencias detectadas: {len(inconsistencias)}")
        for item in inconsistencias[-3:]:
            print(f"- {item['timestamp']}: {item['descricao']}")
        print()

        print("Alertas:")
        if alertas:
            for alerta in alertas:
                print(alerta.formatado())
                print()
        else:
            print("- Nenhum alerta pendente.")
            print()

        print("Recomendacoes:")
        for recomendacao in recomendacoes:
            print(f"- {recomendacao}")


def main():
    SistemaMonitoramentoMissao().executar()


if __name__ == "__main__":
    main()
