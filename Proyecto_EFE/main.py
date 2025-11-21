import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
#config:
from config import TITULO_VENTANA, DIMENSION_VENTANA, COLOR_VENTANA
#ui(botones):
from ui import fn_botones
#ui(ventanas):
from ui import estructura_pestaña_principal
#clases:
from models import *

def main():
    #Iniciar programa
    root = tk.Tk()
    root.title(TITULO_VENTANA)
    root.geometry(DIMENSION_VENTANA)
    root.configure(bg=COLOR_VENTANA)

    #ui(pestañas):
    crear_frames = estructura_pestaña_principal(root)
    #ui(botones):
    crear_botones = fn_botones(root)

    #otorgar comandos a botones
    crear_botones["boton_salir_simulacion"].config(command=lambda: root.destroy())
    crear_botones["boton_configurar_simulacion"].config(command=lambda: crear_frames.select(1))
    crear_botones["boton_iniciar_simulacion"].config(command=lambda: crear_frames.select(2))

    if crear_frames == 1 or crear_frames == 2:
        print("hola")



    root.mainloop()


if __name__ == "__main__":
    # Crear estaciones
    santiago = Estacion("Santiago", (0, 0))
    rancagua = Estacion("Rancagua", (50, 20))

    # Crear tren
    tren1 = Tren(id_tren="EFE01", capacidad=100, velocidad_max=120, ruta=[santiago, rancagua])

    # Crear pasajeros
    p1 = Pasajero(1, "Santiago", "Rancagua")
    p2 = Pasajero(2, "Santiago", "Rancagua")

    # Simulación simple
    santiago.recibir_pasajero(p1)
    santiago.recibir_pasajero(p2)

    santiago.embarcar_pasajeros(tren1)
    tren1.avanzar()

if __name__ == "__main__":
    main()




