from dataclasses import dataclass


@dataclass
class LeituraHoraria:
    timestamp: str
    modulos: dict
    energia: dict
    ambiente: dict
    subsistemas: dict
    eventos: list


@dataclass
class Alerta:
    severidade: str
    mensagem: str
    recomendacao: str
    timestamp: str

    def formatado(self):
        return (
            f"[{self.severidade}] {self.timestamp}\n"
            f"{self.mensagem}\n"
            f"Recomendacao: {self.recomendacao}"
        )
