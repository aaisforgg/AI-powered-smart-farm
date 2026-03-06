
class Crop:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.humedad = 100.0
        self.fase = 0
        self.ticks_creciendo = 0

    def crecer(self, tasa_secado, umbral_crecimiento):
        if self.humedad > 0:
            self.humedad -= tasa_secado
            self.ticks_creciendo += 1
            if self.ticks_creciendo >= umbral_crecimiento:
                self.fase = min(self.fase + 1, 2)
                self.ticks_creciendo = 0
