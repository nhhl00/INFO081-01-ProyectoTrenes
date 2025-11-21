class Estacion:
    def __init__(self, nombre: str, poblacion: int, vias: list, flujo_acumulado: int = 0):
        self.nombre = nombre
        self.poblacion = poblacion
        self.vias = vias  # lista de tuplas: (direccion, numero)
        self.flujo_acumulado = flujo_acumulado
