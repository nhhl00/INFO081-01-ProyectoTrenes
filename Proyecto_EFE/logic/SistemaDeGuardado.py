import tkinter as tk
from tkinter import messagebox

class SistemaDeGuardado:
    def __init__(self, ruta_base="data/"):
        self.ruta_base = ruta_base

    def guardar_simulacion(self, estado_simulacion):
        def guardar():
            nombre = entrada.get().strip()
            if not nombre:
                messagebox.showwarning("Aviso", "Debes ingresar un nombre de archivo")
                return
            ruta = f"{self.ruta_base}{nombre}.txt"
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    for k, v in estado_simulacion.items():
                        f.write(f"{k}={v}\n")
                messagebox.showinfo("Éxito", f"Simulación guardada en:\n{ruta}")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ventana = tk.Tk()
        ventana.title("Guardar Simulación")
        tk.Label(ventana, text="Nombre del archivo:").pack(pady=5)
        entrada = tk.Entry(ventana)
        entrada.pack(pady=5)
        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
        ventana.mainloop()

    def cargar_simulacion(self):
        datos = {}
        def cargar():
            nombre = entrada.get().strip()
            if not nombre:
                messagebox.showwarning("Aviso", "Debes ingresar un nombre de archivo")
                return
            ruta = f"{self.ruta_base}{nombre}.txt"
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    for linea in f:
                        if "=" in linea:
                            k, v = linea.strip().split("=", 1)
                            datos[k] = v
                messagebox.showinfo("Éxito", f"Simulación cargada desde:\n{ruta}")
                ventana.destroy()
            except FileNotFoundError:
                messagebox.showerror("Error", f"No se encontró el archivo '{ruta}'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar:\n{e}")

        ventana = tk.Tk()
        ventana.title("Cargar Simulación")
        tk.Label(ventana, text="Nombre del archivo:").pack(pady=5)
        entrada = tk.Entry(ventana)
        entrada.pack(pady=5)
        tk.Button(ventana, text="Cargar", command=cargar).pack(pady=10)
        ventana.mainloop()
        return datos if datos else None
