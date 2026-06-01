from sistemas_integrados import Sistemas


class Gerenciador:
    def __init__(self):
        self.lista_sistemas = []
        self.sistemas_alerta = []
        self.sistemas_perigo = []
        self.energia_colonia = None
        self.path_logs = r"logs\log_energia.txt"


    def insere_sistema_integrado(self, nome, tipo, criticidade):
        _temp = Sistemas(nome, tipo, criticidade)
        self.lista_sistemas.append(_temp)
        
    def leitura_log_energia(self):
        pass

    def define_enegia_colonia(self):
        if self.energia_colonia is None:
            energia = self.get_last_energy_value()
    