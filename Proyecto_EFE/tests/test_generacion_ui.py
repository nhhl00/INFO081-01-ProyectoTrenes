#Test de generación de pasajeros en la UI simulando el tick del reloj.
import sys
import os

# Agregar la carpeta padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import EstadoSimulacion, horaActual
from models import Estacion, Tren, Vias

def test_passenger_generation_ui_tick():
    #simula ticks y generacion de pasajeros cada 1 min (60 segundos)
    
    # Crear estado de simulación
    estado_sim = EstadoSimulacion()
    
    # Crear estaciones base
    estaciones_base = {
        "Santiago": Estacion("Santiago", "STG", 8242459, 1),
        "Rancagua": Estacion("Rancagua", "RAN", 274407, 1),
        "Talca": Estacion("Talca", "TAL" , 242344, 1),
        "Chillán": Estacion("Chillán", "CHL" , 204091, 1),
    }
    
    # Crear vías
    vias_base = [
        Vias("V01", 87, "Santiago", "Rancagua", False, None),
        Vias("V02", 400, "Santiago", "Chillán", False, None),
        Vias("V03", 120, "Chillán", "Talca", False, None),
        Vias("V04", 60, "Talca", "Santiago", False, None),
    ]
    
    # Crear trenes base
    trenes_base = [
        Tren("BMU", "T01", 236, 160, ["Santiago", "Rancagua", "Santiago"], "Santiago", 4),
        Tren("EMU", "T02", 250, 120, ["Talca", "Chillán", "Talca"], "Talca", 8)
    ]
    
    # Sincronizar estado
    estado_sim.estaciones = estaciones_base
    estado_sim.vias = vias_base
    estado_sim.trenes = trenes_base
    estado_sim.construir_rutas_para_pasajeros()
    
    print(f"[INFO] Rutas construidas: {estado_sim.rutas_para_pasajeros}")
    print(f"[INFO] Hora inicial: {estado_sim.hora_actual}")
    
    # Simular 65 ticks (cada tick es 1 segundo, así que a los 60 ticks se genera)
    seconds_since_gen = 0
    for tick in range(65):
        estado_sim.hora_actual.avanzar_segundos(1)
        seconds_since_gen += 1
        
        if seconds_since_gen >= 60:
            print(f"\n[TICK {tick}] Hora: {estado_sim.hora_actual} - GENERANDO PASAJEROS")
            try:
                estado_sim.generar_demanda(1)
                print(f"[SUCCESS] Pasajeros generados")
                # Mostrar conteos
                for nombre, est in estaciones_base.items():
                    count = len(est.pasajeros_esperando)
                    print(f"  {nombre}: {count} pasajeros en espera")
            except Exception as e:
                print(f"[ERROR] {e}")
            seconds_since_gen = 0
        else:
            print(f"[TICK {tick}] Hora: {estado_sim.hora_actual} - {60 - seconds_since_gen}s para próxima generación")

if __name__ == "__main__":
    test_passenger_generation_ui_tick()
