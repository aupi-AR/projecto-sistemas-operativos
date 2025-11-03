class Particion:
    def __init__(self,nombre,proceso,tamano,inicio,fin):
        self.nombre=nombre
        self.proceso=proceso
        self.tamano=tamano
        self.inicio=inicio
        self.fin=fin
        self.estado="Libre"

    def limpiarParticion(self):
        self.proceso=None
        self.estado="Libre"