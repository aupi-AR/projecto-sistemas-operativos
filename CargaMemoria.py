import tkinter
from tkinter import messagebox, filedialog
import Memoria
import json
import os
import Proceso  # Asumo que Proceso.py contiene la clase proceso (con __init__ correcto)

# 🚨 Importar todas las clases de estrategia y mapearlas
from Estrategia import Estrategia # Clase base (si la usas)
from FirstFit import FirstFit   # Implementación FirstFit

# Diccionario de registro de las clases de estrategia
# 💡 IMPORTANTE: Debes añadir el resto de tus clases (BestFit, NextFit, WorstFit) aquí
REGISTRO_ESTRATEGIAS = {
    "FirstFit": FirstFit,
    # "BestFit": BestFit,    
    # "NextFit": NextFit,
    # "WorstFit": WorstFit 
}

ventana = tkinter.Tk()
ventana.title("Cargar Memoria")
ventana.geometry("300x480")

# Variables globales
procesos = []
memoria = None

def cargar_json():
    """Función para abrir un diálogo y cargar un archivo JSON e instanciar objetos Proceso"""
    global procesos
    
    # Obtener la ruta del directorio actual
    directorio_inicial = os.path.dirname(os.path.abspath(__file__))
    
    # Abrir diálogo para seleccionar archivo
    archivo = filedialog.askopenfilename(
        initialdir=directorio_inicial,
        title="Selecciona un archivo JSON",
        filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*"))
    )
    
    if archivo:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
            # Convertir los datos del JSON en instancias de la clase Proceso
            procesos = []
            for proceso_data in datos:
                # Instanciar la clase Proceso
                nuevo_proceso = Proceso.proceso(
                    nombre=str(proceso_data.get("nombre", "")),
                    arribo=int(proceso_data.get("tiempo_arribo", 0)),
                    duracion=int(proceso_data.get("duracion", 0)),
                    tamano=int(proceso_data.get("memoria_requerida", 0)) 
                )
                procesos.append(nuevo_proceso)
            
            # Actualizar la etiqueta
            nombre_archivo = os.path.basename(archivo)
            etiqueta_archivo.config(
                text=f"Archivo: {nombre_archivo}\nProcesos: {len(procesos)}",
                fg="green"
            )
            
            messagebox.showinfo("Éxito", f"Se cargaron {len(procesos)} procesos correctamente")
            
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON no tiene un formato válido")
            procesos = []
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar/procesar los datos del archivo: {str(e)}")
            procesos = []

def cargar_memoria_wrapper():
    """Función wrapper para cargar la memoria con validaciones y construir la Estrategia"""
    global memoria, procesos
    
    if not procesos:
        messagebox.showwarning("Advertencia", "Primero debes cargar un archivo JSON con los procesos")
        return
    
    try:
        # 1. Validaciones de campos no vacíos y de selección
        if not cajaTexto1.get() or not cajaTexto2.get() or not cajaTexto3.get() or not cajaTexto4.get():
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos numéricos.")
            return

        nombre_estrategia = comboBox_estrategia.get()
        if nombre_estrategia == "Selecciona una estrategia":
            messagebox.showwarning("Advertencia", "Selecciona una estrategia de asignación")
            return
        
        # 2. Convertir valores a los tipos apropiados (maneja ValueError si no son números)
        tamanio_memoria = int(cajaTexto1.get())
        tiempo_seleccion = int(cajaTexto2.get())
        tiempo_liberacion = int(cajaTexto3.get())
        promedio_carga = int(cajaTexto4.get())
        
        # 3. Lógica Clave: Mapeo y Construcción de la Estrategia
        ClaseEstrategia = REGISTRO_ESTRATEGIAS.get(nombre_estrategia)

        if ClaseEstrategia is None:
            messagebox.showerror("Error", f"Estrategia '{nombre_estrategia}' no implementada en el registro.")
            return

        # 4. Instanciar el objeto Estrategia (usando el constructor __init__(self, nombre))
        objeto_estrategia = ClaseEstrategia(nombre_estrategia) 
        
        # 5. Crear el objeto Memoria pasándole el objeto Estrategia instanciado
        memoria = Memoria.Memoria(
            tamanio_memoria,
            objeto_estrategia, # ⬅️ Se pasa el OBJETO Estrategia
            tiempo_seleccion,
            promedio_carga,
            tiempo_liberacion,
            procesos
        )
        
        messagebox.showinfo("Éxito", "Memoria cargada correctamente")
        
    except ValueError:
        messagebox.showerror("Error", "Error en los valores ingresados: Los campos de tiempo y tamaño deben ser números enteros válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar la memoria: {str(e)}")

def ejecutar_simulacion():
    """Función para ejecutar la simulación"""
    global memoria
    
    if memoria is None:
        messagebox.showwarning("Advertencia", "Primero debes cargar la memoria")
        return
    
    try:
        memoria.simulacion()
        messagebox.showinfo("Éxito", "Simulación ejecutada correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar la simulación: {str(e)}")

def mostrar_info_wrapper():
    """Función wrapper para mostrar información de la memoria"""
    global memoria
    
    if memoria is None:
        messagebox.showwarning("Advertencia", "Primero debes cargar la memoria")
        return
    
    try:
        memoria.mostrarInfo() 
        messagebox.showinfo("Información", "Información de la memoria impresa en la consola.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar información: {str(e)}")

def graficar_eventos_wrapper():
    """Función wrapper para graficar eventos"""
    global memoria
    
    if memoria is None or not hasattr(memoria, 'procesosTerminados') or not memoria.procesosTerminados:
        messagebox.showwarning("Advertencia", "Primero debes ejecutar la simulación.")
        return
    
    try:
        memoria.graficar_eventos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al graficar eventos: {str(e)}")

def graficar_detallado_wrapper():
    """Función wrapper para graficar eventos detallados"""
    global memoria
    
    if memoria is None or not hasattr(memoria, 'procesosTerminados') or not memoria.procesosTerminados:
        messagebox.showwarning("Advertencia", "Primero debes ejecutar la simulación.")
        return
    
    try:
        memoria.graficar_eventos_detallado()
    except Exception as e:
        messagebox.showerror("Error", f"Error al graficar eventos detallados: {str(e)}")

def imprimir_resumen_wrapper():
    """Función wrapper para imprimir resumen"""
    global memoria
    
    if memoria is None or not hasattr(memoria, 'procesosTerminados') or not memoria.procesosTerminados:
        messagebox.showwarning("Advertencia", "Primero debes ejecutar la simulación.")
        return
    
    try:
        memoria.imprimir_resumen()
        messagebox.showinfo("Resumen", "Resumen de la simulación impreso en la consola.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al imprimir resumen: {str(e)}")

# --- UI Elements ---
etiqueta = tkinter.Label(ventana, text="Cargar Memoria", font=("Arial", 12, "bold"))
etiqueta.grid(row=0, column=0, columnspan=2, pady=10) 

# Botón para cargar JSON
botonJSON = tkinter.Button(
    ventana, 
    text="Cargar Archivo JSON", 
    command=cargar_json,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 9, "bold")
)
botonJSON.grid(row=1, column=0, columnspan=2, pady=5)

# Etiqueta para mostrar archivo cargado
etiqueta_archivo = tkinter.Label(ventana, text="No se ha cargado ningún archivo", fg="red")
etiqueta_archivo.grid(row=2, column=0, columnspan=2, pady=5)

# Carga de parámetros
etiqueta1 = tkinter.Label(ventana, text="Tamaño de la memoria:")
etiqueta1.grid(row=3, column=0, sticky="w", padx=5, pady=2) 
cajaTexto1 = tkinter.Entry(ventana)
cajaTexto1.grid(row=3, column=1, padx=5, pady=2)

etiqueta2 = tkinter.Label(ventana, text="Tiempo de selección:")
etiqueta2.grid(row=4, column=0, sticky="w", padx=5, pady=2) 
cajaTexto2 = tkinter.Entry(ventana)
cajaTexto2.grid(row=4, column=1, padx=5, pady=2)

etiqueta3 = tkinter.Label(ventana, text="Tiempo de liberación:")
etiqueta3.grid(row=5, column=0, sticky="w", padx=5, pady=2) 
cajaTexto3 = tkinter.Entry(ventana)
cajaTexto3.grid(row=5, column=1, padx=5, pady=2)

etiqueta4 = tkinter.Label(ventana, text="Promedio de carga:")
etiqueta4.grid(row=6, column=0, sticky="w", padx=5, pady=2) 
cajaTexto4 = tkinter.Entry(ventana)
cajaTexto4.grid(row=6, column=1, padx=5, pady=2)

# ComboBox de la estrategia de asignación
etiqueta5 = tkinter.Label(ventana, text="Estrategia de asignación:")
etiqueta5.grid(row=7, column=0, sticky="w", padx=5, pady=2)
comboBox_estrategia = tkinter.StringVar(ventana)
comboBox_estrategia.set("Selecciona una estrategia")

# Usamos las llaves del registro para el OptionMenu
opciones_estrategia = list(REGISTRO_ESTRATEGIAS.keys())
menu_estrategia = tkinter.OptionMenu(ventana, comboBox_estrategia, *opciones_estrategia)
menu_estrategia.grid(row=7, column=1, padx=5, pady=2)

# Botón para cargar la memoria
botonCargar = tkinter.Button(
    ventana,
    text="Cargar Memoria",
    command=cargar_memoria_wrapper
)
botonCargar.grid(row=8, column=0, columnspan=2, pady=5)

# Botón para ejecutar simulación
botonSimular = tkinter.Button(
    ventana,
    text="Ejecutar Simulación",
    command=ejecutar_simulacion,
    bg="#2196F3",
    fg="white"
)
botonSimular.grid(row=9, column=0, columnspan=2, pady=5)

# Botones de resultados
botonMostrar = tkinter.Button(ventana, text="Mostrar Info Memoria", command=mostrar_info_wrapper)
botonMostrar.grid(row=10, column=0, columnspan=2, pady=5)

botonGraficar = tkinter.Button(
    ventana, 
    text="Graficar Eventos", 
    command=graficar_eventos_wrapper,
    bg="#FF9800",
    fg="white"
)
botonGraficar.grid(row=11, column=0, columnspan=2, pady=5)

botonGraficarDetallado = tkinter.Button(
    ventana, 
    text="Graficar Eventos Detallado", 
    command=graficar_detallado_wrapper,
    bg="#9C27B0",
    fg="white"
)
botonGraficarDetallado.grid(row=12, column=0, columnspan=2, pady=5)

botonResumen = tkinter.Button(
    ventana, 
    text="Imprimir Resumen en Consola", 
    command=imprimir_resumen_wrapper
)
botonResumen.grid(row=13, column=0, columnspan=2, pady=5)

# Botón para cerrar
botonCerrar = tkinter.Button(ventana, text="Cerrar", command=ventana.quit)
botonCerrar.grid(row=14, column=0, columnspan=2, pady=5)

ventana.mainloop()