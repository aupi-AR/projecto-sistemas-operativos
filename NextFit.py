import Particion
from Estrategia import Estrategia
class NextFit(Estrategia):

     def indiceParticion(self, proceso, particiones, ultimaParticion):
         if ultimaParticion==-1:
            for i in range(len(particiones)):
                particion = particiones[i]
                if particion.tamano >= proceso.tamano and particion.proceso is None:
                    ultimaParticion=i
                    index=i
                    return index,ultimaParticion
         else:
            final=len(particiones)
            cont=0
            while cont<final:
                indice=(ultimaParticion+1)%final
                particion=particiones[indice]
                if particion.tamano >= proceso.tamano and particion.proceso is None:
                    particion.proceso=proceso
                    ultimaParticion=indice
                    return indice, ultimaParticion
                cont+=1