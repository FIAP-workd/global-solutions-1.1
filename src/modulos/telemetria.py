import random
from src.modulos.modulosCriticos import ModulosCriticos

class Telemetria:
    def __init__(self, list_modulos):
        """
        Nessa camada do __init__ iniciamos todos os atributos que vamos precisar para
        o módulo da Telemetria.
        """
        self.temperatura_interna = None   # Possui
        self.temperatura_externa = None   # Possui
        self.integridade_estrutural = None  # Possui
        self.pressao_tanque = None
        self.modulos = [ModulosCriticos(modulo) for modulo in list_modulos]
        self.dict_validacoes = None
        self.dict_auditoria = None
        self.dict_valores = None
        self.decisao_decolagem = None
        self.nivel_bateria = None
     

    @property
    def valores(self):
        return self.dict_valores

    # Funções para definir valores dos módulos
    def testar_todos_modulos(self):
        for modulo in self.modulos:
          modulo.testar_status()
        return self.modulos

    def captura_temperatura_interna(self):      # Está sendo calculada
        # Distribuição normal com média de 24 e desvio de 6, assim, eu aumento a possibilidade de cair entre o intervalo seguro
        self.temperatura_interna = max(-10, min(350, int(random.gauss(24,6))))   # Com essa distribuição, aumento as chances de cair um valor aleatório dentro do limite seguro de lançamento
        return self.temperatura_interna

    def captura_temperatura_externa(self):      # Está sendo calculada
        self.temperatura_externa = max(-80, min(100, int(random.gauss(25,8))))
        return self.temperatura_externa


    def captura_energy_lvl(self):     # Está sendo calculada
        self.nivel_bateria = random.betavariate(10,1)    # Com essa distribuição aumento as chances de cair entre 80 e 100 de energia.
        return self.nivel_bateria


    def captura_pressao_tanque(self):     # Está sendo calculada
        self.pressao_tanque = random.gauss(70,5)
        return self.pressao_tanque

    def captura_integridade_estrutural(self):   # Está sendo calculada
        self.integridade_estrutural = random.choices([True, False], weights=[0.9, 0.1])[0]
        return self.integridade_estrutural

    def captura_infos_telemetria(self):
        self.captura_temperatura_interna()
        self.captura_temperatura_externa()
        self.captura_integridade_estrutural()
        self.captura_energy_lvl()
        self.captura_pressao_tanque()


    # Funções de validação
    def validacoes_telemetria(self):
        """
        Captura todas as informações da telemetria e armazena
        em self.dict_valores.
        """

        self.testar_todos_modulos()
        self.captura_infos_telemetria()

        self.dict_valores = {
            'temperatura_interna': self.temperatura_interna,
            'temperatura_externa': self.temperatura_externa,
            'integridade_estrutural': self.integridade_estrutural,
            'pressao_tanque': self.pressao_tanque,
            'nivel_bateria': self.nivel_bateria,
            'modulos': {
                modulo.nome: modulo.status
                for modulo in self.modulos
            }
        }

        return self.dict_valores