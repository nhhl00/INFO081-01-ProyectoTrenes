import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import COLOR_TRENES, BORDE_TRENES
from models import Estacion, Tren, Vias
from logic import horaActual
import datetime as dt
from logic.eventos import GestorEventos, Evento

trenes = [
    Tren("BMU", "T01", 236, 160, ["Santiago", "Rancagua","Santiago","Chillán"], "Santiago", 4),
    Tren("EMU", "T02", 250, 120, ["Talca", "Chillán","Talca","Rancagua"], "Talca", 8)
]


class Pestañas:
    #parametros clase pestañas
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

        #integrar reloj a pestañas
        self.reloj = horaActual()
        # estados para manejo del after() del reloj
        self._reloj_running = False
        self._reloj_after_id = None
        self.crear_ui_reloj()

        # Titulos de las pestañas
        tk.Label(self.frame_inicio, text="Sistema de gestion de tráfico ferroviario EFE Chile",
                 bg="#f5f2f4", font=("Arial", 14)).pack(padx=50, pady=50)
        tk.Label(self.frame_config, text="Gestion de trenes:", font=("Arial", 12)).pack(side=tk.TOP)
        # Canvas para dibujar estaciones y trenes en frame_simulacion
        self.canvas = tk.Canvas(self.frame_simulacion, width=640, height=240, bg="#ffffff")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #llamar a panel de estaciones
        self.panel_estaciones()
        #llamar a panel de trenes
        self.panel_trenes()
        #llamar a las estaciones base
        self.iniciar_estaciones_base()
        #llamar a los trenes base
        self.iniciar_trenes_base()
        #llamar a panel vias
        self.panel_vias()
        #llamar a las vias base
        self.iniciar_vias_base()
        # Gestor de eventos: controla movimientos programados de trenes
        try:
            self.gestor_eventos = GestorEventos()
            # Agendar movimientos iniciales para los trenes que tengan destino
            for tren in getattr(self, 'trenes_list', []):
                try:
                    origen = getattr(tren, 'estacion_actual', None)
                    prox = tren.proximo_destino()
                    if origen and prox:
                        via = self.gestor_eventos._encontrar_via(self.vias_base, origen, prox)
                        if via:
                            # Para pruebas rápidas fijamos el primer evento a las 07:02
                            try:
                                fecha = self.reloj.fecha_hora.date()
                                nuevo_tiempo = dt.datetime.combine(fecha, dt.time(7, 2, 0))
                                # si ya pasó esa hora hoy, dejarlo 1 minuto adelante
                                if nuevo_tiempo <= self.reloj.fecha_hora:
                                    nuevo_tiempo = self.reloj.fecha_hora + dt.timedelta(minutes=1)
                            except Exception:
                                # fallback al cálculo por defecto si algo falla
                                velocidad = getattr(tren, 'velocidad_constante', 60) or 60
                                horas = via.longitud / velocidad
                                segundos = int(horas * 3600)
                                if segundos <= 0:
                                    segundos = 1
                                nuevo_tiempo = self.reloj.fecha_hora + dt.timedelta(seconds=segundos)
                            ev = Evento(nuevo_tiempo, 'mover_tren', {'id_tren': tren.id_tren})
                            self.gestor_eventos.agendar(ev)
                except Exception:
                    pass
                # Agendar evento de retorno a Santiago a las 07:05 para el primer tren (prueba)
                try:
                    if self.trenes_list:
                        tren0 = self.trenes_list[0]
                        fecha = self.reloj.fecha_hora.date()
                        retorno_tiempo = dt.datetime.combine(fecha, dt.time(7, 5, 0))
                        if retorno_tiempo <= self.reloj.fecha_hora:
                            retorno_tiempo = self.reloj.fecha_hora + dt.timedelta(minutes=1)
                        ev2 = Evento(retorno_tiempo, 'forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Santiago'})
                        self.gestor_eventos.agendar(ev2)
                        # Si por alguna razón hay duplicados, eliminar el último para que quede uno solo
                        try:
                            self.gestor_eventos.eliminar_ultimo_duplicado('forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Santiago'})
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            self.gestor_eventos = None
        #llamar a dibujar elementos paara inicializar datos y dibujar elementos estáticos
        self.dibujar_elementos()

        # movement controller removed — no MovimientoDeTrenes integration

        # Añadir pestañas
        self.notebook.add(self.frame_inicio, text="Inicio")
        self.notebook.add(self.frame_config, text="Configuracion")
        self.notebook.add(self.frame_simulacion, text="Simulacion")

        #mantener índice de pestaña simulación
        self.sim_indice = 2

        #Bind al cambio de pestaña para mostrar/ocultar botones (vincular cambio de pestañas a ocultmiento de botones)
        self.notebook.bind('<<NotebookTabChanged>>', self.cambio_de_pestañas)
        self.cambio_de_pestañas()
    #panel para estaciones y trenes
    def panel_estaciones(self):
        #frame para estaciones
        self.frame_info_estaciones = ttk.LabelFrame(self.frame_simulacion, text="Estaciones")
        self.frame_info_estaciones.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        #lista de estaciones
        self.lista_estaciones = tk.Listbox(self.frame_info_estaciones, height=10, width=20)
        self.lista_estaciones.pack(padx=5, pady=5, fill=tk.X)
        #bind (click en estacion) asignando la funcion
        self.lista_estaciones.bind('<<ListboxSelect>>', self.estacion_seleccionada)
        
        #informacion de las estaciones
        self.frame_info_para_labels = ttk.Frame(self.frame_info_estaciones)
        self.frame_info_para_labels.pack(padx=5, pady=5, fill=tk.X)
        
        self.label_nombre = ttk.Label(self.frame_info_para_labels, text="Estacion: ")
        self.label_nombre.pack(anchor=tk.W)
        self.label_estado = ttk.Label(self.frame_info_para_labels, text="Estado: ")
        self.label_estado.pack(anchor=tk.W)
        self.label_trenes = ttk.Label(self.frame_info_para_labels, text="Trenes: ")
        self.label_trenes.pack(anchor=tk.W)
        self.label_poblacion = ttk.Label(self.frame_info_para_labels, text="Población: ")
        self.label_poblacion.pack(anchor=tk.W)


    def panel_trenes(self):
        #Frame para trenes
        self.frame_info_trenes = ttk.LabelFrame(self.frame_simulacion, text="Trenes")
        self.frame_info_trenes.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        # Listbox de trenes
        self.lista_trenes = tk.Listbox(self.frame_info_trenes, height=8, width=24)
        self.lista_trenes.pack(padx=5, pady=5, fill=tk.X)
        self.lista_trenes.bind('<<ListboxSelect>>', self.tren_seleccionado)

        # Frame con labels para información del tren seleccionado
        self.frame_info_tren_labels = ttk.Frame(self.frame_info_trenes)
        self.frame_info_tren_labels.pack(padx=5, pady=5, fill=tk.X)

        self.label_tren_nombre = ttk.Label(self.frame_info_tren_labels, text="Tren: ")
        self.label_tren_nombre.pack(anchor=tk.W)
        self.label_tren_id = ttk.Label(self.frame_info_tren_labels, text="ID: ")
        self.label_tren_id.pack(anchor=tk.W)
        self.label_tren_cap = ttk.Label(self.frame_info_tren_labels, text="Capacidad: ")
        self.label_tren_cap.pack(anchor=tk.W)
        self.label_tren_vel = ttk.Label(self.frame_info_tren_labels, text="Velocidad: ")
        self.label_tren_vel.pack(anchor=tk.W)
        self.label_tren_estado = ttk.Label(self.frame_info_tren_labels, text="Estado: ")
        self.label_tren_estado.pack(anchor=tk.W)
        self.label_tren_ruta = ttk.Label(self.frame_info_tren_labels, text="Ruta: ")
        self.label_tren_ruta.pack(anchor=tk.W)

        try:
            # Instanciar gestor de eventos y agendar dos eventos explícitos para pruebas:
            # 1) mover primer tren a Rancagua a las 07:02
            # 2) forzar retorno a Santiago a las 07:05
            self.gestor_eventos = GestorEventos()
            try:
                if getattr(self, 'trenes_list', None) and len(self.trenes_list) > 0:
                    tren0 = self.trenes_list[0]
                    fecha = self.reloj.fecha_hora.date()
                    # evento 07:02 -> Rancagua
                    tiempo1 = dt.datetime.combine(fecha, dt.time(7, 2, 0))
                    if tiempo1 <= self.reloj.fecha_hora:
                        tiempo1 = self.reloj.fecha_hora + dt.timedelta(minutes=1)
                    ev1 = Evento(tiempo1, 'forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Rancagua'})
                    self.gestor_eventos.agendar(ev1)
                    # evento 07:05 -> Santiago
                    tiempo2 = dt.datetime.combine(fecha, dt.time(7, 5, 0))
                    if tiempo2 <= self.reloj.fecha_hora:
                        tiempo2 = self.reloj.fecha_hora + dt.timedelta(minutes=2)
                    ev2 = Evento(tiempo2, 'forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Santiago'})
                    self.gestor_eventos.agendar(ev2)
                    # eliminar duplicados si llegaron a existir
                    try:
                        self.gestor_eventos.eliminar_ultimo_duplicado('forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Rancagua'})
                        self.gestor_eventos.eliminar_ultimo_duplicado('forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Santiago'})
                    except Exception:
                        pass
            except Exception:
                pass
        except Exception:
            self.gestor_eventos = None

    def panel_vias(self):
        # Panel para mostrar vías y sus detalles
        self.frame_info_vias = ttk.LabelFrame(self.frame_simulacion, text="Vías")
        self.frame_info_vias.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Listbox con las vías
        self.lista_vias = tk.Listbox(self.frame_info_vias, height=10, width=30)
        self.lista_vias.pack(padx=5, pady=5, fill=tk.X)
        self.lista_vias.bind('<<ListboxSelect>>', self.via_seleccionada)

        # Frame con labels de información de la vía seleccionada
        self.frame_info_via_labels = ttk.Frame(self.frame_info_vias)
        self.frame_info_via_labels.pack(padx=5, pady=5, fill=tk.X)

        self.label_via_id = ttk.Label(self.frame_info_via_labels, text="Vía: ")
        self.label_via_id.pack(anchor=tk.W)
        self.label_via_estaciones = ttk.Label(self.frame_info_via_labels, text="Conecta: ")
        self.label_via_estaciones.pack(anchor=tk.W)
        self.label_via_longitud = ttk.Label(self.frame_info_via_labels, text="Longitud: ")
        self.label_via_longitud.pack(anchor=tk.W)
        self.label_via_estado = ttk.Label(self.frame_info_via_labels, text="Estado: ")
        self.label_via_estado.pack(anchor=tk.W)
        self.label_via_tipo = ttk.Label(self.frame_info_via_labels, text="Tipo: ")
        self.label_via_tipo.pack(anchor=tk.W)

    #inicia la simulacion con las estaciones base
    def iniciar_estaciones_base(self):
            self.estaciones_base = {
                "Santiago": Estacion("Santiago", "STG", 8242459, 1),
                "Rancagua": Estacion("Rancagua", "RAN", 274407, 1),
                "Talca": Estacion("Talca", "TAL" , 242344, 1),
                "Chillán": Estacion("Chillán", "CHL" , 204091, 1),
            }

    def iniciar_vias_base(self):
        # conectaar nombres de estaciones para que coincidan con claves de self.estaciones_base
        self.vias_base = [
            Vias("V01", 87, "Santiago", "Rancagua", False, None),  # 87km
            Vias("V02", 400, "Santiago", "Chillán", False, None),  # 400km
            # Vías en L para conectar Chillán - Talca: derecha luego arriba
            Vias("V03", 120, "Chillán", "chillan_talca_mitad", False, None), #180km en total
            Vias("V04", 60, "chillan_talca_mitad", "Talca", False, None),
            # Vías en L para conectar Rancagua - Talca: derecha luego abajo
            Vias("V05", 80, "Rancagua", "rancagua_talca_mitad", False, None), #200km en total
            Vias("V06", 120, "rancagua_talca_mitad", "Talca", False, None),
        ]
        # lista para guardar vias mostradas en canvas
        self.vias_mostradas = []
        # lista actual mostrada en listbox para dibujar indices a vias
        self.current_vias_list = list(self.vias_base)
    
    def dibujar_vias_por_estacion(self, nombre_estacion):
        #Al presionar la estacion muestra las vias correspondientes
        c = self.canvas
        # Limpiar vías anteriores
        self.limpiar_vias()
        
        if nombre_estacion is None:
            return
        # Encontrar todas las vías conectadas a esta estación
        vias_conectadas = []
        for via in self.vias_base:
            if via.conexion_estacion_a == nombre_estacion or via.conexion_estacion_b == nombre_estacion:
                vias_conectadas.append(via)
         #dibujar cada vía conectada
        for via in vias_conectadas:
            estacion_a = via.conexion_estacion_a
            estacion_b = via.conexion_estacion_b
            if estacion_a in self._posiciones and estacion_b in self._posiciones:
                x1, y1 = self._posiciones[estacion_a]
                x2, y2 = self._posiciones[estacion_b]
                # Ajustar coordenadas al centro de los rectángulos
                x1_centro = x1 + self._rect_w / 2
                y1_centro = y1 + self._rect_h / 2
                x2_centro = x2 + self._rect_w / 2
                y2_centro = y2 + self._rect_h / 2

                if via.estado == "ocupada":
                    color_via = "#ff0000"  # Rojo para vías ocupadas
                    grosor_via = 4
                else:
                    color_via = "#666666"  # Gris para vías normales
                    grosor_via = 2

                # Añadir tag común 'via_line' para poder limpiar y gestionar todas las vías
                linea = c.create_line(x1_centro, y1_centro, x2_centro, y2_centro, 
                                    fill=color_via, width=grosor_via, 
                                    tags=(f"via_line", f"via_{via.id_via}"))
                # bind onclick para la vía
                try:
                    c.tag_bind(f"via_{via.id_via}", '<Button-1>', self.via_seleccionada)
                except Exception:
                    pass
                
                self.vias_mostradas.append(via.id_via)

    def limpiar_vias(self):
        #borrr vias
        c = self.canvas
        # Eliminar todas las líneas de vías y sus etiquetas
        # Eliminar todas las líneas de vías usando el tag común 'via_line'
        for item in c.find_withtag('via_line'):
            c.delete(item)
        for item in c.find_withtag("etiqueta_via"):
            c.delete(item)
        self.vias_mostradas = []

    def dibujar_todas_las_vias(self):
        #dibujar TODAS las vias cuando se seleccione una estacion en color gris, rojas si ocupadas por tren
        c = self.canvas
        self.limpiar_vias()
        
        for via in self.vias_base:
            estacion_a = via.conexion_estacion_a
            estacion_b = via.conexion_estacion_b
            
            if estacion_a in self._posiciones and estacion_b in self._posiciones:
                x1, y1 = self._posiciones[estacion_a]
                x2, y2 = self._posiciones[estacion_b]
                
                # Ajustar coordenadas al centro de los rectángulos
                x1_centro = x1 + self._rect_w / 2
                y1_centro = y1 + self._rect_h / 2
                x2_centro = x2 + self._rect_w / 2
                y2_centro = y2 + self._rect_h / 2
                
                # Color más tenue para vías no seleccionadas
                if via.estado == "ocupada":
                    color_via = "#ff6666"  # Rojo para ocupadas
                else:
                    color_via = "#cccccc"  # Gris para no seleccionadas pero visibles
                grosor_via = 2
                # Dibujar la línea de la vía
                linea = c.create_line(x1_centro, y1_centro, x2_centro, y2_centro, 
                                    fill=color_via, width=grosor_via, 
                                    tags=(f"via_line", f"via_{via.id_via}"))
                try:
                    c.tag_bind(f"via_{via.id_via}", '<Button-1>', self.via_seleccionada)
                except Exception:
                    pass
                self.vias_mostradas.append(via.id_via)

    #funcion para dibujar estaciones en las coordenadas
    def dibujar_estaciones(self):
        c = self.canvas
        # Borrar todo y redibujar estaciones
        c.delete("all")

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
            'Talca': (centro_x + rect_w + espacio_horizontal, centro_y),
            #crear vías en L (no son estaciones reales)
            'chillan_talca_mitad': (centro_x + rect_w + espacio_horizontal/2, centro_y + rect_h + espacio_vertical),
            'rancagua_talca_mitad': (centro_x + rect_w + espacio_horizontal/2, centro_y - rect_h - espacio_vertical)
        }

        # Guardar posiciones y tamaños para uso propio(en las vias)
        self._posiciones = posiciones
        self._rect_w = rect_w
        self._rect_h = rect_h

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
        # actualizar lista de trenes si existen
        try:
            self.actualizar_lista_trenes()
        except Exception:
            pass
    #actualizar lista de estaciones en caso de borrarse o añadir
    def actualizar_lista_estaciones(self):
        self.lista_estaciones.delete(0, tk.END)
        for nombre, estacion in self.estaciones_base.items():
            self.lista_estaciones.insert(tk.END, f"{estacion.nombre}")
    #al hacer click en una estacion mostrar su informacion y resaltarla
    def estacion_seleccionada(self, event):
        seleccion = self.lista_estaciones.curselection()
        if seleccion:
            indice = seleccion[0]
            nombre_estacion = list(self.estaciones_base.keys())[indice]
            self.estacion_seleccionada_actual = nombre_estacion
            estacion = self.estaciones_base[nombre_estacion]
            self.mostrar_informacion_estacion(estacion)
            self.resaltar_estacion(nombre_estacion)
            # mostrar solo las vías conectadas a esta estación
            self.dibujar_vias_por_estacion(nombre_estacion)
            # Actualizar lista de vías en el panel por estacion
            self.actualizar_lista_vias_por_estacion(nombre_estacion)
        else:
            # si no hay selección, mostrar todas las vias grises
            self.estacion_seleccionada_actual = None
            self.dibujar_todas_las_vias()
            self.actualizar_lista_vias_todas()

    def actualizar_lista_vias_por_estacion(self, nombre_estacion):
        #actualizar la lista de vias por estacion seleccionada
        if hasattr(self, "lista_vias"):
            self.lista_vias.delete(0, tk.END)
            
            vias_conectadas = []
            for via in self.vias_base:
                if via.conexion_estacion_a == nombre_estacion or via.conexion_estacion_b == nombre_estacion:
                    vias_conectadas.append(via)
            # Guardar la lista actual mostrada para mapping de selección
            self.current_vias_list = vias_conectadas
            for via in vias_conectadas:
                estado = "Libre" if via.estado == "desocupada" else "Ocupada"
                otra_estacion = via.conexion_estacion_b if via.conexion_estacion_a == nombre_estacion else via.conexion_estacion_a
                self.lista_vias.insert(tk.END, f"{via.id_via} → {otra_estacion} | {estado} | {via.longitud} km")

    def actualizar_lista_vias_todas(self):
        #actualizar la lista de vias
        if hasattr(self, 'lista_vias'):
            self.lista_vias.delete(0, tk.END)
            # Mostrar una única línea por vía y guardar la lista actual
            self.current_vias_list = list(self.vias_base)
            for via in self.vias_base:
                estado = "Libre" if via.estado == "desocupada" else "Ocupada"
                self.lista_vias.insert(tk.END, f"{via.id_via}: {via.conexion_estacion_a}-{via.conexion_estacion_b} | {estado} | {via.longitud}km")

    def dibujar_elementos(self):
        #dibujar todos los elementos de la interfaz
        c = self.canvas
        
        # Dibujar estaciones primero
        try:
            self.dibujar_estaciones()
        except Exception as error:
            print(f"Error dibujando estaciones: {error}")
        
        # Dibujar todas las vías inicialmente (tenues)
        try:
            self.dibujar_todas_las_vias()
        except Exception as error:
            print(f"Error dibujando vías: {error}")
        
        # Dibujar trenes
        try:
            if not hasattr(self, 'trenes_list'):
                self.iniciar_trenes_base()
            self.dibujar_trenes()
            self.actualizar_lista_trenes()
        except Exception as error:
            print(f"Error dibujando trenes: {error}")
        
        # Actualizar lista de vías
        self.actualizar_lista_vias_todas()

    def via_seleccionada(self, event):
        #Manejar seleccion de vias
        # Detectar si la selección proviene del Listbox o del Canvas
        widget = getattr(event, 'widget', None)
        if widget == getattr(self, 'lista_vias', None):
            seleccion = self.lista_vias.curselection()
            if not seleccion:
                return
            indice = seleccion[0]
            # usar la lista actual mostrada para obtener el objeto via
            vias_mostradas = getattr(self, 'current_vias_list', None)
            if vias_mostradas is None:
                vias_mostradas = getattr(self, 'vias_base', [])
            if 0 <= indice < len(vias_mostradas):
                via = vias_mostradas[indice]
                self.mostrar_informacion_via(via)
                self.resaltar_via(via.id_via)
            return
        # Si no es el Listbox asumir que es un click en el canvas
        try:
            c = self.canvas
            item = c.find_closest(event.x, event.y)
            tags = c.gettags(item)
            via_id = None
            for t in tags:
                if isinstance(t, str) and t.startswith('via_'):
                    via_id = t.split('_', 1)[1]
                    break
            if not via_id:
                return
            via = next((v for v in getattr(self, 'vias_base', []) if v.id_via == via_id), None)
            if via:
                self.mostrar_informacion_via(via)
                self.resaltar_via(via.id_via)
            return
        except Exception:
            pass

    def mostrar_informacion_estacion(self, estacion):
        nombre = getattr(estacion, 'nombre', 'Desconocida')
        estado = getattr(estacion, 'estado', 'Desconocido')
        trenes_esperando = len(getattr(estacion, 'trenes_esperando', []))
        capacidad_trenes = getattr(estacion, 'capacidad_de_trenes', 'N/A')
        poblacion = getattr(estacion, 'poblacion', 'N/D')

        self.label_nombre.config(text=f"Estación: {nombre}")
        self.label_estado.config(text=f"Estado: {estado}")
        # Mostrar trenes como: número esperandos / capacidad si disponible
        self.label_trenes.config(text=f"Trenes: {trenes_esperando}/{capacidad_trenes}")
        self.label_poblacion.config(text=f"Población: {poblacion}")

    def mostrar_informacion_via(self, via):
        if not via:
            return
        try:
            self.label_via_id.config(text=f"Vía: {via.id_via}")
            self.label_via_estaciones.config(text=f"Conecta: {via.conexion_estacion_a} - {via.conexion_estacion_b}")
            self.label_via_longitud.config(text=f"Longitud: {via.longitud} km")
            estado = "Libre" if getattr(via, 'estado', 'desocupada') == 'desocupada' else "Ocupada"
            self.label_via_estado.config(text=f"Estado: {estado}")
            tipo = "Rotatoria" if getattr(via, 'via_rotatoria', False) else "Normal"
            self.label_via_tipo.config(text=f"Tipo: {tipo}")
        except Exception:
            pass

    def resaltar_via(self, via_id):
        c = self.canvas
        # resetear todas las vías a su color base
        try:
            for item in c.find_withtag('via_line'):
                # Encontrar a qué via pertenece por tags
                tags = c.gettags(item)
                cur_via_id = None
                for t in tags:
                    if isinstance(t, str) and t.startswith('via_') and t != 'via_line':
                        cur_via_id = t.split('_', 1)[1]
                        break
                # Obterner estado del objeto via para pintar acorde
                via_obj = next((v for v in getattr(self, 'vias_base', []) if v.id_via == cur_via_id), None)
                if via_obj and via_obj.estado == 'ocupada':
                    c.itemconfig(item, fill='#ff6666', width=4)
                else:
                    c.itemconfig(item, fill='#cccccc', width=2)
        except Exception:
            pass
        # Ahora resaltar la seleccionada en verde oscuro
        try:
            if via_id is None:
                return
            for item in c.find_withtag(f'via_{via_id}'):
                c.itemconfig(item, fill='#00aa00', width=4)
        except Exception:
            pass

    #al cambiar pestañas se ocultn los botones
    def cambio_de_pestañas(self, event=None):
        indice = self.notebook.index(self.notebook.select())
        if indice == 0:
            self.frame_botones.pack(side=tk.BOTTOM, pady=10, padx=10)
        else:
            self.frame_botones.pack_forget()

    # Métodos para compatibilidad
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

    def dibujar_elementos(self):
        #dibujar elementos en la interfaz
        c = self.canvas
        # Dibujar estaciones primero
        try:
            self.dibujar_estaciones()
        except Exception:
            pass

        # Dibujar trenes (representación simple en columna izquierda)
        try:
            # Asegurar que la lista de trenes esté inicializada
            if not hasattr(self, 'trenes_list'):
                self.iniciar_trenes_base()
            self.dibujar_trenes()
            # Actualizar listbox de trenes
            self.actualizar_lista_trenes()
        except Exception:
            pass

    #iniciar la simulacion con los trenes bsae (BMU-EMU)
    def iniciar_trenes_base(self):
        # Inicializar lista de trenes si no existe un sistema
        try:
            self.trenes_list = list(self.sistema.trenes) if self.sistema and hasattr(self.sistema, "trenes") else list(trenes)
        except:
            self.trenes_list = list(trenes)
        self.train_items = {}
        self._route_items = []  # guardar items dibujados para rutas (líneas sobre canvas)
    # actualizar lista de trenes en caso de borrar o añadir
    def actualizar_lista_trenes(self):
        # Actualiza la listbox de trenes en el panel derecho
        try:
            self.lista_trenes.delete(0, tk.END)
            for tren in self.trenes_list:
                nombre = getattr(tren, 'nombre_tren', str(tren))
                self.lista_trenes.insert(tk.END, nombre)
        except Exception:
            pass
    #dibujar los trenes en sus coordenadas
    def dibujar_trenes(self):
        c = self.canvas
        # Dibujar rectangulos que represtnan a los trenes
        x = 10
        y = 80
        ancho = 60
        alto = 20
        espacio = 10
        # limpiar items previos de tren por si acaso
        if hasattr(self, '_train_items'):
            for item in self.train_items.values():
                try:
                    c.delete(item)
                except Exception:
                    pass
        self.train_items = {}
        for tren in self.trenes_list:
            nombre = getattr(tren, 'nombre_tren', 'Tren')
            tag = f'tren_{nombre}'
            # Si el tren tiene estacion_actual conocida, dibujarlo cerca de esa estación
            if getattr(tren, 'estacion_actual', None) and getattr(self, '_posiciones', None) and tren.estacion_actual in self._posiciones:
                sx, sy = self._posiciones[tren.estacion_actual]
                # Ajuste para dibujar a la derecha del rectángulo de estación
                rect_x = sx + self._rect_w + 10
                rect_y = sy + 5
                rect = c.create_rectangle(rect_x, rect_y, rect_x + ancho, rect_y + alto, fill=COLOR_TRENES, outline=BORDE_TRENES, tags=(tag,))
                txt = c.create_text(rect_x + ancho / 2, rect_y + alto / 2, text=nombre, font=('Arial', 9, 'bold'), tags=(tag,))
            else:
                rect = c.create_rectangle(x, y, x + ancho, y + alto, fill=COLOR_TRENES, outline=BORDE_TRENES, tags=(tag,))
                txt = c.create_text(x + ancho / 2, y + alto / 2, text=nombre, font=('Arial', 9, 'bold'), tags=(tag,))
            self.train_items[nombre] = (rect, txt)
            y += alto + espacio
    #al hacer click mostrar laa informcaion del tren resaltarlo
    def tren_seleccionado(self, event):
        seleccionado = self.lista_trenes.curselection()
        if not seleccionado:
            return
        indice = seleccionado[0]
        try:
            tren = self.trenes_list[indice]
        except Exception:
            return
        nombre = getattr(tren, 'nombre_tren', str(tren))
        # actualizar labels de información con datos
        self.label_tren_nombre.config(text=f"Tren: {nombre}")
        self.label_tren_id.config(text=f"ID: {getattr(tren, 'id_tren', 'N/A')}")
        self.label_tren_cap.config(text=f"Capacidad: {getattr(tren, 'capacidad', 'N/A')}")
        self.label_tren_vel.config(text=f"Velocidad: {getattr(tren, 'velocidad_constante', 'N/A')}")
        self.label_tren_estado.config(text=f"Estado: {getattr(tren, 'estado', 'N/A')}")
        # Mostrar ruta en el label
        ruta = getattr(tren, 'ruta', [])
        try:
            self.label_tren_ruta.config(text=f"Ruta: {' -> '.join(ruta)}")
        except Exception:
            self.label_tren_ruta.config(text=f"Ruta: {ruta}")
        # resaltar en canvas
        self.resaltar_tren(nombre)
        # Mostrar ruta del tren en el canvas
        self.mostrar_ruta_tren(tren)

    def mostrar_eventos_dialog(self):
        """Muestra la cola de eventos en un diálogo modal para depuración."""
        try:
            print('[DEBUG] mostrar_eventos_dialog llamado')
            eventos = []
            # preferir el gestor de eventos de la propia pestaña
            if getattr(self, 'gestor_eventos', None) is not None:
                print('[DEBUG] usando self.gestor_eventos')
                eventos = self.gestor_eventos.listar_eventos()
            # si existe un sistema externo con estado, usarlo
            elif getattr(self, 'sistema', None) is not None and hasattr(self.sistema, 'gestor_eventos'):
                print('[DEBUG] usando sistema.gestor_eventos')
                eventos = self.sistema.gestor_eventos.listar_eventos()

            print(f'[DEBUG] eventos obtenidos: {type(eventos)} len={len(eventos) if hasattr(eventos, "__len__") else "?"}')

            if not eventos:
                messagebox.showinfo("Eventos", "No hay eventos programados.")
                return
            # Normalizar distintos formatos posibles de 'eventos'
            # Vamos a mostrar los eventos en un Listbox con botones para eliminar
            # Normalizar la colección de eventos a una lista de objetos/dicts
            if isinstance(eventos, dict):
                eventos = [eventos]
            if not isinstance(eventos, (list, tuple)) and hasattr(eventos, 'listar_eventos'):
                try:
                    eventos = eventos.listar_eventos()
                except Exception:
                    eventos = list(eventos)
            try:
                iterator = iter(eventos)
            except TypeError:
                eventos = [eventos]

            # Crear ventana y listbox
            top = tk.Toplevel(self.parent)
            top.title("Cola de eventos")
            top.geometry('600x320')

            frame_list = ttk.Frame(top)
            frame_list.pack(fill=tk.BOTH, expand=True)

            lb = tk.Listbox(frame_list, selectmode=tk.SINGLE)
            lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=lb.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            lb.config(yscrollcommand=scrollbar.set)

            # Mapear índices a event ids
            idx_to_id = []
            for e in eventos:
                try:
                    if hasattr(e, 'tiempo') or hasattr(e, 'tipo'):
                        tiempo = getattr(e, 'tiempo', None)
                        tipo = getattr(e, 'tipo', '')
                        datos = getattr(e, 'datos', {})
                        id_ev = getattr(e, 'id', '')
                    elif isinstance(e, dict):
                        tiempo = e.get('tiempo')
                        tipo = e.get('tipo', '')
                        datos = e.get('datos', {})
                        id_ev = e.get('id', '')
                    else:
                        tiempo = ''
                        tipo = ''
                        datos = str(e)
                        id_ev = ''
                    display = f"{tiempo} | {tipo} | {datos} | id={id_ev}"
                except Exception:
                    display = str(e)
                    id_ev = getattr(e, 'id', '') if hasattr(e, 'id') else ''
                lb.insert(tk.END, display)
                idx_to_id.append(id_ev)

            # Botones de acción
            frame_buttons = ttk.Frame(top)
            frame_buttons.pack(fill=tk.X)

            def eliminar_seleccionado():
                sel = lb.curselection()
                if not sel:
                    messagebox.showinfo('Eliminar', 'Seleccione un evento primero.')
                    return
                i = sel[0]
                event_id = idx_to_id[i]
                if not event_id:
                    messagebox.showerror('Eliminar', 'Evento sin id, no se puede eliminar.')
                    return
                gestor = getattr(self, 'gestor_eventos', None) or (getattr(self, 'sistema', None) and getattr(self.sistema, 'gestor_eventos', None))
                if not gestor:
                    messagebox.showerror('Eliminar', 'No hay gestor de eventos disponible.')
                    return
                try:
                    ok = gestor.eliminar_evento_por_id(event_id)
                    if ok:
                        lb.delete(i)
                        idx_to_id.pop(i)
                        messagebox.showinfo('Eliminar', 'Evento eliminado.')
                    else:
                        messagebox.showerror('Eliminar', 'Evento no encontrado.')
                except Exception as ex:
                    messagebox.showerror('Eliminar', f'Error al eliminar: {ex}')

            btn_eliminar = ttk.Button(frame_buttons, text='Eliminar seleccionado', command=eliminar_seleccionado)
            btn_eliminar.pack(side=tk.LEFT, padx=6, pady=6)

            btn_cerrar = ttk.Button(frame_buttons, text='Cerrar', command=top.destroy)
            btn_cerrar.pack(side=tk.RIGHT, padx=6, pady=6)
        except Exception as e:
            import traceback
            traceback.print_exc()
            try:
                messagebox.showerror("Error", f"No se pudo obtener la lista de eventos: {e}")
            except Exception:
                pass

    #funcion para resaltar tren
    def resaltar_tren(self, nombre):
        c = self.canvas
        # resetear outline de todos los trenes
        for tren_info in getattr(self, "_train_items", {}).values():
            rectangulo_id = tren_info[0]
            c.itemconfig(rectangulo_id, outline=BORDE_TRENES, width=2) 
        # resaltar el seleccionado
        if nombre in getattr(self, '_train_items', {}):
            rectangulo_id = self.train_items[nombre][0]
            c.itemconfig(rectangulo_id, outline='#00aa00', width=2)

    #funcion para resaltar estaciones al seleccionarla
    def resaltar_estacion(self, nombre):
        #resaltaa estacion seleccionada
        c = self.canvas
        #resetear resaltamiento
        for n, est in self.estaciones_base.items():
            tag_estacion = f'estacion_{n}'
            c.itemconfig(tag_estacion, outline=est.borde, width=2)
        #resaltar en rojo
        if nombre in self.estaciones_base:
            tag_sel = f'estacion_{nombre}'
            c.itemconfig(tag_sel, outline='#ff0000', width=2)
        # Limpiar cualquier resaltado de rutas previas cuando se selecciona una estación
        self.limpiar_resaltado_ruta()

    def limpiar_resaltado_ruta(self):
        c = self.canvas
        # Borrar líneas de rutas dibujadas previamente
        if hasattr(self, '_route_items') and self._route_items:
            for item in list(self._route_items):
                try:
                    c.delete(item)
                except Exception:
                    pass
            self._route_items = []
        # Resetear outline de todas las estaciones a su color original
        for nombre, est in getattr(self, 'estaciones_base', {}).items():
            try:
                c.itemconfig(f'estacion_{nombre}', outline=est.borde, width=2)
            except Exception:
                pass

    def mostrar_ruta_tren(self, tren):
        #dibuja en el canvas la ruta de los trenes 
        # Limpiar ruta previa
        self.limpiar_resaltado_ruta()
        if not tren:
            return
        ruta = getattr(tren, 'ruta', None)
        if not ruta:
            return
        c = self.canvas
        puntos = []
        for nombre in ruta:
            if nombre in getattr(self, '_posiciones', {}):
                # Resaltar la estación
                try:
                    c.itemconfig(f'estacion_{nombre}', outline='#0000ff', width=3)
                except Exception:
                    pass
                x, y = self._posiciones[nombre]
                # Centro del rectángulo
                x_c = x + self._rect_w / 2
                y_c = y + self._rect_h / 2
                puntos.append((x_c, y_c))
        # Dibujar líneas entre puntos consecutivos
        for a, b in zip(puntos, puntos[1:]):
                line = c.create_line(a[0], a[1], b[0], b[1], fill='#0000ff', width=3, tags=(f'ruta_{getattr(tren, "id_tren", "")}'))
                # Guardar para poder borrar luego
                self._route_items.append(line)

    #funcion para crear el ui del reloj 
    def crear_ui_reloj(self):
        frame_reloj = ttk.Frame(self.frame_simulacion)
        frame_reloj.pack(pady=10)

        # Label principal del reloj
        self.label_reloj = ttk.Label(frame_reloj, text="", font=('Arial', 8))
        self.label_reloj.pack()

        # Botón para ver la cola de eventos (está dentro de la pestaña Simulación)
        try:
            boton_eventos_local = ttk.Button(frame_reloj, text="Ver eventos", command=self.mostrar_eventos_dialog)
            boton_eventos_local.pack(padx=4, pady=2)
        except Exception:
            pass
        # Mostrar la hora inicial
        self.actualizar_ui_reloj()
    #funcion para actualizar la ui del reloj junto a los ticks
    def actualizar_ui_reloj(self):
        #acuatliza la ui del rejol continumamente
        try:
            hora = self.reloj.obtener_hora()
        except Exception:
            hora = str(self.reloj)
        self.label_reloj.config(text=f"Hora: {hora}")

    def reloj_tick_por_segundo(self):
        # avanzar segundos y actualizar
        self.reloj.avanzar_segundos(1)
        self.actualizar_ui_reloj()
        # Procesar eventos programados hasta la hora actual (movimientos de trenes)
        try:
            if getattr(self, 'gestor_eventos', None) is not None:
                procesados = self.gestor_eventos.procesar_hasta(self.reloj.fecha_hora, self.estaciones_base, self.vias_base, self.trenes_list)
                if procesados:
                    # Redibujar para reflejar cambios de posición
                    try:
                        self.dibujar_estaciones()
                        self.dibujar_trenes()
                        self.actualizar_lista_trenes()
                    except Exception:
                        pass
        except Exception:
            pass
        # reprogramar si está corriendo
        if self._reloj_running:
            self._reloj_after_id = self.parent.after(1000, self.reloj_tick_por_segundo)

    def empezar_reloj(self):
        # inicia el avance del reloj 
        if not self._reloj_running:
            self._reloj_running = True
            self._reloj_after_id = self.parent.after(1000, self.reloj_tick_por_segundo)

    def parar_reloj(self):
        # detiene el avance del reloj 
        if self._reloj_running:
            self._reloj_running = False
            if self._reloj_after_id is not None:
                try:
                    self.parent.after_cancel(self._reloj_after_id)
                except Exception:
                    pass
                self._reloj_after_id = None