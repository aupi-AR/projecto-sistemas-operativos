
from abc import abstractmethod


class Estrategia:
    @abstractmethod
    def seleccionarParticion(self,proceso, particiones,ultimaParticion):
        pass