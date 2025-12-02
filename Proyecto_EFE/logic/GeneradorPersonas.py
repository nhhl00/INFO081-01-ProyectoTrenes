from .GeneradorClase import Generador
import datetime as dt
import random
from collections.abc import Callable
from typing import Any

class GeneradorPersonas(Generador):
    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        estacion_origen: Any,
        rutas_para_pasajeros: dict,
        update: bool = True,
    ): 

        if update:
            self.datetime_actual += dt.timedelta(minutes=minutos)

        # CPM: clientes por minuto basado en población y horas de operación
        # Usar max(1, ...) para evitar división por cero o valores negativos
        minutos_operacion = max(1, self.minutos_transcurridos())
        cpm = (self.poblacion * 0.2) / minutos_operacion
        size = int(minutos * cpm)
        # Asegurar al menos 1 cliente por minuto si hay población
        if self.poblacion > 0 and size < 1 and minutos > 0:
            size = max(1, int(self.poblacion * 0.001))
        clientes = []
        for _ in range(size):
            val = self.rdm.randint(0, 5_000_000)
            origen_nombre = estacion_origen.nombre
            destino_nombre = self.seleccionar_destino(origen_nombre, rutas_para_pasajeros)
            cliente = constructor(id_pasajero=val, origen=origen_nombre,destino=destino_nombre, tiempo_de_creacion=self.datetime_actual)
            clientes.append(cliente)
        return clientes
    
    def seleccionar_destino(self,origen_nombre:str, mapa_rutas:dict):
        # Busca los destinos que son accesibles desde el origen en el mapa de rutas
        destinos_validos = mapa_rutas.get(origen_nombre, []) 
    
        if not destinos_validos:
            # Si no hay vías que salgan de aquí, el pasajero no tiene destino
            return None 
    
        # Selecciona un destino al azar de los destinos posibles
        import random # Asegúrate de que random está importado (ya lo está en tu archivo)
        return random.choice(destinos_validos)
        

        
        
