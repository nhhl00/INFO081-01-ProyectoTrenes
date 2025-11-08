import tkinter as tk
from tkinter import ttk

def botones(parent):
    boton_nueva_simulacion = ttk.Button(parent, text="Nueva Simulación")
    boton_nueva_simulacion.pack(padx = 10, pady = 5)
    boton_cargar_simulacion = ttk.Button(parent, text="Cargar Simulación")
    boton_cargar_simulacion.pack(padx = 10, pady = 5)