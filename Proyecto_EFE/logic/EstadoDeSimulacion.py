import datetime as dt
from .eventos import GestorEventos, Evento

class horaActual:
    """Representa la fecha y hora de la simulación y permite avanzar el tiempo."""
    def __init__(self, hora=7, minuto=0, segundos=0, fecha=None):
        if fecha is None:
            fecha = dt.date(2015, 3, 1)
        self.fecha_hora = dt.datetime.combine(fecha, dt.time(hora, minuto, segundos))

    def avanzar_segundos(self, segundos=1):
        self.fecha_hora += dt.timedelta(seconds=segundos)

    def avanzar_minutos(self, minutos=1):
        self.fecha_hora += dt.timedelta(minutes=minutos)

    def avanzar_horas(self, horas=1):
        self.fecha_hora += dt.timedelta(hours=horas)

    @property
    def hora(self):
        return self.fecha_hora.hour

    @property
    def minuto(self):
        return self.fecha_hora.minute

    @property
    def segundos(self):
        return self.fecha_hora.second

    @property
    def fecha(self):
        return self.fecha_hora.date()

    def obtener_segundos(self):
        return self.fecha_hora.strftime("%S")

    def obtener_hora(self):
        return self.fecha_hora.strftime("%H:%M:%S")

    def obtener_fecha(self):
        return self.fecha_hora.strftime("%Y-%m-%d")

    def isoformat(self):
        return self.fecha_hora.isoformat()

    def __str__(self):
        return self.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")


class EstadoSimulacion:
    """Estado global de la simulación.

    Contiene el reloj (`hora_actual`), colecciones de `estaciones`, `vias`, `trenes`,
    `pasajeros_activos` y un `GestorEventos` para mantener la agenda de eventos.
    """
    def __init__(self):
        self.hora_actual = horaActual()
        self.estaciones = {}  # dict nombre -> Estacion (o serializable dicts)
        self.vias = []
        self.trenes = []
        self.pasajeros_activos = []
        self.gestor_eventos = GestorEventos()
        self.rutas_para_pasajeros = {}

    def construir_rutas_para_pasajeros(self):
        self.rutas_para_pasajeros = {}
        for via in self.vias:
            estacion_a = via.conexion_estacion_a
            estacion_b = via.conexion_estacion_b
            # Ruta de A hacia B
            if estacion_a not in self.rutas_para_pasajeros:
                self.rutas_para_pasajeros[estacion_a] = []
            self.rutas_para_pasajeros[estacion_a].append(estacion_b)
        
            # también permite la ruta de B hacia A (asegurarse de inicializar la lista)
            if estacion_b not in self.rutas_para_pasajeros:
                self.rutas_para_pasajeros[estacion_b] = []
            self.rutas_para_pasajeros[estacion_b].append(estacion_a)


    def generar_demanda(self,minutos:int):
        # Asegurar que el mapa de rutas está construido
        if not self.rutas_para_pasajeros:
            self.construir_rutas_para_pasajeros()
        
        rutas_disponibles = self.rutas_para_pasajeros
    
        for estacion in self.estaciones.values():
            # Importar Pasajero localmente para evitar import circular entre logic <-> models
            try:
                from models import Pasajero
            except Exception:
                Pasajero = None
            if Pasajero is None:
                continue
            
            # Sincronizar el datetime del generador con la simulación
            try:
                estacion.generador.datetime_actual = self.hora_actual.fecha_hora
            except Exception:
                pass
            
            clientes = estacion.generador.generar_clientes(minutos=minutos, constructor=Pasajero, estacion_origen=estacion, rutas_para_pasajeros=rutas_disponibles, update=False)
            # Añadir clientes generados a la estación (si existe API) y al estado global
            try:
                for c in clientes:
                    try:
                        estacion.recibir_pasajero(c)
                    except Exception:
                        pass
                    # mantener lista global de pasajeros activos para monitoreo
                    try:
                        self.pasajeros_activos.append(c)
                    except Exception:
                        pass
            except Exception:
                pass

    def contar_pasajeros_en_estacion(self, nombre_estacion):
        try:
            est = self.estaciones.get(nombre_estacion)
            if not est:
                return 0
            return len(getattr(est, 'pasajeros_esperando', []))
        except Exception:
            return 0

    def listar_pasajeros_en_estacion(self, nombre_estacion):
        try:
            est = self.estaciones.get(nombre_estacion)
            if not est:
                return []
            return list(getattr(est, 'pasajeros_esperando', []))
        except Exception:
            return []

    # lista de eventos: registrar, listar y procesar
    def registrar_evento(self, evento):
        if isinstance(evento, Evento):
            self.gestor_eventos.agendar(evento)
            return evento
        try:
            tiempo_iso = evento.get('tiempo')
            tiempo = dt.datetime.fromisoformat(tiempo_iso)
            ev = Evento(tiempo, evento.get('tipo', ''), evento.get('datos', {}))
            # permitir conservar id si viene
            if 'id' in evento:
                ev.id = evento['id']
            self.gestor_eventos.agendar(ev)
            return ev
        except Exception:
            return None

    def listar_eventos(self):
        resultado = []
        for e in self.gestor_eventos.listar_eventos():
            resultado.append({
                'tiempo': e.tiempo.isoformat(),
                'tipo': e.tipo,
                'datos': e.datos,
                'id': getattr(e, 'id', None)
            })
        return resultado

    def cargar_eventos_desde_lista(self, eventos_lista):
        for ev in eventos_lista or []:
            try:
                tiempo = dt.datetime.fromisoformat(ev.get('tiempo'))
                nuevo = Evento(tiempo, ev.get('tipo'), ev.get('datos', {}))
                if 'id' in ev:
                    nuevo.id = ev['id']
                self.gestor_eventos.agendar(nuevo)
            except Exception:
                pass

    def procesar_hasta(self):
        return self.gestor_eventos.procesar_hasta(self.hora_actual.fecha_hora, self.estaciones, self.vias, self.trenes)

    # propiedad para compatibilidad con el sistema de guardado
    @property
    def eventos(self):
        return self.listar_eventos()