import Particion


class Memoria:
    def __init__(self,tamano,estrategia,tiempoSeleccion,PromedioCarga,TiempoLiberacion):
        self.tamano = tamano
        self.estrategia = estrategia
        self.tiempoSeleccion = tiempoSeleccion
        self.PromedioCarga = PromedioCarga
        self.TiempoLiberacion = TiempoLiberacion
        self.particiones = [Particion("p0", None, self.tamano),]

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
    
    def setTamano(self, tamano):
        if not isinstance(tamano, int):
            raise TypeError("Tamaño debe ser un entero (int)")
        self.tamano = tamano

    def setEstrategia(self, estrategia):
        if not isinstance(estrategia, str):
            raise TypeError("Estrategia debe ser una cadena de texto (string)")
        self.estrategia = estrategia

    def setTiempoSeleccion(self, tiempoSeleccion):
        if not isinstance(tiempoSeleccion, (int, float)):
            raise TypeError("Tiempo de selección debe ser un número real")
        self.tiempoSeleccion = float(tiempoSeleccion)

    def setPromedioCarga(self, PromedioCarga):
        if not isinstance(PromedioCarga, (int, float)):
            raise TypeError("Promedio de carga debe ser un número real")
        self.PromedioCarga = float(PromedioCarga)

    def setTiempoLiberacion(self, TiempoLiberacion):
        if not isinstance(TiempoLiberacion, (int, float)):
            raise TypeError("Tiempo de liberación debe ser un número real")
        self.TiempoLiberacion = float(TiempoLiberacion)

    def cargarMemoria(self, tamano, estrategia, tiempoSeleccion, PromedioCarga, TiempoLiberacion):
        self.setTamano(tamano)
        self.setEstrategia(estrategia)
        self.setTiempoSeleccion(tiempoSeleccion)
        self.setPromedioCarga(PromedioCarga)
        self.setTiempoLiberacion(TiempoLiberacion)
        return self
    
    