import json
import os
import datetime

class SistemaGuardado:
    def __init__(self, directorio = "saves"):
        self.directorio = directorio
        if not os.path.exists(directorio):
            os.makedirs(directorio)


    def guardar_simluacion(self, estado, nombre_archivo):
        try:
            datos = {
                "hora_actual": getattr(estado, 'hora_actual').fecha_hora.isoformat() if hasattr(estado, 'hora_actual') else None,
                "estaciones": getattr(estado, "estaciones", []),
                "vias": getattr(estado, 'vias', []),
                "trenes": getattr(estado, "trenes", []),
                "eventos": getattr(estado, "eventos", []),
                "pasajeros_activos": getattr(estado, "pasajeros_activos", [])
            }

            ruta = f"{self.directorio}/{nombre_archivo}.json"
            with open(ruta, "w", encoding ="utf-8") as f:
                json.dump(datos, f, indent = 2, ensure_ascii = False)
            return True
        except Exception as e:
            print(f"Error guardando: {e}")
            return False


    def cargar_simulacion(self, nombre_archivo):
        try:
            ruta = f"{self.directorio}/{nombre_archivo}.json"
            with open(ruta, "r", encoding = "utf-8") as f:
                datos = json.load(f)

            from .EstadoDeSimulacion import EstadoSimulacion
            estado = EstadoSimulacion()
            # restaurar hora
            try:
                if datos.get("hora_actual"):
                    estado.hora_actual.fecha_hora = datetime.datetime.fromisoformat(datos.get("hora_actual"))
            except Exception:
                pass
            estado.estaciones = datos.get("estaciones", {})
            estado.vias = datos.get("vias", [])
            estado.trenes = datos.get("trenes", [])
            # cargar eventos (lista de dicts)
            try:
                estado.cargar_eventos_desde_lista(datos.get("eventos", []))
            except Exception:
                pass
            estado.pasajeros_activos = datos.get("pasajeros_activos", [])
            return estado
        except Exception as e:
            print(f"Error cargando: {e}")
            return None
    