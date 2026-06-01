from datetime import datetime
import pandas as pd
from src.modulos.sistemas_integrados import Sistemas


class Gerenciador:
    # Função de inicialização de sistemas
    def __init__(self):
        self.lista_sistemas = []
        self.sistemas_alerta = []
        self.sistemas_perigo = []
        self.energia_colonia = None
        self.path_logs = r"logs\log.txt"
        self.coordenadas:tuple = (-4.5, 137.4) # Cratera Gale
        self.dict_sistemas = {}


    # Função de inserção de sistemas integrados sendo o estilo 
    def insere_sistema_integrado(self, nome, tipo, criticidade):
        sistema = Sistemas(nome, tipo, criticidade)
        self.lista_sistemas.append(sistema)
        self.dict_sistemas = self.define_dict_sistemas(sistema, tipo)
        

    def define_energia_colonia(self):
        if self.energia_colonia is None:
            energia = self.get_last_energy_value()
    

    def define_dict_sistemas(self, sistema, tipo):
        dict_gerenciador = self.dict_sistemas
        value = dict_gerenciador.get(tipo, [])
        value.append(sistema)
        dict_gerenciador.update(tipo, value)
        return dict_gerenciador


    # Funções referente a logs de sistemas.
    def leitura_log(self):
        with open(self.path_logs, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        return conteudo
    

    def escrita_log(self, log_message):
        now = datetime.now()
        message = f"[{now}] {log_message} \n"
        with open(self.path_logs, "a", encoding="utf-8") as arquivo:
            arquivo.write(message)
        return 
