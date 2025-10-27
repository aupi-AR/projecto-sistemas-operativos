import Particion

class FirstFit:


        def aceptarProceso(self, proceso, particiones, numeroParticion):
            auxiliar=[]
            for i in range(len(particiones)):
                particion = particiones[i]
                if particion.tamano >= proceso.tamano and particion.proceso is None:
                    if particion.tamano == proceso.tamano:
                        particion[i].proceso = proceso
                        return True
                    else:
                        nueva_particion = Particion("P" + str(numeroParticion), None, particion[i].tamano - proceso.tamano)
                        particion[i].proceso = proceso
                        particion[i].tamano -= proceso.tamano
                        for p in self.particiones:
                            if p == particion[i]:
                                auxiliar.append(particion[i])
                                auxiliar.append(nueva_particion)
                            else:
                                auxiliar.append(p)

            self.particiones = auxiliar