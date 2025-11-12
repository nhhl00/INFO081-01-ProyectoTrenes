import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from logic.SistemaDeGuardado import SistemaGuardado


#config:
TITULO_VENTANA = "Gestion de Trenes"
DIMENSION_VENTANA = "800x600"
COLOR_VENTANA = "#f5f2f4"

#ui(botones):
#ui(ventanas):

def main():
    root = tk.Tk()
    root.title(TITULO_VENTANA)
    root.geometry(DIMENSION_VENTANA)
    root.configure(bg=COLOR_VENTANA)

    #ui(ventana):
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, fill='both', expand=True)

    frame_inicio = ttk.Frame(notebook)
    frame_simulacion = ttk.Frame(notebook)

    tk.Label(frame_inicio, text="Sistema de gestion de tráfico ferroviario EFE Chile",bg="#f5f2f4",font=("Arial", 14)).pack(padx=50, pady=50)

    notebook.add(frame_inicio, text="Inicio")
    notebook.add(frame_simulacion, text="Simulación")

    #ui(botones):
    boton_nueva_simulacion = ttk.Button(root, text="Nueva Simulación", command = lambda:notebook.select(1))
    boton_nueva_simulacion.pack(padx = 10, pady = 5)
    boton_cargar_simulacion = ttk.Button(root, text="Cargar Simulación")
    boton_cargar_simulacion.pack(padx = 10, pady = 5)

    root.mainloop()



from models.clases import Tren
from models.clases import Estacion
from models.clases import Pasajero

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




