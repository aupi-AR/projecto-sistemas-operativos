import Particion
import Estrategia
import FirstFit
import BestFit
import NextFit
import WorstFit
from Proceso import Proceso
class Memoria:
    def __init__(self, tamano, estrategia, tiempoSeleccion, PromedioCarga, TiempoLiberacion, procesos):
        self.tamano = tamano
        self.setEstrategia(estrategia)
        self.tiempoSeleccion = tiempoSeleccion
        self.PromedioCarga = PromedioCarga
        self.TiempoLiberacion = TiempoLiberacion
        self.estado = "libre"  
        self.particiones = [Particion.Particion("p0", None, self.tamano, 0, self.tamano)]
        
        

        self.procesos = []
        for p in procesos:
            proceso = Proceso(
                p["nombre"],          
                p["tiempo_arribo"],    
                p["duracion"],         
                p["memoria_requerida"] 
            )
            self.procesos.append(proceso)
        
        # Ordenar por tiempo de arribo
        self.procesos.sort(key=lambda x: x.getArribo())
        
        # Atributos que uso en la simulación
        self.nroParticion = 1
        self.procesosTerminados = []
        self.fragmentacion = 0
        self.tiempo = 0
        self.ultimaParticion = 0  # Cambiar de -1 a 0
        self.ready = []
        self.finalizando = []
   

    def mostrarInfo(self):
        print("Tamaño de la memoria: ",self.tamano)
        print("Estrategia de asignación: ",self.estrategia)
        print("Tiempo de selección: ",self.tiempoSeleccion)
        print("Promedio de carga: ",self.PromedioCarga)
        print("Tiempo de liberación: ",self.TiempoLiberacion)

        
    def getTamano(self):
        return self.tamano  
    
    def getEstrategia(self):
        return self.estrategia
    
    def getTiempoSeleccion(self):
        return self.tiempoSeleccion
    
    def getPromedioCarga(self):
        return self.PromedioCarga
    
    def getTiempoLiberacion(self):  
        return self.TiempoLiberacion
    

    def getEstado(self):
        return self.estado
    
    def setTamano(self, tamano):
        if not isinstance(tamano, int):
            raise TypeError("Tamaño debe ser un entero (int)")
        if tamano <= 0:
            raise ValueError("Tamaño debe ser mayor que 0")
        self.tamano = tamano

    def setEstrategia(self, estrategia):
        if isinstance(estrategia, str):
            if estrategia == "FirstFit":
                self.estrategia = FirstFit.FirstFit()
            elif estrategia == "BestFit":
                self.estrategia = BestFit.BestFit()
            elif estrategia == "NextFit":
                self.estrategia = NextFit.NextFit()
            elif estrategia == "WorstFit":
                self.estrategia = WorstFit.WorstFit()
            else:
                raise ValueError(f"Estrategia '{estrategia}' no reconocida")
        else:
            self.estrategia = estrategia


    def setTiempoSeleccion(self, tiempoSeleccion):
        if not isinstance(tiempoSeleccion, (int)):
            raise TypeError("Tiempo de selección debe ser un número")
        tiempoSeleccion = int(tiempoSeleccion)
        if tiempoSeleccion < 0:
            raise ValueError("Tiempo de selección no puede ser negativo")
        self.tiempoSeleccion = tiempoSeleccion

    def setPromedioCarga(self, PromedioCarga):
        if not isinstance(PromedioCarga, (int)):
            raise TypeError("Promedio de carga debe ser un número")
        PromedioCarga = int(PromedioCarga)
        if PromedioCarga < 0:
            raise ValueError("Promedio de carga no puede ser negativo")
        self.PromedioCarga = PromedioCarga

    def setTiempoLiberacion(self, TiempoLiberacion):
        if not isinstance(TiempoLiberacion, (int)):
            raise TypeError("Tiempo de liberación debe ser un número")
        TiempoLiberacion = int(TiempoLiberacion)
        if TiempoLiberacion < 0:
            raise ValueError("Tiempo de liberación no puede ser negativo")
        self.TiempoLiberacion = TiempoLiberacion

    def cargarMemoria(self, tamano, estrategia, tiempoSeleccion, PromedioCarga, TiempoLiberacion):
        try:
            tamano = int(tamano)
            tiempoSeleccion = int(tiempoSeleccion)
            PromedioCarga = int(PromedioCarga)
            TiempoLiberacion = int(TiempoLiberacion)

            self.setTamano(tamano)
            self.setEstrategia(estrategia)
            self.setTiempoSeleccion(tiempoSeleccion)
            self.setPromedioCarga(PromedioCarga)
            self.setTiempoLiberacion(TiempoLiberacion)
            return self
        except ValueError as ve:
            print("error de conversión:", ve)
    


    

    def decrementarTiempos(self,):
        for particion in self.particiones:
            if particion.proceso is not None and particion.estado == "ejecutando":
                particion.proceso.duracion -= 1
                if particion.proceso.duracion <= 0:
                    particion.estado="finalizando"
                    if particion not in self.finalizando:
                        self.finalizando.append(particion)
               
                    






    def asignarParticion(self, proceso, index):
        # Seguridad: no permitir índices fuera de rango
        if index < 0 or index >= len(self.particiones):
            print(f"⚠️ Índice {index} fuera de rango. Particiones disponibles: {len(self.particiones)}")
            return

        particion = self.particiones[index]

        # Si la partición encaja justo
        if particion.tamano == proceso.tamano:
            particion.proceso = proceso
            particion.estado = "cargando"
        else:
            # Calcular el tamaño libre restante
            tamano_libre = particion.tamano - proceso.tamano

            # Actualizar la partición ocupada
            particion.proceso = proceso
            particion.estado = "cargando"
            particion.fin = particion.inicio + proceso.tamano  # ← corregido
            particion.tamano = proceso.tamano

            # Crear nueva partición libre solo si sobra espacio
            if tamano_libre > 0:
                nueva_inicio = particion.fin
                nueva_fin = nueva_inicio + tamano_libre
                nueva_particion = Particion.Particion(
                    "P" + str(self.nroParticion),
                    None,
                    tamano_libre,
                    nueva_inicio,
                    nueva_fin
                )
                nueva_particion.estado = "libre"
                self.particiones.insert(index + 1, nueva_particion)

            self.nroParticion += 1

                   

    def unirParticionesLibres(self,):
        i = 0
        while i < len(self.particiones) - 1:
            particion_actual = self.particiones[i]
            particion_siguiente = self.particiones[i + 1]
            if particion_actual.estado=="libre"  and particion_siguiente.estado=="libre":
                particion_actual.tamano += particion_siguiente.tamano
                particion_actual.fin=particion_actual.fin+particion_siguiente.tamano
                del self.particiones[i + 1]
            else:
                i += 1






    def ejecutarFinalizacion(self,):
        while len(self.finalizando) > 0:
            pop = self.finalizando.pop(0)
            pop.cargarEvento(self.tiempo, self.tiempo + self.TiempoLiberacion, "finalizando") 
            
            for t in range(self.TiempoLiberacion):
                self.tiempo += 1
                self.decrementarTiempos()
                self.calcularFragmentacion()
            
            self.procesosTerminados.append(pop.proceso)
            
            if pop.proceso in self.ready:
                self.ready.remove(pop.proceso)
                print("Se libero la particion", pop.getNombre(), "del proceso:", pop.proceso.getNombre(), "en el tiempo:", self.tiempo)
            else:
                print(f"⚠️ Advertencia: Proceso {pop.proceso.getNombre()} no encontrado en ready al momento de liberar.")

            pop.limpiarParticion()
            self.unirParticionesLibres()



    def meterEnReady(self,proceso):
        
        self.ready.append(proceso)
        self.procesos.remove(proceso)
        

    def ejecutarCarga(self,proceso):
        cargado=False
        while cargado!=True:
            if len(self.finalizando)==0:
                    proceso.cargarEvento(self.tiempo,self.tiempo+self.PromedioCarga,"cargando") 
                    for i in range(self.PromedioCarga):
                        self.tiempo+=1
                        self.decrementarTiempos()
                        self.calcularFragmentacion()
                    self.meterEnReady(proceso)
                    proceso.cargarEvento(self.tiempo,self.tiempo+proceso.duracion,"ejecutando")
                    cargado=True
            else: 
                    self.ejecutarFinalizacion()
                    proceso.cargarEvento(self.tiempo,self.tiempo+self.PromedioCarga)           
        

    def calcularFragmentacion(self,):
        frag=0
        if self.procesos:
            for p in self.particiones:
                if p.estado=="libre":
                    frag+=p.tamano
            self.fragmentacion+=frag


    def simulacion(self,):
        index=-1

        while len(self.ready)>0 or len(self.procesos)>0:
            proceso_actual = self.procesos[0]
            if self.getEstado()=="libre" and proceso_actual.getArribo()<=self.tiempo:
                index,self.ultimaParticion=self.estrategia.indiceParticion(proceso_actual,self.particiones,self.ultimaParticion)
                if index != -1:
                    proceso_actual.cargarTamano(self.particiones[index].inicio,self.particiones[index].inicio)
                    print("DEBUG → tiempo:", self.tiempo, 
      "proceso:", proceso_actual.getNombre(),
      "índice:", index,
      "cantidad particiones:", len(self.particiones))

                    self.asignarParticion(proceso_actual,index)
                    print("DEBUG → tiempo:", self.tiempo, 
      "proceso:", proceso_actual.getNombre(),
      "índice:", index,
      "cantidad particiones:", len(self.particiones))

                    proceso_actual.cargarEvento(self.tiempo,self.tiempo+self.tiempoSeleccion,"seleccion")
                    for i in range(self.tiempoSeleccion):
                        self.tiempo+=1
                        self.decrementarTiempos()
                        self.calcularFragmentacion()
                    
                        
                    self.ejecutarCarga(proceso_actual)
                    self.nroParticion+=1
        
                else:
                    self.tiempo+=1
                    self.decrementarTiempos()
                    if len(self.finalizando)>0:
                        self.ejecutarFinalizacion()
                        
                        #memoria.calcularFragmentacion()
            else:
                self.tiempo+=1
                self.decrementarTiempos()
                if len(self.finalizando)>0:
                    self.calcularFragmentacion()
                    self.ejecutarFinalizacion()
                else:
                    self.calcularFragmentacion()

