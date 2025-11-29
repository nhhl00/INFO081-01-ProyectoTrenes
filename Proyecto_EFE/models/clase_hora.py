import datetime as dt

class Hora:
    def __init__(self, hora=7, minuto=0, fecha=dt.date(2015, 3, 1)):
        self.hora = hora
        self.minuto = minuto

    def avanzar_minuto(self):
        self.minuto += 1
        if self.minuto >= 60:
            self.minuto = 0
            self.hora += 1
            if self.hora >= 24:
                self.hora = 0

    def __str__(self):
        return f"{self.hora:02}:{self.minuto:02}"