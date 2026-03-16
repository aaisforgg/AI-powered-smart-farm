import random


class Particle:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto  = alto
        self.reset()

    def reset(self):
        self.x         = random.randint(0, self.ancho)
        self.y         = random.randint(-self.alto, 0)
        self.velocidad = random.randint(2, 6)

    def caer(self):
        self.y += self.velocidad
        if self.y > self.alto:
            self.reset()
