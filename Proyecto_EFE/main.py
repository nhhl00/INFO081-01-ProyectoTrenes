import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
#config:
from config import TITULO_VENTANA, DIMENSION_VENTANA, COLOR_VENTANA
#ui(botones):
from ui import fn_botones
#ui(ventanas):
from ui import estructura_pestañas
#clases:
from models import *
#logica(Estado):
from logic import EstadoSimulacion

def main():
    #Iniciar programa
    root = tk.Tk()
    root.title(TITULO_VENTANA)
    root.geometry(DIMENSION_VENTANA)
    root.configure(bg=COLOR_VENTANA)


    #ui(ésta{as}):
    crear_botones = fn_botones(root)
    frame_botones = crear_botones["frame_para_botones"]
    frame_botones.pack(side=tk.BOTTOM, pady=10, padx=10)

    #ui(botones):
    crear_frames = estructura_pestañas(root,frame_botones)

    #otorgar comandos a botones
    crear_botones["boton_salir_simulacion"].config(command=lambda: root.destroy())
    crear_botones["boton_configurar_simulacion"].config(command=lambda: crear_frames.select(1))

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
    
    #funcion para comeranzar la simulacion
    def iniciar_simulacion():
        tren1.abordar_pasajero(p1)
        tren1.avanzar()

        print(f"Estado del Tren {tren1.id_tren}: {len(tren1.pasajeros)} pasajeros a bordo.")

        crear_frames.select(2)

    def funciones_para_simulacion():
        iniciar_simulacion()

        

    crear_botones["boton_iniciar_simulacion"].config(command=lambda: funciones_para_simulacion())


    
    root.mainloop()


if __name__ == "__main__":
    main()
