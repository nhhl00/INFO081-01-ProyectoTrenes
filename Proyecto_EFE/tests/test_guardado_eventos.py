import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic.SistemaDeGuardado import SistemaGuardado
from logic.EstadoDeSimulacion import EstadoSimulacion
import datetime as dt
from logic.eventos import Evento

estado = EstadoSimulacion()
estado.estaciones = {"Santiago": {"nombre":"Santiago"}}
estado.vias = []
estado.trenes = []

ev = Evento(estado.hora_actual.fecha_hora + dt.timedelta(seconds=2), 'test_event', {'msg':'hola'})
estado.registrar_evento(ev)
sg = SistemaGuardado(directorio='saves_test')
ok = sg.guardar_simluacion(estado, 'prueba_eventos')
print('guardado', ok)
loaded = sg.cargar_simulacion('prueba_eventos')
print('loaded hora', loaded.hora_actual)
print('loaded eventos', loaded.listar_eventos())
