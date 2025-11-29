from models.estacion import Estacion

class GestorEstaciones:
    def __init__(self):              # Lista donde se almacenarán todas las estaciones creadas
        self.estaciones = []

    def agregar(self, nombre, poblacion, vias):
        est = Estacion(nombre, poblacion, vias)           # Crea una nueva estación y la agrega a la lista
        self.estaciones.append(est)

    def encontrar_estacion(self, nombre):                               # Busca y devuelve una estación según su nombre
        for e in self.estaciones:
            if e.nombre == nombre:
                return e
        return None

    def eliminar(self, nombre):                               # Elimina la estación cuyo nombre coincida, dejando todas las demás
        self.estaciones = [e for e in self.estaciones if e.nombre != nombre]
