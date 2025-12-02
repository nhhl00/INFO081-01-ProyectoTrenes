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

    # API de eventos: registrar, listar y procesar
    def registrar_evento(self, evento):
        """Agrega un evento. `evento` puede ser instancia de Evento o dict serializable."""
        if isinstance(evento, Evento):
            self.gestor_eventos.agendar(evento)
            return evento
        # aceptar dict con campos 'tiempo' (iso), 'tipo', 'datos'
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
        """Devuelve la lista de eventos como diccionarios serializables."""
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
        """Carga eventos desde una lista de diccionarios (ej. desde JSON)."""
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
        """Procesa eventos hasta la hora actual del estado."""
        return self.gestor_eventos.procesar_hasta(self.hora_actual.fecha_hora, self.estaciones, self.vias, self.trenes)

    # propiedad para compatibilidad con el sistema de guardado
    @property
    def eventos(self):
        return self.listar_eventos()















