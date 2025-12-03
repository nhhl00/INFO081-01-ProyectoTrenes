import tkinter as tk
from tkinter import ttk

def fn_botones(parent):
    frame_para_botones = ttk.Frame(parent)

    boton_iniciar_simulacion = ttk.Button(frame_para_botones, text="Iniciar simulación")
    boton_iniciar_simulacion.pack(side=tk.TOP, padx=5, pady=5)
    
    boton_configurar_simulacion = ttk.Button(frame_para_botones, text="Configuración de simulación")
    boton_configurar_simulacion.pack(side=tk.TOP, padx=5, pady=5)

    boton_salir_simulacion = ttk.Button(frame_para_botones, text="Salir")
    boton_salir_simulacion.pack(side=tk.TOP, padx=5, pady=5)

    return {
        "frame_para_botones": frame_para_botones,
        "boton_iniciar_simulacion": boton_iniciar_simulacion,
        "boton_salir_simulacion": boton_salir_simulacion,
        "boton_configurar_simulacion": boton_configurar_simulacion,
    }