from logic.GeneradorClase import Generador
import datetime as dt
import random
from collections.abc import Callable
from typing import Any
from logic import EstadoDeSimulacion

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

        cpm = self.poblacion * 0.2 / self.minutos_transcurridos()
        size = int(minutos * cpm)
        clientes = []
        for _ in range(size):
            val = self.rdm.randint(0, 5_000_000)
            origen_nombre = estacion_origen.nombre
            destino_nombre = self.seleccionar_destino(origen_nombre)
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
        

        
        
