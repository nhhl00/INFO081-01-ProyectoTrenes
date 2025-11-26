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
                "hora_actual": estado.hora_actual.isoformat(),
                "estaciones": getattr(estado, "estaciones", []),
                "trenes": getattr(estado, "trenes", []),
                "eventos": getattr(estado, "eventos", []),
                "pasajeros_activos": getattr(estado, "pasajeros_activos", [])
            }

            ruta = f"{sel.directorio}/{nombre_archivo}.json"
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

            from models.EstadoDeSimulacion import EstadoSimulacion
            estado = EstadoSimulacion()
            estado.hora_actual = datetime.datetime.fromisoformat(datos["hora_actual"])
            estado.estaciones = datos.get("estaciones", [])
            estado.trenes = datos.get("trenes", [])
            estado.eventos = datos.get("eventos", [])
            estado_pasajeros_activos = datos.get("pasajeros_activos", [])
            return estado
        except Exception as e:
            print(f"Error cargando: {e}")
            return None
    