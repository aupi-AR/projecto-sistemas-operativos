import Particion
from Estrategia import Estrategia

class WorstFit(Estrategia):
        def indiceParticion(self, proceso, particiones,ultimaParticion):
            bigger_size = -1
            bigger_index = -1
            for i in range(len(particiones)):
                particion = particiones[i]
                if particion.tamano >= proceso.tamano and particion.proceso is None:
                    if particion.tamano > bigger_size:
                        bigger_size = particion.tamano
                        bigger_index = i
            
            return bigger_index,ultimaParticion


            
