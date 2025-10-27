class Proceso:
    def __init__(self, nombre, arribo, duracion, tamano):
        self.nombre = nombre
        self.arribo = arribo
        self.duracion = duracion
        self.tamano = tamano

    def mostrarInfo(self):
        print("Nombre del proceso: ",self.nombre)
        print("Tiempo de arribo: ",self.arribo)
        print("Duración del proceso: ",self.duracion)
        print("Tamaño del proceso: ",self.tamano)

    def getNombre(self):                
        return self.nombre

    def getArribo(self):
        return self.arribo

    def getDuracion(self):
        return self.duracion

    def getTamano(self):
        return self.tamano
    
    def setNombre(self, nombre):
        if not isinstance(nombre, str):
            raise TypeError("Nombre debe ser una cadena de texto (string)")
        self.nombre = nombre

    def setArribo(self, arribo):
        if not isinstance(arribo, (int, float)):
            raise TypeError("Arribo debe ser un número real")
        self.arribo = float(arribo)

    def setDuracion(self, duracion):
        if not isinstance(duracion, (int, float)):
            raise TypeError("Duración debe ser un número real")
        self.duracion = float(duracion)

    def setTamano(self, tamano):
        if not isinstance(tamano, int):
            raise TypeError("Tamaño debe ser un entero (int)")
        self.tamano = tamano


    def cargarProceso(self, nombre, arribo, duracion, tamano):
        self.setNombre(nombre)
        self.setArribo(arribo)
        self.setDuracion(duracion)
        self.setTamano(tamano)
        return self 
    
    