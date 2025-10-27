import Memoria
import projectoSO.Proceso as Proceso
import heapq



def cargarMemoria():
    print("ingrese el tamaño de la memoria:")
    tamano=int(input())
    print("ingrese la estrategia de asignación:")
    estrategia=input()
    print("ingrese el tiempo de selección:")
    tiempoSeleccion=float(input())
    print("ingrese el promedio de carga:")
    PromedioCarga=float(input())
    print("ingrese el tiempo de espera:")
    tiempoEspera=float(input())
    memoria=Memoria.Memoria(tamano,estrategia,tiempoSeleccion,PromedioCarga,tiempoEspera)
    return memoria

def cargarProceso():
    print("ingrese la cantidad de procesos a simular:")
    n=int(input("ingrese n: "))
    procesos=[]
    ready=[]

    for i in range(n):
        print("ingrese el nombre del proceso:")
        nombre=input()
        print("ingrese el tiempo de arribo:")
        arribo=float(input())
        print("ingrese la duracion del proceso:")
        duracion=float(input())
        print("ingrese el tamaño del proceso:")
        tamano=int(input())
        proceso=proceso.cargarProceso(nombre,arribo,duracion,tamano)
        procesos.append(proceso)
    procesos.sort(key=lambda p: p.arribo)
    

def simulacion():
    nroParticion=1
    tiempo=0
    memoria=cargarMemoria()
    procesos=cargarProceso()
    ready=[]
    
    while len(ready)>0 or len(procesos)>0:
        proceso_actual = procesos.pop(0)
        if proceso_actual.arribo>=tiempo:
            ready.append(proceso)
            procesos.remove(proceso)
            memoria.estrategia.aceptarProceso(proceso_actual)
        else:
            print("en el tiempo",tiempo,"no entraron nuevos procesos")
            tiempo+=1
        

