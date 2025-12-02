#!/usr/bin/env python3
"""
Test para verificar que los eventos se procesan sin mover visualmente los trenes.
"""
import sys
import os
import datetime as dt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.EstadoDeSimulacion import EstadoSimulacion, horaActual
from logic.eventos import Evento
from models import Estacion, Tren, Vias

def test_eventos_sin_movimiento_visual():
    """Verifica que los trenes permanecen en su posición inicial incluso con eventos."""
    
    # Crear estado
    estado_sim = EstadoSimulacion()
    
    # Crear estaciones
    estaciones = {
        "Santiago": Estacion("Santiago", "STG", 8242459, 1),
        "Rancagua": Estacion("Rancagua", "RAN", 274407, 1),
        "Talca": Estacion("Talca", "TAL", 242344, 1),
    }
    
    # Crear vías
    vias = [
        Vias("V01", 87, "Santiago", "Rancagua", False, None),
        Vias("V02", 200, "Rancagua", "Talca", False, None),
    ]
    
    # Crear tren
    tren = Tren("BMU", "T01", 236, 160, ["Santiago", "Rancagua", "Talca"], "Santiago", 4)
    trenes = [tren]
    
    # Sincronizar
    estado_sim.estaciones = estaciones
    estado_sim.vias = vias
    estado_sim.trenes = trenes
    
    print(f"[TEST] Posición inicial del tren: {tren.estacion_actual}")
    print(f"[TEST] Próximo destino: {tren.proximo_destino()}")
    
    # Crear y agendar evento para mover tren a Rancagua
    tiempo_evento = dt.datetime(2015, 3, 1, 7, 2, 0)
    evento = Evento(tiempo_evento, 'forzar_mover_tren', {'id_tren': tren.id_tren, 'destino': 'Rancagua'})
    estado_sim.gestor_eventos.agendar(evento)
    
    print(f"\n[TEST] Evento agendado: {evento.tipo} hacia {evento.datos['destino']} a las {tiempo_evento}")
    print(f"[TEST] Posición antes de procesar: {tren.estacion_actual}")
    
    # Procesar evento
    estado_sim.hora_actual.fecha_hora = tiempo_evento
    procesados = estado_sim.gestor_eventos.procesar_hasta(estado_sim.hora_actual.fecha_hora, estaciones, vias, trenes)
    
    print(f"\n[TEST] Eventos procesados: {len(procesados)}")
    print(f"[TEST] Posición después de procesar: {tren.estacion_actual}")
    
    # Verificar que la posición NO cambió
    if tren.estacion_actual == "Santiago":
        print("\n✓ [PASS] El tren sigue en su posición inicial (Santiago)")
    else:
        print(f"\n✗ [FAIL] El tren se movió a {tren.estacion_actual} (debería seguir en Santiago)")
    
    # Verificar que el próximo destino sigue siendo válido
    print(f"[TEST] Próximo destino del tren: {tren.proximo_destino()}")

if __name__ == "__main__":
    test_eventos_sin_movimiento_visual()
