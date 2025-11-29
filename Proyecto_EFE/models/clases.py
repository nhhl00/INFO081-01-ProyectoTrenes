from config import COLOR_ESTACIONES, BORDE_ESTACIONES

class Estacion:
    def __init__(self, nombre, id_estacion, poblacion, capacidad_de_trenes):
        self.nombre = nombre
        self.ubicacion = id_estacion  
        self.poblacion = poblacion
        self.estado = "activa"
        self.capacidad_de_trenes = capacidad_de_trenes
        self.trenes_esperando = []
        self.pasajeros_esperando = []
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
    def __init__(self, id_via, longitud, conexion_estacion_a, conexion_estacion_b, via_rotatoria):
        self.id_via = id_via
        self.conexion_estacion_a = conexion_estacion_a
        self.conexion_estacion_b = conexion_estacion_b
        self.longitud = longitud
        self.via_rotatoria = via_rotatoria






class Tren:
    def __init__(self, id_tren, capacidad, velocidad_max, ruta):
        self.id_tren = id_tren
        self.capacidad = capacidad
        self.velocidad_max = velocidad_max
        self.ruta = ruta  
        self.pasajeros = []  

    def abordar_pasajero(self, pasajero):
        if len(self.pasajeros) < self.capacidad:
            self.pasajeros.append(pasajero)
        else:
            print(f"El tren {self.id_tren} está lleno.")

    def avanzar(self):
        print(f"El tren {self.id_tren} avanza a la siguiente estación.")


class Pasajero:
    def __init__(self, id_pasajero, origen, destino):
        self.id_pasajero = id_pasajero
        self.origen = origen
        self.destino = destino

    def __str__(self):
        return f"Pasajero {self.id_pasajero} (de {self.origen} a {self.destino})"
    