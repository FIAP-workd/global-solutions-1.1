class PrevisorMediaMovel:
    def __init__(self, janela=3):
        self.janela = janela

    def prever(self, valores):
        if len(valores) < self.janela:
            raise ValueError("Quantidade de valores insuficiente para a media movel.")

        ultimos_valores = valores[-self.janela :]
        return round(sum(ultimos_valores) / self.janela, 2)
