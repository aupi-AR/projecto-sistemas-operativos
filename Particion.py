class Particion:
    def __init__(self,nombre,proceso,tamano):
        self.nombre=nombre
        self.proceso=proceso
        self.tamano=tamano

    def limpiarParticion(self):
        self.proceso=None