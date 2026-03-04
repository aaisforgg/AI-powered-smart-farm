class Animal:
    def __init__(self, especie, x, y):
        self.especie = especie # "Vaca", "Gallina"
        self.pos = (x, y)
        self.hambre = 0
        self.peso_producto = 2.0 if especie == "Vaca" else 0.1 # Leche vs Huevo

    def actualizar(self):
        self.hambre += 2