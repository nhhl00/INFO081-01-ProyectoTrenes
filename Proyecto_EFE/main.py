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
    # comando para mostrar la cola de eventos en la UI
    def mostrar_eventos_ui():
        try:
            # debug: confirmar que el handler se ejecuta
            print('[DEBUG] mostrar_eventos_ui llamado')
            messagebox.showinfo('Debug', 'Ver eventos: handler llamado')
            if pestanas_instancia and hasattr(pestanas_instancia, 'mostrar_eventos_dialog'):
                pestanas_instancia.mostrar_eventos_dialog()
            else:
                messagebox.showinfo("Eventos", "No hay gestor de eventos disponible.")
        except Exception as e:
            print(f'[ERROR] mostrar_eventos_ui: {e}')
            messagebox.showerror("Error", f"No se pudo mostrar eventos: {e}")

    if "boton_listar_eventos" in crear_botones:
        crear_botones["boton_listar_eventos"].config(command=mostrar_eventos_ui)

    # Iniciar simulación automáticamente para pruebas y cerrar tras 5 segundos
    try:
        iniciar_simulacion()
    except Exception:
        pass
    root.mainloop()


if __name__ == "__main__":
    # Ejecutar sin diálogo modal para pruebas automatizadas
    main()