import Particion
from Estrategia import Estrategia

class FirstFit(Estrategia):

        def indiceParticion(self, proceso, particiones, ultimaParticion):
                i=-1
                for i in range(len(particiones)):
                        particion = particiones[i]
                        if particion.tamano >= proceso.tamano and particion.proceso is None:
                                return i,ultimaParticion

                return i,ultimaParticion

                        