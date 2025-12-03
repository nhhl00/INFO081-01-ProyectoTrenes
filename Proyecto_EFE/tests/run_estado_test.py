import sys
# Asegurar que el paquete local esté en sys.path
sys.path.insert(0, '.')

from logic import EstadoSimulacion
from models import Estacion, Vias

es = EstadoSimulacion()
# Crear estaciones de prueba
es.estaciones = {
    'Santiago': Estacion('Santiago', 'STG', 1000000, 5),
    'Rancagua': Estacion('Rancagua', 'RAN', 200000, 3),
}
# Crear vías entre ellas
es.vias = [Vias('V01', 87, 'Santiago', 'Rancagua', False, None)]
# Construir rutas y generar demanda
es.construir_rutas_para_pasajeros()

try:
    es.generar_demanda(5)
    total = sum(len(s.pasajeros_esperando) for s in es.estaciones.values())
    print('OK - generación completada')
    print('Total pasajeros generados:', total)
    for nombre, estacion in es.estaciones.items():
        print(f"  {nombre}: {len(estacion.pasajeros_esperando)} pasajeros esperando")
except Exception as e:
    print('ERROR durante generar_demanda:', e)
    raise
