import datetime as dt

class horaActual:
    def __init__(self, hora=7, minuto=0, segundos=0, fecha = None): #07:00 hrs 
        if fecha is None:
            fecha = dt.date(2015, 3, 1)
        self.fecha_hora = dt.datetime.combine(fecha, dt.time(hora, minuto, segundos))

    def avanzar_segundos(self, segundos=1):
        self.fecha_hora += dt.timedelta(seconds=segundos)

    def avanzar_minutos(self, minutos=1):
        self.fecha_hora += dt.timedelta(minutes=minutos)

    def avanzar_horas(self, horas=1):
        self.fecha_hora += dt.timedelta(hours=horas)
    
    #propiedades para acceder a hora, minuto, segundo y fecha
    @property
    def hora(self):
        return self.fecha_hora.hour
    @property
    def minuto(self):
        return self.fecha_hora.minute
    @property
    def segundos(self):
        return self.segundos
    @property
    def fecha(self):
        return self.fecha_hora.date()

    def obtener_segundos(self):
        return self.fecha_hora.strftime("%S")
    def obtener_hora(self):
        return self.fecha_hora.strftime("%H:%M:%S")
    def obtener_fecha(self):
        return self.fecha_hora.strftime("%Y-%m-%d")
    def __str__(self):
        return self.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    

       

    
        


                    
            

        


    
