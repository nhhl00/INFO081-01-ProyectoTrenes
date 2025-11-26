import datetime

class EstadoSimulacion:
    def __init__(self):
       #07:00 hrs del 1 de marzo de 2015
        self.hora_actual = datetime.datetime(2015, 3, 1, 7, 0)
        self.estaciones = []
        self.trenes = []
        self.pasajeros_activos = []
        self.eventos = []
        self.historial_pasajeros = []


    
