import tkinter as tk
from tkinter import ttk

def estructura_pestañas(parent, frame_botones):
    #Define frame de pestañas
    frame_pestañas = ttk.Notebook(parent)
    frame_pestañas.pack(pady=10,padx=10,fill="both",expand=True)

    def gestionar_botones_en_pestañas(event):
        #mostrar o ocultar botones en diferentes pestañas
        indice_sel = frame_pestañas.index(frame_pestañas.select())

        if indice_sel == 0:
            frame_botones.pack(side=tk.BOTTOM, pady=10, padx=10)

        else:
            frame_botones.pack_forget()

        frame_pestañas.bind("<<NotebookTabChanged>>", gestionar_botones_en_pestañas)
        return frame_pestañas

    #pestaña de inicio
    frame_inicio = ttk.Frame(frame_pestañas)
    #pestaña de simulacion
    frame_config  = ttk.Frame(frame_pestañas)
    #pestaña configuracion
    frame_simulacion = ttk.Frame(frame_pestañas)
    #texto para pestaña principal y fondos
    tk.Label(frame_inicio,text="Sistema de gestion de tráfico ferroviario EFE Chile",bg="#f5f2f4",font=("Arial", 14)).pack(padx=50, pady=50)
    tk.Label(frame_config,text="Gestion de trenes:",font=("Arial",12)).pack(side=tk.TOP)
    tk.Label(frame_simulacion, font=("Arial",12)).pack(side=tk.TOP)
    #añadir pestaña=
    frame_pestañas.add(frame_inicio,text="Inicio")
    frame_pestañas.add(frame_config,text="Configuracion")
    frame_pestañas.add(frame_simulacion,text="Simulacion")

    #referencias
    return frame_pestañas
















   

