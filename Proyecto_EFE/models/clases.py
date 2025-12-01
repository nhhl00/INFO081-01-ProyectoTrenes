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
    def __init__(self, id_via, longitud, conexion_estacion_a, conexion_estacion_b, via_rotatoria, tren_en_via):
        self.id_via = id_via
        self.conexion_estacion_a = conexion_estacion_a
        self.conexion_estacion_b = conexion_estacion_b
        self.longitud = longitud
        self.via_rotatoria = via_rotatoria
        self.tren_en_via = tren_en_via
        self.estado = "desocupada" #estado inicial de la via
    #funcion para las conexiones entre estaciones
    def conexiones(self, conexion_estaacion_a, conexion_estacion_b):
        return self.conexion_estacion_a, self.conexion_estacion_b
    #calcular tiempo que demoraria un tren
    def tiempo_de_recorrido(self, longitud, velocidad_tren):
        self.tiempo_rec = self.longitud / velocidad_tren
        return self.tiempo_rec
    #cuando via esta ocupada
    def ocupar_via(self, tren):
        self.tren_en_via = tren
        self.estado = "ocupada"
    #cundo via esta desocupada
    def desocupar_via(self):
        self.tren_en_via = None
        self.estado = "desocupada"
    #referencias
    def __str__(self):
        return f"Via {self.id_via}: {self.conexion_estacion_a} <-> {self.conexion_estacion_b} {self.estado}"
    
        
        
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
        # Asegurar que la ruta sea lista y contenga al menos la estacion_actual
        self.ruta = ruta or []
        self.estacion_destino = estacion_destino if estacion_destino is not None else self.proximo_destino()
        self.estado = "detenido"

    def avanzar_a_destino(self):
        next_station = self.proximo_destino()
        if next_station:
            # Avanzar: actualizar estacion_actual y recalcular destino
            self.estacion_actual = next_station
            self.estacion_destino = self.proximo_destino()
            self.estado = "viajando"
            return next_station
        return None

    def indice_ruta_actual(self):
        #devuelve indice de la ruta actual o None si no est en ningun ruta
        if not self.ruta or self.estacion_actual is None:
            return None
        try:
            return self.ruta.index(self.estacion_actual)
        except ValueError:
            return None

    def proximo_destino(self):
        #proximo destino segun la ruta y estacion actual
        if not self.ruta:
            return None
        #tomar la primera estación de la ruta si no hay estacion actual
        if self.estacion_actual is None:
            return self.ruta[0]
        try:
            indice = self.ruta.index(self.estacion_actual)
            if indice < len(self.ruta) - 1:
                return self.ruta[indice + 1]
            else:
                return None  # Fin de la ruta
        except ValueError:
            # Si la estación actual no está en la ruta, devolver primer elemento
            return self.ruta[0]

    def ruta_restante(self):
        #lista con lo que falta de la ruta teniendo en cuenta la primera estacion
        if not self.ruta:
            return []
        indice = self.indice_ruta_actual()
        if indice is None:
            return list(self.ruta)
        return self.ruta[indice:]
    
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