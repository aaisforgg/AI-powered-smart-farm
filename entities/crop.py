import random

CROP_TYPES = {
    "trigo":  {"ticks_0": 20, "ticks_1": 30, "valor": 1, "estacion": "Primavera"},
    "maiz":   {"ticks_0": 25, "ticks_1": 40, "valor": 2, "estacion": "Verano"},
    "tomate": {"ticks_0": 30, "ticks_1": 50, "valor": 3, "estacion": "Otoño"},
    "papa":   {"ticks_0": 35, "ticks_1": 55, "valor": 2, "estacion": "Invierno"},
}


class Crop:

    def __init__(self, x, y, tipo=None):
        self.x = x
        self.y = y
        self.tipo = tipo or random.choice(list(CROP_TYPES.keys()))
        self.humedad = 100.0
        self.fase = 0
        self.ticks_en_fase = 0.0
        self.ticks_sequia = 0
        self.muerto = False

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def TICKS_PER_PHASE(self):
        info = CROP_TYPES.get(self.tipo, {"ticks_0": 30, "ticks_1": 50})
        return {0: info["ticks_0"], 1: info["ticks_1"]}

    @property
    def valor(self):
        return CROP_TYPES.get(self.tipo, {}).get("valor", 1)

    def crecer(self, tasa_secado, umbral_crecimiento=20, dry_multiplier=1.0, growth_multiplier=1.0):
        if self.muerto:
            return

        if self.humedad > 0:
            self.humedad = max(0.0, self.humedad - tasa_secado * dry_multiplier)

        if self.humedad <= 0:
            self.ticks_sequia += 1
            if self.ticks_sequia >= 20:
                self.muerto = True
                return
        else:
            self.ticks_sequia = 0

        if self.humedad > umbral_crecimiento and self.fase < 2:
            self.ticks_en_fase += growth_multiplier
            ticks_necesarios = self.TICKS_PER_PHASE.get(self.fase, 999)
            if self.ticks_en_fase >= ticks_necesarios:
                self.fase += 1
                self.ticks_en_fase = 0.0
