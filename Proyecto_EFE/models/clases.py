from config import COLOR_ESTACIONES, BORDE_ESTACIONES

class Estacion:
    def __init__(self, nombre, id_estacion, poblacion, capacidad_de_trenes): #parametros de la estacion
        self.nombre = nombre
        self.ubicacion = id_estacion  
        self.poblacion = poblacion
        self.estado = "activa"
        self.capacidad_de_trenes = capacidad_de_trenes
        self.trenes_esperando = []
        self.pasajeros_esperando = []
        #colores propios de las estaciones
        self.color = COLOR_ESTACIONES
        self.borde = BORDE_ESTACIONES

    def recibir_pasajero(self, pasajero):
        self.pasajeros_esperando.append(pasajero)

    def agregar_tren(self, tren):
        if tren not in self.trenes_esperando and len(self.trenes_esperando) < self.capacidad_de_trenes:
            self.trenes_esperando.append(tren)
            return True
        return False

    def embarcar_pasajeros(self, tren):
        while self.pasajeros_esperando and len(tren.pasajeros) < tren.capacidad:
            pasajero = self.pasajeros_esperando.pop(0)
            tren.abordar_pasajero(pasajero)

class Vias:
    def __init__(self, id_via, longitud, conexion_estacion_a, conexion_estacion_b, via_rotatoria, tren_en_via, estado):
        self.id_via = id_via
        self.conexion_estacion_a = conexion_estacion_a
        self.conexion_estacion_b = conexion_estacion_b
        self.longitud = longitud
        self.via_rotatoria = via_rotatoria
        self.tren_en_via = tren_en_via
        self.estado = "desocupada" #estado inicial de la via
        
            




class Tren:
    def __init__(self, nombre_tren, id_tren, capacidad, velocidad_constante, ruta, estacion_actual, vagones=2, estacion_destino=None):
        self.nombre_tren = nombre_tren 
        self.id_tren = id_tren
        self.capacidad = capacidad
        self.velocidad_constante = velocidad_constante
        self.ruta = ruta  
        self.pasajeros = []  
        self.estacion_actual = estacion_actual
        self.vagones = vagones
        self.estacion_destino = self.proximo_destino()
        self.estado = "detenido"

    def proximo_destino(self):
        if self.ruta and len(self.ruta) > 1:
            try:
                indice_actual = self.ruta.index(self.estacion_actual)
                if indice_actual < len(self.ruta) - 1:
                    return self.ruta[indice_actual+1]
            except ValueError:
                return self.ruta[0] if self.ruta else None
        return None
    
    def info_tren(self):
    #Informacion del tren en tkinter
        return f"""Tren: {self.nombre_tren}
    "ID": {self.id_tren}
    "Capacidad": {self.capacidad} pasajeros
    "Velocidad": {self.velocidad_constante} km/h
    "Vagones": {self.vagones}

    "Estación actual": {self.estacion_actual}
    "Próximo destino": {self.estacion_destino or "Fin de la ruta"}
    "Estado": {self.estado}

    "Pasajeros a bordo": {len(self.pasajeros)}/{self.capacidad}
    "Ruta": {' → '.join(self.ruta)}"""
    

class Pasajero:
    def __init__(self, id_pasajero, origen, destino):
        self.id_pasajero = id_pasajero
        self.origen = origen
        self.destino = destino

    def __str__(self):
        return f"Pasajero {self.id_pasajero} (de {self.origen} a {self.destino})"
    