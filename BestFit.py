import Particion
from Estrategia import Estrategia

class BestFit(Estrategia):
        def indiceParticion(self, proceso, particiones, ultimaParticion):

            melior_index = -1
            melior_size = -1
            for i in range(len(particiones)):
                particion = particiones[i]
                if particion.tamano >= proceso.tamano and particion.proceso is None:
                    if particion.tamano < melior_size:
                        melior_size = particion.tamano
                        melior_index = i
            
            return melior_index,ultimaParticion