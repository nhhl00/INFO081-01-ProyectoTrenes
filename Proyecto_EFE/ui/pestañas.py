import tkinter as tk
from tkinter import ttk


class Pestanas:
    """Encapsula la estructura de pestañas (Notebook) y el control de los botones.

    Mantiene la interfaz del código previo: la función `estructura_pestañas` retorna
    el widget `Notebook` y anexa la instancia `Pestanas` como atributo `_pestanas`
    del notebook. Esto preserva compatibilidad con el código que usa
    `crear_frames.select(indice)`.
    """

    def __init__(self, parent, frame_botones):
        self.parent = parent
        self.frame_botones = frame_botones

        # Crear Notebook
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Crear frames para pestañas
        self.frame_inicio = ttk.Frame(self.notebook)
        self.frame_config = ttk.Frame(self.notebook)
        self.frame_simulacion = ttk.Frame(self.notebook)

        # Contenido base
        tk.Label(self.frame_inicio, text="Sistema de gestion de tráfico ferroviario EFE Chile",
                 bg="#f5f2f4", font=("Arial", 14)).pack(padx=50, pady=50)
        tk.Label(self.frame_config, text="Gestion de trenes:", font=("Arial", 12)).pack(side=tk.TOP)
        tk.Label(self.frame_simulacion, text="Hora:", font=("Arial", 10)).pack(side=tk.TOP)

        # Añadir pestañas
        self.notebook.add(self.frame_inicio, text="Inicio")
        self.notebook.add(self.frame_config, text="Configuracion")
        self.notebook.add(self.frame_simulacion, text="Simulacion")

        # Opcional: mantener índice de pestaña simulación
        self.sim_index = 2

        # Bind al cambio de pestaña para mostrar/ocultar botones
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        self._on_tab_changed()

    def _on_tab_changed(self, event=None):
        indice = self.notebook.indice(self.notebook.select())
        if indice == 0:
            self.frame_botones.pack(side=tk.BOTTOM, pady=10, padx=10)
        else:
            self.frame_botones.pack_forget()

    # Métodos públicos para compatibilidad
    def select(self, indice):
        return self.notebook.select(indice)

    def get_notebook(self):
        return self.notebook

    # métodos extra opcionales sin comportamiento por defecto
    def start(self):
        """Compat API placeholder: no-op (compatibilidad)"""
        return

    def stop(self):
        """Compat API placeholder: no-op (compatibilidad)"""
        return

















   

