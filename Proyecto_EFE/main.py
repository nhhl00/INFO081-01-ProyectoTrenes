import tkinter as tk
from tkinter import ttk, messagebox
#config:
from config import TITULO_VENTANA, DIMENSION_VENTANA, COLOR_VENTANA
#ui(botones):
from ui import fn_botones
#ui(ventanas):
from ui import Pestañas
#clases:
from models import *
#logica(Estado):

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
    crear_frames = Pestañas(root,frame_botones)
    # obtener la instancia de Pestañas (crear_frames puede ser el objeto Pestañas)
    if isinstance(crear_frames, Pestañas):
        pestanas_instancia = crear_frames
    else:
        pestanas_instancia = getattr(crear_frames, '_pestanas', None)

    #funcion para boton de salida
    def salir():
        try:
            if pestanas_instancia:
                try:
                    pestanas_instancia.parar_reloj()
                except Exception:
                    pass
        finally:
            root.destroy()
    #botones de salida y configuracion
    crear_botones["boton_salir_simulacion"].config(command=salir)
    crear_botones["boton_configurar_simulacion"].config(command=lambda: crear_frames.select(1))

    # funcion para iniciar la simulacion (cambiar a la pestaña simulacion y dibujar elementos de la pestaña)
    def iniciar_simulacion():
        if pestanas_instancia:
            try:
                pestanas_instancia.select(2)
                pestanas_instancia.dibujar_elementos()
                # iniciar actualización del reloj
                try:
                    pestanas_instancia.empezar_reloj()
                except Exception:
                    pass
            except IndexError:
                messagebox.showerror("Error!","Pestaña no existe")
            except Exception:
                messagebox.showerror("Error!", "Hubo un error inesperado")
    
    # Asignar comando al boton de iniciar simulación
    crear_botones["boton_iniciar_simulacion"].config(command=iniciar_simulacion)

    root.mainloop()


if __name__ == "__main__":
    messagebox.showinfo("Bienvenido al Programa","Utilizar el programa en pantalla completa")
    main()