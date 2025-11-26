import tkinter as tk
from tkinter import ttk


class Pestanas:

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

        # Contenido de las pestañas
        tk.Label(self.frame_inicio, text="Sistema de gestion de tráfico ferroviario EFE Chile",
                 bg="#f5f2f4", font=("Arial", 14)).pack(padx=50, pady=50)
        tk.Label(self.frame_config, text="Gestion de trenes:", font=("Arial", 12)).pack(side=tk.TOP)
        tk.Label(self.frame_simulacion, text="Hora:", font=("Arial", 10)).pack(side=tk.TOP)
        # Canvas para dibujar estaciones y trenes
        self.canvas = tk.Canvas(self.frame_simulacion, width=640, height=240, bg="#ffffff")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # Dibujar elementos estáticos
        self._draw_static_elements()

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
        index = self.notebook.index(self.notebook.select())
        if index == 0:
            self.frame_botones.pack(side=tk.BOTTOM, pady=10, padx=10)
        else:
            self.frame_botones.pack_forget()

    # Métodos públicos para compatibilidad
    def select(self, index):
        return self.notebook.select(index)

    def get_notebook(self):
        return self.notebook

    # métodos extra opcionales sin comportamiento por defecto
    def start(self):
        """Compat API placeholder: no-op (compatibilidad)"""
        return

    def stop(self):
        """Compat API placeholder: no-op (compatibilidad)"""
        return

    def set_status(self, text: str):
        """Compat API placeholder: set a status (no-op for now)."""
        return

    # funcion para dibujar en la pestaña
    def _draw_static_elements(self):
        c = self.canvas
        # limpiar
        c.delete('all')

        # Definir posiciones de estaciones
        canvas_w = int(c['width']) if 'width' in c.keys() else 640
        canvas_h = int(c['height']) if 'height' in c.keys() else 240
        rect_w = 120
        rect_h = 50
        
        center_x = (canvas_w - rect_w) / 2
        center_y = (canvas_h - rect_h) / 2

        spacing_v = 20
        spacing_h = 40
        x_santiago = center_x
        y_santiago = center_y
        x_rancagua = center_x
        y_rancagua = y_santiago - rect_h - spacing_v
        x_chillan = center_x
        y_chillan = y_santiago + rect_h + spacing_v
        x_talca = center_x + rect_w + spacing_h
        y_talca = center_y

        stations = [
            (x_santiago, y_santiago, 'Santiago'),
            (x_rancagua, y_rancagua, 'Rancagua'),
            (x_chillan, y_chillan, 'Chillán'),
            (x_talca, y_talca, 'Talca'),
        ]
        # Dibujar bloques para laas estaciones y trenes
        for x, y, name in stations:
            # draw rectangle block
            c.create_rectangle(x, y, x + rect_w, y + rect_h, fill='#a3d3ff', outline='#1f75fe')
            # draw label centered inside the block
            c.create_text(x + rect_w / 2, y + rect_h / 2, text=name, font=('Arial', 10, 'bold'), fill='#000000')

        train_x1 = 10
        train_width = 60
        train_height = 20
        train_spacing = 8
        # BMU 
        bmuy = 10
        c.create_rectangle(train_x1, bmuy, train_x1 + train_width, bmuy + train_height, fill='#ffc1a3', outline='#ff7f50')
        c.create_text(train_x1 + train_width / 2, bmuy + train_height / 2, text='BMU', font=('Arial', 9, 'bold'))
        # EMU
        emuy = bmuy + train_height + train_spacing
        c.create_rectangle(train_x1, emuy, train_x1 + train_width, emuy + train_height, fill='#ffc1a3', outline='#ff7f50')
        c.create_text(train_x1 + train_width / 2, emuy + train_height / 2, text='EMU', font=('Arial', 9, 'bold'))

















   

