import json
import os
import datetime
import tkinter as tk

class SistemaGuardado:
    def __init__(self, directorio="saves"):
        self.directorio = directorio
        if not os.path.exists(directorio):
            os.makedirs(directorio)
    #crear la ruta para guardar
    def _crear_ruta_guardado(self, fecha_hora):
        fecha = fecha_hora.date()
        hora = fecha_hora.time()
        año = fecha.year
        carpeta_año = os.path.join(self.directorio, str(año))
        #mes del archivo
        mes = f"{fecha.month:02d}"
        carpeta_mes = os.path.join(carpeta_año, mes)
        #dia del archivo
        dia = f"{fecha.day:02d}"
        carpeta_dia = os.path.join(carpeta_mes, dia)
        
        if not os.path.exists(carpeta_dia):
            os.makedirs(carpeta_dia)
        #darle nombre al archivo en base al tiempo
        nombre_archivo = f"guardado_{hora.hour:02d}-{hora.minute:02d}-{hora.second:02d}.json"
        ruta_completa = os.path.join(carpeta_dia, nombre_archivo)
        
        return ruta_completa
    
    def guardar_simulacion(self, estado, nombre_archivo=None):
        #Guarda la simulacion en una estructura de archivos por fecha y hora, usando como nombre la fecha y hora respectiva
        try:
            # Obtener la hora actual de la simulación
            fecha_hora = getattr(estado, 'hora_actual').fecha_hora if hasattr(estado, 'hora_actual') else datetime.datetime.now()
            
            # Crear ruta con estructura de carpetas
            ruta = self._crear_ruta_guardado(fecha_hora)
            
            # datos de la simulación
            datos = {
                "hora_actual": fecha_hora.isoformat() if fecha_hora else None,
                "estaciones": self.serializar_estaciones(getattr(estado, "estaciones", {})),
                "vias": self.serializar_vias(getattr(estado, 'vias', [])),
                "trenes": self.serializar_trenes(getattr(estado, "trenes", [])),
                "eventos": self.serializar_eventos(getattr(estado, "eventos", [])),
                "pasajeros_activos": self.serializar_pasajeros(getattr(estado, "pasajeros_activos", []))
            }
            # Guardar a archivo JSON
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True, ruta
        except Exception as error:
            print(f"Error guardando: {error}")
            return False, None
    #guardar datos de estaciones en el archivo de guardado
    def serializar_estaciones(self, estaciones):
        if isinstance(estaciones, dict):
            resultado = {}
            for nombre, estacion in estaciones.items():
                resultado[nombre] = {
                    "nombre": getattr(estacion, 'nombre', nombre),
                    "id_estacion": getattr(estacion, 'ubicacion', ''),
                    "poblacion": getattr(estacion, 'poblacion', 0),
                    "capacidad_de_trenes": getattr(estacion, 'capacidad_de_trenes', 0),
                    "estado": getattr(estacion, 'estado', 'activa'),
                    "trenes_esperando": [getattr(t, 'id_tren', str(t)) for t in getattr(estacion, 'trenes_esperando', [])],
                    "pasajeros_esperando": len(getattr(estacion, 'pasajeros_esperando', []))
                }
            return resultado
        return estaciones
    #guardar datos de vias en el archivo de guardado
    def serializar_vias(self, vias):
        resultado = []
        for via in vias:
            resultado.append({
                "id_via": getattr(via, 'id_via', ''),
                "longitud": getattr(via, 'longitud', 0),
                "conexion_estacion_a": getattr(via, 'conexion_estacion_a', ''),
                "conexion_estacion_b": getattr(via, 'conexion_estacion_b', ''),
                "estado": getattr(via, 'estado', 'desocupada'),
                "tren_en_via": getattr(via, 'tren_en_via', None),
                "via_rotatoria": getattr(via, 'via_rotatoria', False)
            })
        return resultado
    #guardar datos de trenes en el archivo de guardado
    def serializar_trenes(self, trenes):
        resultado = []
        for tren in trenes:
            resultado.append({
                "nombre_tren": getattr(tren, 'nombre_tren', ''),
                "id_tren": getattr(tren, 'id_tren', ''),
                "capacidad": getattr(tren, 'capacidad', 0),
                "velocidad_constante": getattr(tren, 'velocidad_constante', 0),
                "ruta": getattr(tren, 'ruta', []),
                "estacion_actual": getattr(tren, 'estacion_actual', ''),
                "estacion_destino": getattr(tren, 'estacion_destino', ''),
                "vagones": getattr(tren, 'vagones', 0),
                "estado": getattr(tren, 'estado', 'detenido'),
                "pasajeros": len(getattr(tren, 'pasajeros', []))
            })
        return resultado
    #guardar datos de eventos en el archivo de guardado
    def serializar_eventos(self, eventos):
        resultado = []
        if hasattr(eventos, 'listar_eventos'):
            eventos = eventos.listar_eventos()
        for evento in eventos:
            resultado.append({
                "tiempo": str(getattr(evento, 'tiempo', '')),
                "tipo": getattr(evento, 'tipo', ''),
                "datos": getattr(evento, 'datos', {})
            })
        return resultado
    #guardar datos de pasajeros en el archivo de guardado
    def serializar_pasajeros(self, pasajeros):
        return len(pasajeros)
    #guardar datos de simulacion en el archivo de guardado
    def cargar_simulacion(self, ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            from .EstadoDeSimulacion import EstadoSimulacion
            estado = EstadoSimulacion()
            
            #Restaurar hora
            if datos.get("hora_actual"):
                    estado.hora_actual.fecha_hora = datetime.datetime.fromisoformat(datos.get("hora_actual"))
            
            estado.estaciones = datos.get("estaciones", {})
            estado.vias = datos.get("vias", [])
            estado.trenes = datos.get("trenes", [])
            estado.pasajeros_activos = datos.get("pasajeros_activos", [])
            
            return estado
        except Exception as e:
            print(f"Error cargando: {e}")
            return None
    ##lista de archivos guardados
    def listar_guardados(self):
        guardados = {}
        
        if not os.path.exists(self.directorio):
            return guardados
        
        #Recorrer la estructura de carpetas año/mes/día
        for año in os.listdir(self.directorio):
            año_path = os.path.join(self.directorio, año)
            if not os.path.isdir(año_path):
                continue
            
            for mes in os.listdir(año_path):
                mes_path = os.path.join(año_path, mes)
                if not os.path.isdir(mes_path):
                    continue
                
                for dia in os.listdir(mes_path):
                    dia_path = os.path.join(mes_path, dia)
                    if not os.path.isdir(dia_path):
                        continue
                    
                    fecha_str = f"{año}-{mes}-{dia}"
                    if fecha_str not in guardados:
                        guardados[fecha_str] = []
                    
                    # Listar archivos de guardado en este día
                    for archivo in sorted(os.listdir(dia_path)):
                        if archivo.endswith('.json'):
                            ruta_completa = os.path.join(dia_path, archivo)
                            guardados[fecha_str].append({
                                'nombre': archivo,
                                'ruta': ruta_completa
                            })
        return guardados