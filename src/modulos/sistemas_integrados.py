from datetime import datetime
import pandas as pd
import numpy as np
import pvlib
import random
import math

from telemetria import Telemetria

def gerar_coordenadas_aleatorias():
    # Latitude: -90 a 90 graus
    lat = random.uniform(-90.0, 90.0)
    # Longitude: -180 a 180 graus
    lon = random.uniform(-180.0, 180.0)
    return lat, lon

class Sistemas:

    def __init__(self, nome: str, tipo: str, criticidade):
        self.modulos_telemetria = [ 
            "communication_system",
            "power_system"
        ]
        self._nome = nome
        self.tipo = tipo
        self.telemetria = Telemetria(self.modulos_telemetria)
        self.telemetria.validacoes_telemetria()
        self.criticidade = criticidade
        

    # Exclusivo para sistema de geração de energia
    def geracao_energia_solar(self, 
                        now,
                        coordenadas_operacao: list,
                        potencia_instalada_kwp: float = 1000, 
                        fator_perda: float = 0.8):
        """
        Define geração de energia da última hora do módulo de energia.
        Temos um fator de perda de 0.8, para representar a perda da radiação solar no meio do caminho.
        Além disso, usamos um fator no cálculo da potencia de 0.85 que é a capacidade dos nossos módulos solares de traduzir a radiação em energia, transformando em média 85% do valor.
        """
        posicao_solar = pvlib.solarposition.get_solarposition(now, *coordenadas_operacao)
        elevation = posicao_solar['elevation'].iloc[0]

        if elevation < 0:
            geracao_solar = 0
        
        else:
            irradiancia = 1000 * np.sin(np.radians(elevation)) * fator_perda

            geracao_solar = potencia_instalada_kwp * (irradiancia/1000) * 0.85
           
        return geracao_solar
    

    # Exclusivo para sistema de geração de energia
    def geracao_eolica(self,
                       velocidade_vento: float,
                       turbinas: int = 5,
                       densidade_atmosfera:float = 0.02,
                       coeficiente_potencia:float = 0.35
                       ):
        """
        Além das geração de energia solar, temos também a geração de energia eólica.
        Aqui precisamos do diametro_rotor e numero de turbinas funcionais.
        Energia é calculada em kW/h
        """
        diametro_rotor = 50

        if velocidade_vento <= 0:
            energia_eolica = 0

        else:
            potencia_watts = (
                0.5
                * densidade_atmosfera
                * (math.pi*((diametro_rotor/2)**2))
                * (velocidade_vento ** 3)
                * coeficiente_potencia
                * turbinas
            )
            energia_eolica = potencia_watts/1000

        return energia_eolica
    

    # Exclusivo para sistema de geração de energia
    def geracao_energia(self, 
                            coordenadas_operacao,
                            velocidade_vento,
                            turbinas_funcionais,
                            densidade_atmosera
                        ):
        now = datetime.now()
        solar = self.geracao_energia_solar(now, coordenadas_operacao=coordenadas_operacao)
        eolica = self.geracao_eolica(velocidade_vento=velocidade_vento, turbinas=turbinas_funcionais, densidade_atmosfera=densidade_atmosera)
        energia_total = solar + eolica
        return now, energia_total
    

    def valida_energia_sistema(self, energia_total_colonia):
        nivel_bateria = self.telemetria.nivel_bateria

        if nivel_bateria <=0.3:
            precisa_recarga = True
            urgente = True

        elif nivel_bateria <=0.6:
            precisa_recarga = True
            urgente = False

        else:
            precisa_recarga = False
            urgente = False
        
        return {
            "recarga": precisa_recarga,
            "urgência": urgente
        }
    
    
    @property
    def values(self):
        self.telemetria.validacoes_telemetria()
        dados = self.telemetria.valores
        modulo = dados.pop("modulos", {})
        dados.update(modulo)
        return dados