
class Crop:
    
    TICKS_PER_PHASE = {
        0: 30,
        1: 50,
    }

    def __init__(self, x, y):
        self.pos = (x, y)
        self.humedad = 100.0
        self.fase = 0
        self.ticks_en_fase = 0

    def crecer(self, tasa_secado, umbral_crecimiento, dry_multiplier=1.0):
        # Se seca más rápido si hay sequía/plaga
        if self.humedad > 0:
            self.humedad -= tasa_secado * dry_multiplier

        # Solo crece si hay humedad suficiente Y no está maduro
        if self.humedad > umbral_crecimiento and self.fase < 2:
            self.ticks_en_fase += 1
            ticks_necesarios = self.TICKS_PER_PHASE.get(self.fase, 999)
            if self.ticks_en_fase >= ticks_necesarios:
                self.fase += 1
                self.ticks_en_fase = 0