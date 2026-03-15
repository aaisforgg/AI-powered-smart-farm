
class Crop:

    def __init__(self, x, y):
        self.pos = (x, y)
        self.humedad = 100.0
        self.fase = 0
        self.ticks_en_fase = 0

    def crecer(self, tasa_secado, ticks_por_fase=20):
        if self.humedad > 0:
            self.humedad -= tasa_secado

        if self.fase < 2:
            self.ticks_en_fase += 1
            if self.ticks_en_fase >= ticks_por_fase:
                self.fase += 1
                self.ticks_en_fase = 0