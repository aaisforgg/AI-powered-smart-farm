class Crop:

    TICKS_PER_PHASE = {
        0: 30,
        1: 50,
    }

    def __init__(self, x, y, tipo="generico"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.humedad = 100.0
        self.fase = 0
        self.ticks_en_fase = 0
        self.ticks_sequia = 0
        self.muerto = False

    @property
    def pos(self):
        return (self.x, self.y)

    def crecer(self, tasa_secado, umbral_crecimiento=20, dry_multiplier=1.0):
        if self.muerto:
            return

        if self.humedad > 0:
            self.humedad = max(0.0, self.humedad - tasa_secado * dry_multiplier)

        # Muerte por sequía prolongada
        if self.humedad <= 0:
            self.ticks_sequia += 1
            if self.ticks_sequia >= 20:
                self.muerto = True
                return
        else:
            self.ticks_sequia = 0

        # Crecimiento normal
        if self.humedad > umbral_crecimiento and self.fase < 2:
            self.ticks_en_fase += 1
            ticks_necesarios = self.TICKS_PER_PHASE.get(self.fase, 999)
            if self.ticks_en_fase >= ticks_necesarios:
                self.fase += 1
                self.ticks_en_fase = 0