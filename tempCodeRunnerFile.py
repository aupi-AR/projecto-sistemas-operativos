proceso1 = proceso("P1",  0, 5, 300)
proceso2 = proceso("P2",   0, 5, 500)
proceso3 = proceso("P3", 0, 5, 150)
proceso4 = proceso("P4", 6, 10, 100)
lista_de_procesos_nuevos = [proceso1, proceso2,proceso3,proceso4]
simulacion = Memoria(1000, estrategia, 2, 2, 3,lista_de_procesos_nuevos) 