from sistemas_integrados import Sistemas


class Gerenciador:
    def __init__(self):
        self.lista_sistemas = []
        self.sistemas_alerta = []
        self.sistemas_perigo = []
        self.energia_colonia = None
        self.path_logs = r"logs\log_energia.txt"
        self.coordenadas:tuple = (-4.5, 137.4) # Cratera Gale
        self.dict_sistemas = {}


    def insere_sistema_integrado(self, nome, tipo, criticidade):
        sistema = Sistemas(nome, tipo, criticidade)
        self.lista_sistemas.append(sistema)
        self.dict_sistemas = self.define_dict_sistemas(sistema, tipo)
        

    def leitura_log_energia(self):
        pass


    def define_enegia_colonia(self):
        if self.energia_colonia is None:
            energia = self.get_last_energy_value()
    

    def define_dict_sistemas(self, sistema, tipo):
        dict_gerenciador = self.dict_sistemas
        value = dict_gerenciador.get(tipo, [])
        value.append(sistema)
        dict_gerenciador.update(tipo, value)
        return dict_gerenciador