import datetime as dt
import uuid


class Evento:
    """Evento programado en la simulación.

    Atributos:
    - tiempo: datetime cuando debe ejecutarse
    - tipo: str identificador de la acción (ej. 'mover_tren')
    - datos: dict con datos necesarios para ejecutar el evento
    - id: id único del evento
    """
    def __init__(self, tiempo: dt.datetime, tipo: str, datos: dict = None):
        self.tiempo = tiempo
        self.tipo = tipo
        self.datos = datos or {}
        self.id = str(uuid.uuid4())

    def __lt__(self, other):
        return self.tiempo < other.tiempo


class GestorEventos:
    """Gestor simple de eventos: mantiene una lista ordenada y ejecuta acciones.

    Métodos principales:
    - agendar(evento)
    - procesar_hasta(hora_actual, estaciones, vias, trenes)
    """
    def __init__(self):
        self._eventos = []

    def agendar(self, evento: Evento):
        # Insertar manteniendo orden por tiempo
        self._eventos.append(evento)
        self._eventos.sort(key=lambda e: e.tiempo)

    def listar_eventos(self):
        return list(self._eventos)

    def eliminar_ultimo_duplicado(self, tipo: str, datos: dict) -> bool:
        """Elimina el último evento en la lista que coincida por tipo y datos si hay duplicados.

        Devuelve True si eliminó uno, False en caso contrario.
        """
        indices = [i for i, e in enumerate(self._eventos) if getattr(e, 'tipo', None) == tipo and getattr(e, 'datos', None) == datos]
        if len(indices) > 1:
            # eliminar el último (más reciente)
            del self._eventos[indices[-1]]
            return True
        return False

    def eliminar_evento_por_id(self, event_id: str) -> bool:
        """Elimina un evento por su id. Devuelve True si se eliminó, False si no se encontró."""
        for i, e in enumerate(self._eventos):
            if getattr(e, 'id', None) == event_id:
                del self._eventos[i]
                return True
        return False

    def _encontrar_tren(self, trenes, id_tren=None):
        if id_tren is None:
            return None
        for t in trenes:
            if getattr(t, 'id_tren', None) == id_tren:
                return t
        return None

    def _encontrar_via(self, vias, a, b):
        for v in vias:
            if (v.conexion_estacion_a == a and v.conexion_estacion_b == b) or (v.conexion_estacion_a == b and v.conexion_estacion_b == a):
                return v
        return None

    def procesar_hasta(self, hora_actual: dt.datetime, estaciones: dict, vias: list, trenes: list):
        """Procesa todos los eventos cuya hora <= hora_actual.

        Acciones soportadas por ahora:
        - 'mover_tren': mueve el tren al siguiente destino y (si aplica) agenda el siguiente movimiento.
        """
        procesados = []
        while self._eventos and self._eventos[0].tiempo <= hora_actual:
            evento = self._eventos.pop(0)
            try:
                # Debug: indicar qué evento se procesa
                try:
                    print(f"[GestorEventos] Procesando evento: {evento.tipo} id={getattr(evento,'id', '')} tiempo={evento.tiempo}")
                except Exception:
                    pass

                if evento.tipo == 'mover_tren':
                    id_tren = evento.datos.get('id_tren')
                    tren = self._encontrar_tren(trenes, id_tren)
                    if not tren:
                        continue
                    # determinar próximo destino
                    prox = tren.proximo_destino()
                    if prox is None:
                        # fin de ruta, no re-agendar
                        continue

                    # actualizar estado del tren: quitarlo de la estación actual (si estaba)
                    origen = getattr(tren, 'estacion_actual', None)
                    if origen and origen in estaciones:
                        try:
                            est_obj = estaciones[origen]
                            if tren in getattr(est_obj, 'trenes_esperando', []):
                                est_obj.trenes_esperando.remove(tren)
                        except Exception:
                            pass

                    # mover tren
                    tren.estacion_actual = prox

                    # agregar tren a la estación destino (si existe y hay capacidad)
                    if prox in estaciones:
                        try:
                            estaciones[prox].agregar_tren(tren)
                        except Exception:
                            pass

                    # agenda siguiente movimiento: buscar vía entre prox y siguiente de prox
                    siguiente = tren.proximo_destino()
                    if siguiente:
                        via = self._encontrar_via(vias, prox, siguiente)
                        if via:
                            # tiempo estimado: longitud (km) / velocidad (km/h) -> horas -> segundos
                            velocidad = getattr(tren, 'velocidad_constante', 60) or 60
                            horas = via.longitud / velocidad
                            segundos = int(horas * 3600)
                            if segundos <= 0:
                                segundos = 1
                            nuevo_tiempo = hora_actual + dt.timedelta(seconds=segundos)
                            nuevo_evento = Evento(nuevo_tiempo, 'mover_tren', {'id_tren': tren.id_tren})
                            self.agendar(nuevo_evento)

                elif evento.tipo == 'forzar_mover_tren':
                    # mover tren a una estación destino dada en los datos
                    id_tren = evento.datos.get('id_tren')
                    destino = evento.datos.get('destino')
                    tren = self._encontrar_tren(trenes, id_tren)
                    if not tren or not destino:
                        continue
                    # quitar tren de origen
                    origen = getattr(tren, 'estacion_actual', None)
                    if origen and origen in estaciones:
                        try:
                            est_obj = estaciones[origen]
                            if tren in getattr(est_obj, 'trenes_esperando', []):
                                est_obj.trenes_esperando.remove(tren)
                        except Exception:
                            pass
                    # mover a destino
                    tren.estacion_actual = destino
                    if destino in estaciones:
                        try:
                            estaciones[destino].agregar_tren(tren)
                        except Exception:
                            pass
                # otros tipos de eventos pueden añadirse aquí
            except Exception:
                # no detener procesamiento por excepción en un evento
                pass
            procesados.append(evento)
        return procesados
