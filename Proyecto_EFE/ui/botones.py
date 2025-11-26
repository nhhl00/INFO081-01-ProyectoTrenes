import tkinter as tk
from tkinter import ttk

def fn_botones(parent):
    #Define el frame para todos los botones
    frame_para_botones = ttk.Frame(parent)

    #Crear los botones
    boton_iniciar_simulacion = ttk.Button(frame_para_botones, text="Iniciar simulación")
    boton_iniciar_simulacion.pack(side=tk.BOTTOM,padx=5)

    boton_cargar_simulacion = ttk.Button(frame_para_botones, text="Cargar simulación")
    boton_cargar_simulacion.pack(side=tk.BOTTOM, padx=5)

    boton_salir_simulacion = ttk.Button(frame_para_botones, text="Salir")
    boton_salir_simulacion.pack(side=tk.BOTTOM, padx=5)
    
    boton_configurar_simulacion = ttk.Button(frame_para_botones, text="Configuracion de simulacion")
    boton_configurar_simulacion.pack(side=tk.BOTTOM, padx=5)

    #referencias
    return {
        "frame_para_botones": frame_para_botones,
        "boton_iniciar_simulacion": boton_iniciar_simulacion,
        "boton_cargar_simulacion": boton_cargar_simulacion,
        "boton_salir_simulacion": boton_salir_simulacion,
        "boton_configurar_simulacion": boton_configurar_simulacion,
    }


    
    
import tkinter as tk
from tkinter import ttk

def fn_botones(parent):
    #Define el frame para todos los botones
    frame_para_botones = ttk.Frame(parent)
    # Layout: left and right frames so we can put a save button bottom-right
    left_frame = ttk.Frame(frame_para_botones)
    left_frame.pack(side=tk.LEFT)
    right_frame = ttk.Frame(frame_para_botones)
    right_frame.pack(side=tk.RIGHT)

    #Crear los botones (izquierda)
    boton_iniciar_simulacion = ttk.Button(left_frame, text="Iniciar simulación")
    boton_iniciar_simulacion.pack(side=tk.LEFT,padx=5)

    boton_cargar_simulacion = ttk.Button(left_frame, text="Cargar simulación")
    boton_cargar_simulacion.pack(side=tk.LEFT, padx=5)

    boton_configurar_simulacion = ttk.Button(left_frame, text="Configuracion de simulacion")
    boton_configurar_simulacion.pack(side=tk.LEFT, padx=5)

    boton_salir_simulacion = ttk.Button(left_frame, text="Salir")
    boton_salir_simulacion.pack(side=tk.LEFT, padx=5)

    # botón Guardar en la esquina derecha
    boton_guardar_simulacion = ttk.Button(right_frame, text="Guardar simulación")
    boton_guardar_simulacion.pack(side=tk.RIGHT, padx=5)

    #referencias
    return {
        "frame_para_botones": frame_para_botones,
        "boton_iniciar_simulacion": boton_iniciar_simulacion,
        "boton_cargar_simulacion": boton_cargar_simulacion,
        "boton_salir_simulacion": boton_salir_simulacion,
        "boton_configurar_simulacion": boton_configurar_simulacion,
        "boton_guardar_simulacion": boton_guardar_simulacion,
    }


    
    