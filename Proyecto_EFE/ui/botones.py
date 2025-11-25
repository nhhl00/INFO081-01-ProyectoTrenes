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


    
    