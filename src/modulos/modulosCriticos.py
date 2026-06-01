import random

class ModulosCriticos:
    def __init__(self, nome):
      self.nome = nome
      self.status = None

    def __str__(self) -> str:
       return {self.nome:self.status}

    def testar_status(self):
        # Define os valores entre True e False com 95% de ser True, e 5% de ser False.
        self.status = random.choices([True, False], weights=[0.95, 0.05])[0]
        return self.status
    
