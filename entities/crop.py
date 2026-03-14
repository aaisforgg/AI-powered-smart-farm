class Crop:

    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.humedad = 100.0
        self.fase = 0

    @property
    def pos(self):
        return (self.x, self.y)

    def crecer(self, tasa_secado, umbral_crecimiento):

        if self.humedad > 0:
            self.humedad -= tasa_secado

        if self.humedad > umbral_crecimiento:
            self.fase = min(self.fase + 1, 3)
