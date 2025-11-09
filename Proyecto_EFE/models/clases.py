class Estacion:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion  
        self.pasajeros_esperando = []

    def recibir_pasajero(self, pasajero):
        self.pasajeros_esperando.append(pasajero)

    def embarcar_pasajeros(self, tren):
        while self.pasajeros_esperando and len(tren.pasajeros) < tren.capacidad:
            pasajero = self.pasajeros_esperando.pop(0)
            tren.abordar_pasajero(pasajero)

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

