import random


ANIMAL_TYPES = {
    "gallina": {"producto": "huevo",  "valor": 1, "hambre_rate": 2, "produce_cada": 40},
    "vaca":    {"producto": "leche",  "valor": 3, "hambre_rate": 3, "produce_cada": 60},
    "oveja":   {"producto": "lana",   "valor": 2, "hambre_rate": 2, "produce_cada": 50},
}


class Animal:
    def __init__(self, x, y, especie=None):
        self.x = x
        self.y = y
        self.especie = especie or random.choice(list(ANIMAL_TYPES.keys()))
        info = ANIMAL_TYPES[self.especie]
        self.producto         = info["producto"]
        self.valor            = info["valor"]
        self.hambre_rate      = info["hambre_rate"]
        self.produce_cada     = info["produce_cada"]

        self.hambre                 = 0
        self.ticks_sin_alimentar    = 0
        self.ticks_desde_produccion = 0
        self.producto_listo         = False

    @property
    def pos(self):
        return (self.x, self.y)

    def actualizar(self):
        """Llamar cada tick desde tick_animals."""
        self.hambre = min(100, self.hambre + self.hambre_rate)
        self.ticks_sin_alimentar += 1

        if self.hambre < 50:
            self.ticks_desde_produccion += 1
            if self.ticks_desde_produccion >= self.produce_cada:
                self.producto_listo = True
                self.ticks_desde_produccion = 0

    def alimentar(self):
        self.hambre = 0
        self.ticks_sin_alimentar = 0

    def recoger_producto(self):
        if self.producto_listo:
            self.producto_listo = False
            return (self.producto, self.valor)
        return None
