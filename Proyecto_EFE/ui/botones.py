import tkinter as tk
from tkinter import ttk

def fn_botones(parent):
    #Define el frame para todos los botones
    frame_para_botones = ttk.Frame(parent)
    frame_para_botones.pack(pady=10, padx=10)

    #Crear los botones
    boton_iniciar_simulacion = ttk.Button(frame_para_botones, text="Iniciar simulación")
    boton_iniciar_simulacion.pack(side=tk.LEFT,padx=5)

    boton_cargar_simulacion = ttk.Button(frame_para_botones, text="Cargar simulación")
    boton_cargar_simulacion.pack(side=tk.LEFT, padx=5)

    #referencias
    return {
        "frame": frame_para_botones,
        "iniciar simulación": boton_iniciar_simulacion,
        "Cargaar simulacion": boton_cargar_simulacion,
    }


    
    