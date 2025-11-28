import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import COLOR_TRENES, BORDE_TRENES, COLOR_ESTACIONES, BORDE_ESTACIONES
from models import Estacion


class Pestañas:

    def __init__(self, parent, frame_botones, sistema_ferroviario=None):
        self.parent = parent
        self.frame_botones = frame_botones
        self.sistema = sistema_ferroviario

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

        #panel de estaciones
        self.panel_estaciones()
    
        if not self.sistema:
            self.iniciar_estaciones_base()
        # Dibujar elementos estáticos
        self.dibujar_elementos()

        # Añadir pestañas
        self.notebook.add(self.frame_inicio, text="Inicio")
        self.notebook.add(self.frame_config, text="Configuracion")
        self.notebook.add(self.frame_simulacion, text="Simulacion")

        # Opcional: mantener índice de pestaña simulación
        self.sim_index = 2

        # Bind al cambio de pestaña para mostrar/ocultar botones
        self.notebook.bind('<<NotebookTabChanged>>', self.cambio_de_pestañas)
        self.cambio_de_pestañas()

    def panel_estaciones(self):
        self.frame_info_estaciones = ttk.LabelFrame(self.frame_simulacion, text="Estaciones")
        self.frame_info_estaciones.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        #lista estaciones
        self.lista_estaciones = tk.Listbox(self.frame_info_estaciones, height=10, width=20)
        self.lista_estaciones.pack(padx=5,pady=5, fill=tk.X)
        self.lista_estaciones.bind('<<ListboxSelect>>', self.estacion_seleccionada)
        #informacion
        self.frame_info = ttk.Frame(self.frame_info_estaciones)
        self.frame_info.pack(padx=5, pady=5, fill=tk.X)

        self.lbl_nombre = ttk.Label(self.frame_info, text="Estacion: ")
        self.lbl_nombre.pack(anchor=tk.W)
        self.lbl_estado = ttk.Label(self.frame_info, text="Estado: ")
        self.lbl_estado.pack(anchor=tk.W)
        self.lbl_trenes = ttk.Label(self.frame_info, text="Trenes: ")
        self.lbl_trenes.pack(anchor=tk.W)
        self.lbl_poblacion = ttk.Label(self.frame_info, text="Población: ")
        self.lbl_poblacion.pack(anchor=tk.W)

    def iniciar_estaciones_base(self):
            self.estaciones_base = {
                "Santiago": Estacion("Santiago", "STG", 8242459, 1),
                "Rancagua": Estacion("Rancagua", "RAN", 274407, 1),
                "Talca": Estacion("Talca", "TAL" , 242344, 1),
                "Chillán": Estacion("Chillán", "CHL" , 204091, 1),
            }

    def dibujar_estaciones(self):
        c = self.canvas
        c.delete('all')

        canvas_w = int(c['width']) if 'width' in c.keys() else 640
        canvas_h = int(c['height']) if 'height' in c.keys() else 240
        rect_w = 100
        rect_h = 40

        centro_x = (canvas_w - rect_w) / 2
        centro_y = (canvas_h - rect_h) / 2

        espacio_vertical = 40
        espacio_horizontal = 50

        posiciones = {
            'Santiago': (centro_x, centro_y),
            'Rancagua': (centro_x, centro_y - rect_h - espacio_vertical),
            'Chillán': (centro_x, centro_y + rect_h + espacio_vertical),
            'Talca': (centro_x + rect_w + espacio_horizontal, centro_y)
        }

        # Dibujar cada estación
        for nombre, (x, y) in posiciones.items():
            if nombre in self.estaciones_base:
                estacion = self.estaciones_base[nombre]
                
                # Dibujar rectángulo de la estación
                c.create_rectangle(x, y, x + rect_w, y + rect_h, 
                                 fill=estacion.color, outline=estacion.borde, width=2,
                                 tags=f'estacion_{nombre}')
                
                # Nombre de la estación
                c.create_text(x + rect_w/2, y + rect_h/2, 
                            text=estacion.nombre, font=('Arial', 10, 'bold'),
                            tags=f'texto_{nombre}')
                
                # Información de trenes
                info_trenes = f"{len(estacion.trenes_esperando)}/{estacion.capacidad_de_trenes}"
                c.create_text(x + rect_w/2, y + rect_h + 15, 
                            text=info_trenes, font=('Arial', 8),
                            tags=f'info_{nombre}')
                
        self.actualizar_lista_estaciones()
                
    def actualizar_lista_estaciones(self):
            self.lista_estaciones.delete(0, tk.END)
            for nombre, estacion in self.estaciones_base.items():
                self.lista_estaciones.insert(tk.END, f"{estacion.nombre}")

    def estacion_seleccionada(self, event):
            seleccion = self.lista_estaciones.curselection()
            if seleccion:
                indice = seleccion[0]
                nombre_estacion = list(self.estaciones_base.keys())[indice]
                estacion = self.estaciones_base[nombre_estacion]
                self.mostrar_informacion_estacion(estacion)
                self.resaltar_estacion(nombre_estacion)

    def mostrar_informacion_estacion(self, estacion):
        nombre = getattr(estacion, 'nombre', 'Desconocida')
        estado = getattr(estacion, 'estado', 'Desconocido')
        trenes_esperando = len(getattr(estacion, 'trenes_esperando', []))
        capacidad_trenes = getattr(estacion, 'capacidad_de_trenes', 'N/A')
        poblacion = getattr(estacion, 'poblacion', 'N/D')

        self.lbl_nombre.config(text=f"Estación: {nombre}")
        self.lbl_estado.config(text=f"Estado: {estado}")
        # Mostrar trenes como: número esperandos / capacidad si disponible
        self.lbl_trenes.config(text=f"Trenes: {trenes_esperando}/{capacidad_trenes}")
        self.lbl_poblacion.config(text=f"Población: {poblacion}")


    def cambio_de_pestañas(self, event=None):
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
    

    #agregar trenes a las estaciones
    def agregar_tren_a_estacion(self, nombre_estacion, tren):   
        if nombre_estacion in self.estaciones_base:
            estacion = self.estaciones_base[nombre_estacion]
            if estacion.agregar_tren(tren):
                self.dibujar_estaciones()
                return True
        return False
        
         
    #funcion para dibujar en la pestaña
    def dibujar_elementos(self):
        c = self.canvas
        #dibujar estaciones 
        self.dibujar_estaciones()

        posicion_inicial_x_tren = 10
        tren_ancho = 60
        tren_alto = 20
        espacio_entre_trenes = 10
        # BMU 
        bmuy = 10
        c.create_rectangle(posicion_inicial_x_tren, bmuy, posicion_inicial_x_tren + tren_ancho, bmuy + tren_alto, fill=COLOR_TRENES, outline=BORDE_TRENES)
        c.create_text(posicion_inicial_x_tren + tren_ancho / 2, bmuy + tren_alto / 2, text='BMU', font=('Arial', 9, 'bold'))
        # EMU
        emuy = bmuy + tren_alto + espacio_entre_trenes
        c.create_rectangle(posicion_inicial_x_tren, emuy, posicion_inicial_x_tren + tren_ancho, emuy + tren_alto, fill=COLOR_TRENES, outline=BORDE_TRENES)
        c.create_text(posicion_inicial_x_tren + tren_ancho / 2, emuy + tren_alto / 2, text='EMU', font=('Arial', 9, 'bold'))
    
    def resaltar_estacion(self, nombre):
        #resaltaa estacion seleccionada
        c = self.canvas
        #resetear
        for n, est in self.estaciones_base.items():
            tag = f'estacion_{n}'
            try:
                c.itemconfig(tag, outline=est.borde, width=2)
            except Exception:
                pass
        #resaltar en rojo
        if nombre in self.estaciones_base:
            tag_sel = f'estacion_{nombre}'
            try:
                c.itemconfig(tag_sel, outline='#ff0000', width=3)
            except Exception:
                messagebox.showerror("Error! no se pudo resaltar la estacion")