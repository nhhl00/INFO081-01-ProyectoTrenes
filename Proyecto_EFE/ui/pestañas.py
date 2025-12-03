import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from config import COLOR_TRENES, BORDE_TRENES
from models import Estacion, Tren, Vias
from logic import horaActual
from logic.EstadoDeSimulacion import EstadoSimulacion
from logic.SistemaDeGuardado import SistemaGuardado
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

        self.sistema_guardado = SistemaGuardado(directorio="saves")

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
        # contador para generación periódica de pasajeros (en segundos simulados)
        self._seconds_since_last_generation = 0
        self.crear_ui_reloj()

        # Titulos de las pestañas
        tk.Label(self.frame_inicio, text="Sistema de gestion de tráfico ferroviario EFE Chile",
                 bg="#f5f2f4", font=("Arial", 14)).pack(padx=50, pady=50)
        tk.Label(self.frame_config, text="Gestion de trenes:", font=("Arial", 12)).pack(side=tk.TOP)
        # Canvas para dibujar estaciones y trenes en frame_simulacion
        self.canvas = tk.Canvas(self.frame_simulacion, width=640, height=240, bg="#ffffff")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # llamar a panel de estaciones y crear datos base
        self.panel_estaciones()
        self.iniciar_estaciones_base()
        # inicializar vías y trenes base antes de crear el Estado de Simulación
        self.iniciar_vias_base()
        self.iniciar_trenes_base()

        # Crear EstadoSimulacion y sincronizar estructuras compartidas
        
        self.estado_sim = EstadoSimulacion()
        # usar el mismo reloj
        self.estado_sim.hora_actual = self.reloj
        # vincular referencias (usar objetos existentes en UI)
        self.estado_sim.estaciones = self.estaciones_base
        self.estado_sim.vias = self.vias_base
        self.estado_sim.trenes = self.trenes_list
        # construir mapa de rutas para la generación de pasajeros
        self.estado_sim.construir_rutas_para_pasajeros()
        
        # exponer el gestor de eventos para la UI
        self.gestor_eventos = self.estado_sim.gestor_eventos
        

        # paneles que dependen de las listas previas
        self.panel_trenes()
        self.panel_vias()

        # dibujar elementos paara inicializar datos y dibujar elementos estáticos
        self.dibujar_elementos()

        # Añadir pestañas
        self.notebook.add(self.frame_inicio, text="Inicio")
        self.notebook.add(self.frame_config, text="Configuracion")
        self.notebook.add(self.frame_simulacion, text="Simulacion")

        #mantener índice de pestaña simulación
        self.sim_indice = 2

        
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
       
        self.lista_estaciones.bind('<<ListboxSelect>>', self.estacion_seleccionada)
        
        #informacion de las estaciones
        self.frame_info_para_labels = ttk.Frame(self.frame_info_estaciones)
        self.frame_info_para_labels.pack(padx=5, pady=5, fill=tk.X)
        #informacion principal de la estacion
        self.label_nombre = ttk.Label(self.frame_info_para_labels, text="Estacion: ")
        self.label_nombre.pack(anchor=tk.W)
        self.label_estado = ttk.Label(self.frame_info_para_labels, text="Estado: ")
        self.label_estado.pack(anchor=tk.W)
        self.label_trenes = ttk.Label(self.frame_info_para_labels, text="Trenes: ")
        self.label_trenes.pack(anchor=tk.W)
        self.label_poblacion = ttk.Label(self.frame_info_para_labels, text="Población: ")
        self.label_poblacion.pack(anchor=tk.W)
        # Label para mostrar pasajeros en espera en la estación seleccionada
        self.label_pasajeros = ttk.Label(self.frame_info_para_labels, text="Pasajeros en espera: 0")
        self.label_pasajeros.pack(anchor=tk.W)

    #panel para trenes(labels)
    def panel_trenes(self):
        #gestion para trenes
        self.frame_info_trenes = ttk.LabelFrame(self.frame_simulacion, text="Trenes")
        self.frame_info_trenes.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        # Lista de trenes
        self.lista_trenes = tk.Listbox(self.frame_info_trenes, height=8, width=24)
        self.lista_trenes.pack(padx=5, pady=5, fill=tk.X)
        self.lista_trenes.bind('<<ListboxSelect>>', self.tren_seleccionado)

        # gestion para información del tren seleccionado
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
            # Usar el gestor de eventos compartido (creado en EstadoSimulacion)
            # Agendar dos eventos explícitos para pruebas:
            # 1) mover primer tren a Rancagua a las 07:02
            # 2) forzar retorno a Santiago a las 07:05
            # self.gestor_eventos ya debe estar inicializado desde EstadoSimulacion
            try:
                if getattr(self, 'trenes_list', None) and len(self.trenes_list) > 0:
                    tren0 = self.trenes_list[0]
                    fecha = self.reloj.fecha_hora.date()
                    # evento 07:02  Rancagua
                    tiempo1 = dt.datetime.combine(fecha, dt.time(7, 2, 0))
                    if tiempo1 <= self.reloj.fecha_hora:
                        tiempo1 = self.reloj.fecha_hora + dt.timedelta(minutes=1)
                    ev1 = Evento(tiempo1, 'forzar_mover_tren', {'id_tren': tren0.id_tren, 'destino': 'Rancagua'})
                    self.gestor_eventos.agendar(ev1)
                    # evento 07:05  Santiago
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
                    # evento para tren EMU (T02) que viaje a Chillán a las 07:03
                    try:
                        if len(self.trenes_list) > 1:
                            tren1 = self.trenes_list[1]
                            tiempo_emu = dt.datetime.combine(fecha, dt.time(7, 3, 0))
                            if tiempo_emu <= self.reloj.fecha_hora:
                                tiempo_emu = self.reloj.fecha_hora + dt.timedelta(minutes=3)
                            ev_emu = Evento(tiempo_emu, 'forzar_mover_tren', {'id_tren': tren1.id_tren, 'destino': 'Chillán'})
                            self.gestor_eventos.agendar(ev_emu)
                            print(f"Evento EMU agendado: tren={tren1.id_tren}, destino=Chillán, tiempo={tiempo_emu}")
                    except Exception as e:
                        print(f"Error agendando evento EMU: {e}")
                        pass
            except Exception:
                pass
        except Exception:
            self.gestor_eventos = None
    #panel para vias(labels)
    def panel_vias(self):
        # Panel para mostrar vías y sus detalles
        self.frame_info_vias = ttk.LabelFrame(self.frame_simulacion, text="Vías")
        self.frame_info_vias.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Lista con las vías
        self.lista_vias = tk.Listbox(self.frame_info_vias, height=10, width=30)
        self.lista_vias.pack(padx=5, pady=5, fill=tk.X)
        self.lista_vias.bind('<<ListboxSelect>>', self.via_seleccionada)

        # gestion de información de la vía seleccionada
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
                    grosor_via = 2
                else:
                    color_via = "#666666"  # Gris para vías sin seleccionar
                    grosor_via = 2

                # Añadir tag común 'via_line' para poder limpiar y gestionar todas las vías
                linea = c.create_line(x1_centro, y1_centro, x2_centro, y2_centro, 
                                    fill=color_via, width=grosor_via, 
                                    tags=(f"via_line", f"via_{via.id_via}"))
                # bind en click para la vía
                try:
                    c.tag_bind(f"via_{via.id_via}", '<Button-1>', self.via_seleccionada)
                except Exception:
                    pass
                
                self.vias_mostradas.append(via.id_via)

    def limpiar_vias(self):
        #borrat vias
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
                
                # Color gris para vías no seleccionadas
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
        cnv = self.canvas
        # Borrar solo estaciones, vías y etiquetas de pasajeros (preservar trenes)
        for item in cnv.find_withtag('estacion'):
            cnv.delete(item)
        for item in cnv.find_withtag('texto'):
            cnv.delete(item)
        for item in cnv.find_withtag('info'):
            cnv.delete(item)
        for item in cnv.find_withtag('pasajeros'):
            cnv.delete(item)
        for item in cnv.find_withtag('via_line'):
            cnv.delete(item)
        #Area de dibujo
        canvas_w = int(cnv['width']) 
        canvas_h = int(cnv['height']) 
        rect_w = 100
        rect_h = 40
        #coordenadas
        centro_x = (canvas_w - rect_w) / 2
        centro_y = (canvas_h - rect_h) / 2
        #espacios entre estaciones
        espacio_vertical = 40
        espacio_horizontal = 50
        # Asignar coordenadas a cada estacion
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
                cnv.create_rectangle(x, y, x + rect_w, y + rect_h, 
                                 fill=estacion.color, outline=estacion.borde, width=2,
                                 tags=('estacion', f'estacion_{nombre}'))
                
                #nombre de la estación
                cnv.create_text(x + rect_w/2, y + rect_h/2, 
                            text=estacion.nombre, font=('Arial', 10, 'bold'),
                            tags=('texto', f'texto_{nombre}'))
                
                #información de trenes
                info_trenes = f"{len(estacion.trenes_esperando)}/{estacion.capacidad_de_trenes}"
                cnv.create_text(x + rect_w/2, y + rect_h + 12, 
                            text=info_trenes, font=('Arial', 8),
                            tags=('info', f'info_{nombre}'))
                #información de pasajeros en espera (debajo de la info de trenes)
                try:
                    if getattr(self, 'estado_sim', None) is not None:
                        pasajeros_esperando = self.estado_sim.contar_pasajeros_en_estacion(nombre)
                    else:
                        pasajeros_esperando = len(getattr(estacion, 'pasajeros_esperando', []))
                except Exception:
                    pasajeros_esperando = len(getattr(estacion, 'pasajeros_esperando', []))
                cnv.create_text(x + rect_w/2, y + rect_h + 28,
                              text=f"Pasajeros: {pasajeros_esperando}", font=('Arial', 8),
                              tags=('pasajeros', f'pasajeros_{nombre}'))
        # actualizar lista de trenes 
        self.actualizar_lista_estaciones()
        # Si hay una estación seleccionada actualizar su panel de información (pasajeros, trenes)
        if getattr(self, 'estacion_seleccionada_actual', None):
            estacion = self.estaciones_base.get(self.estacion_seleccionada_actual)
            if estacion:
                self.mostrar_informacion_estacion(estacion)
        
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
            self.resaltar_estacion()
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
    #funcion para que se vea la informacion de cada estacion
    def mostrar_informacion_estacion(self, estacion):
        nombre = getattr(estacion, 'nombre', 'Desconocida')
        estado = getattr(estacion, 'estado', 'Desconocido')
        trenes_esperando = len(getattr(estacion, 'trenes_esperando', []))
        capacidad_trenes = getattr(estacion, 'capacidad_de_trenes', 'N/A')
        poblacion = getattr(estacion, 'poblacion', 'N/D')
        #labels
        self.label_nombre.config(text=f"Estación: {nombre}")
        self.label_estado.config(text=f"Estado: {estado}")
        # Mostrar trenes como: número esperandos / capacidad si disponible
        self.label_trenes.config(text=f"Trenes: {trenes_esperando}/{capacidad_trenes}")
        self.label_poblacion.config(text=f"Población: {poblacion}")
        # Mostrar pasajeros en espera si la estación tiene la lista correspondiente
        try:
            if getattr(self, 'estado_sim', None) is not None:
                pasajeros = self.estado_sim.listar_pasajeros_en_estacion(nombre)
            else:
                pasajeros = getattr(estacion, 'pasajeros_esperando', [])
        except Exception:
            pasajeros = getattr(estacion, 'pasajeros_esperando', [])
        pasajeros_esperando = len(pasajeros)
        try:
            self.label_pasajeros.config(text=f"Pasajeros en espera: {pasajeros_esperando}")
        except Exception:
            pass
        # (Opcional) mostrar destinos de hasta 3 pasajeros en espera en el label de población
        try:
            destinos = []
            for p in pasajeros[:3]:
                try:
                    destinos.append(getattr(p, 'destino', str(p)))
                except Exception:
                    destinos.append(str(p))
            if destinos:
                self.label_poblacion.config(text=f"Población: {poblacion} | Destinos: {', '.join(destinos)}")
            else:
                self.label_poblacion.config(text=f"Población: {poblacion}")
        except Exception:
            try:
                self.label_poblacion.config(text=f"Población: {poblacion}")
            except Exception:
                pass

    def mostrar_informacion_via(self, via):
        if not via:
            return
        self.label_via_id.config(text=f"Vía: {via.id_via}")
        self.label_via_estaciones.config(text=f"Conecta: {via.conexion_estacion_a} - {via.conexion_estacion_b}")
        self.label_via_longitud.config(text=f"Longitud: {via.longitud} km")
        estado = "Libre" if getattr(via, 'estado', 'desocupada') == 'desocupada' else "Ocupada"
        self.label_via_estado.config(text=f"Estado: {estado}")
        tipo = "Rotatoria" if getattr(via, 'via_rotatoria', False) else "Normal"
        self.label_via_tipo.config(text=f"Tipo: {tipo}")
    #funcion para resaltar las vias
    def resaltar_via(self, via_id):
        c = self.canvas
        # resetear todas las vías a su color base
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
                c.itemconfig(item, fill='#ff6666', width=2)
            else:
                c.itemconfig(item, fill='#cccccc', width=2)
        # Ahora resaltar la seleccionada en verde oscuro
        
        if via_id is None:
            return
        for item in c.find_withtag(f'via_{via_id}'):
            c.itemconfig(item, fill="#00aa00", width=4)

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
        self.lista_trenes.delete(0, tk.END)
        for tren in self.trenes_list:
            nombre = getattr(tren, 'nombre_tren', str(tren))
            self.lista_trenes.insert(tk.END, nombre)
        
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
                c.delete(item)
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
            eventos = []
            # preferir el gestor de eventos de la propia pestaña
            if getattr(self, 'gestor_eventos', None) is not None:
                print('usando self.gestor_eventos')
                eventos = self.gestor_eventos.listar_eventos()
            # si existe un sistema externo con estado, usarlo
            elif getattr(self, 'sistema', None) is not None and hasattr(self.sistema, 'gestor_eventos'):
                eventos = self.sistema.gestor_eventos.listar_eventos()
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
                iterador = iter(eventos)
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

    #funcion para resaltar tren y sus rutas
    def resaltar_tren(self, nombre):
        c = self.canvas
        # resetear bosuqejo de todos los trenes
        for tren_info in getattr(self, "_train_items", {}).values():
            rectangulo_id = tren_info[0]
            c.itemconfig(rectangulo_id, outline=BORDE_TRENES, width=2) 
        # resaltar el seleccionado
        if nombre in getattr(self, '_train_items', {}):
            rectangulo_id = self.train_items[nombre][0]
    
        
    #funcion para resaltar estaciones al seleccionarla con sus vias
    def resaltar_estacion(self):
        # Limpiar cualquier resaltado de rutas previas cuando se selecciona una estación
        self.limpiar_resaltado_ruta()

    def limpiar_resaltado_ruta(self):
        c = self.canvas
        # Borrar líneas de rutas dibujadas previamente
        if hasattr(self, '_route_items') and self._route_items:
            for item in list(self._route_items):
                c.delete(item)
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
        cnv = self.canvas
        puntos = []
        for nombre in ruta:
            if nombre in getattr(self, '_posiciones', {}):
                # Resaltar la estación
                cnv.itemconfig(f'estacion_{nombre}', outline='#0000ff', width=3)
                x, y = self._posiciones[nombre]
                # Centro del rectángulo
                x_c = x + self._rect_w / 2
                y_c = y + self._rect_h / 2
                puntos.append((x_c, y_c))
        #dibujar líneas entre puntos consecutivos
        for a, b in zip(puntos, puntos[1:]):
                line = cnv.create_line(a[0], a[1], b[0], b[1], fill='#0000ff', width=3, tags=(f'ruta_{getattr(tren, "id_tren", "")}'))
                # Guardar para poder borrar luego
                self._route_items.append(line)

    def guardar_simulacion_actual(self):
        try:
            if self.estado_sim is None:
                messagebox.showwarning("Guardar", "No hay simulación en curso para guardar.")
                return
            
            exito, ruta = self.sistema_guardado.guardar_simulacion(self.estado_sim)
            
            if exito:
                messagebox.showinfo("Guardar", f"Simulación guardada exitosamente.\n\nUbicación: {ruta}")
            else:
                messagebox.showerror("Guardar", "Error al guardar la simulación. Consulte la consola para detalles.")
        except Exception as e:
            messagebox.showerror("Guardar", f"Error al guardar la simulación: {e}")
            print(f"Error en guardar_simulacion_actual: {e}")

    def cargar_simulacion_guardada(self):
        try:
            guardados = self.sistema_guardado.listar_guardados()
            
            if not guardados:
                messagebox.showinfo("Cargar", "No hay simulaciones guardadas disponibles.")
                return
            
            top = tk.Toplevel(self.parent)
            top.title("Cargar simulación")
            top.geometry('500x400')
            
            tk.Label(top, text="Selecciona una simulación para cargar:", font=("Arial", 10)).pack(pady=10)
            
            frame_list = ttk.Frame(top)
            frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            listbox = tk.Listbox(frame_list, selectmode=tk.SINGLE)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)
            
            mapeo_guardados = []
            
            for fecha in sorted(guardados.keys(), reverse=True):
                for guardado in sorted(guardados[fecha], key=lambda x: x['nombre'], reverse=True):
                    nombre_mostrado = f"{fecha} - {guardado['nombre'].replace('guardado_', '').replace('.json', '')}"
                    listbox.insert(tk.END, nombre_mostrado)
                    mapeo_guardados.append(guardado['ruta'])
            
            frame_botones = ttk.Frame(top)
            frame_botones.pack(fill=tk.X, padx=10, pady=10)
            
            def cargar_seleccionado():
                seleccion = listbox.curselection()
                if not seleccion:
                    messagebox.showwarning("Cargar", "Selecciona una simulación primero.")
                    return
                
                indice = seleccion[0]
                ruta = mapeo_guardados[indice]
                
                nuevo_estado = self.sistema_guardado.cargar_simulacion(ruta)
                
                if nuevo_estado is None:
                    messagebox.showerror("Cargar", "Error al cargar la simulación.")
                    return
                
                self.estado_sim = nuevo_estado
                self.reloj = self.estado_sim.hora_actual
                
                try:
                    self.dibujar_elementos()
                    self.actualizar_ui_reloj()
                    messagebox.showinfo("Cargar", "Simulación cargada exitosamente.")
                    top.destroy()
                except Exception as e:
                    messagebox.showerror("Cargar", f"Error al redibujar la simulación: {e}")
            
            def cancelar():
                top.destroy()
            
            btn_cargar = ttk.Button(frame_botones, text="Cargar", command=cargar_seleccionado)
            btn_cargar.pack(side=tk.LEFT, padx=5)
            
            btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=cancelar)
            btn_cancelar.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Cargar", f"Error al cargar simulaciones: {e}")
            print(f"Error en cargar_simulacion_guardada: {e}")

    #funcion para crear el ui del reloj 
    def crear_ui_reloj(self):
        frame_reloj = ttk.Frame(self.frame_simulacion)
        frame_reloj.pack(pady=10)

        self.label_reloj = ttk.Label(frame_reloj, text="", font=('Arial', 8))
        self.label_reloj.pack()

        boton_eventos_local = ttk.Button(frame_reloj, text="Ver eventos", command=self.mostrar_eventos_dialog)
        boton_eventos_local.pack(padx=4, pady=2)
        
        frame_botones_guardado = ttk.Frame(self.frame_simulacion)
        frame_botones_guardado.pack(pady=10, expand=False)
        
        boton_guardar_local = ttk.Button(frame_botones_guardado, text="Guardar simulación", command=self.guardar_simulacion_actual)
        boton_guardar_local.pack(padx=4, pady=2, side=tk.LEFT)
        
        boton_cargar_local = ttk.Button(frame_botones_guardado, text="Cargar simulación", command=self.cargar_simulacion_guardada)
        boton_cargar_local.pack(padx=4, pady=2, side=tk.LEFT)
        
        try:
            self._stop_when_empty_var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(frame_reloj, text='Detener al terminar eventos', variable=self._stop_when_empty_var)
            chk.pack(padx=4, pady=2)
        except Exception:
            self._stop_when_empty_var = tk.BooleanVar(value=True)
        
        self.actualizar_ui_reloj()
    #funcion para actualizar la ui del reloj junto a los ticks
    def actualizar_ui_reloj(self):
        try:
            hora = self.reloj.obtener_hora()
        except Exception:
            hora = str(self.reloj)
        self.label_reloj.config(text=f"Hora: {hora}")

    def reloj_tick_por_segundo(self):
        # avanzar segundos y actualizar
        self.reloj.avanzar_segundos(1)
        # contabilizar segundos para generación periódica de pasajeros
        try:
            self._seconds_since_last_generation += 1
        except Exception:
            self._seconds_since_last_generation = 1
        self.actualizar_ui_reloj()
        #procesar eventos programados hasta la hora actual (movimientos de trenes)
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
                    #si no quedan eventos y la opción está activa, detener el reloj
                    try:
                        eventos_restantes = len(self.gestor_eventos.listar_eventos())
                        if eventos_restantes == 0 and getattr(self, '_stop_when_empty_var', None) is not None and self._stop_when_empty_var.get():
                            try:
                                self.parar_reloj()
                                messagebox.showinfo('Simulación', 'Todos los eventos fueron procesados. Simulación detenida.')
                            except Exception:
                                pass
                    except Exception:
                        pass
        except Exception:
            pass
        # Generación periódica de pasajeros: cada 60 segundos simulados
        try:
            if getattr(self, 'estado_sim', None) is not None:
                if self._seconds_since_last_generation >= 60:
                    try:
                        # generar demanda por 1 minuto
                        try:
                            self.estado_sim.generar_demanda(1)
                            print(f'Pasajeros generados a las {self.reloj.obtener_hora()}')
                        except Exception as error:
                            print(f'Error generando pasajeros: {error}')
                        # redibujar estaciones y actualizar listas para reflejar nuevos pasajeros
                        try:
                            self.dibujar_estaciones()
                            self.actualizar_lista_estaciones()
                        except Exception:
                            pass
                    except Exception as error:
                        print(f'Error en generación periódica: {error}')
                    finally:
                        self._seconds_since_last_generation = 0
        except Exception as error:
            print(f'Error general en generación: {error}')
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
                self.parent.after_cancel(self._reloj_after_id)
                self._reloj_after_id = None