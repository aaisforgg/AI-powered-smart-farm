class Crop:
    def __init__(self, tipo, x, y):
        self.tipo = tipo  # "Trigo", "Maiz"
        self.pos = (x, y)
        self.fase = 0  # 0: Semilla, 1: Brote, 2: Maduro
        self.humedad = 100
        # Definimos pesos por tipo
        self.peso = 0.5 if tipo == "Trigo" else 0.8

    def crecer(self):
        if self.humedad > 0:
            self.humedad -= 5 
            if self.humedad > 20: self.fase = min(self.fase + 1, 2)