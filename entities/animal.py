class Animal:
    def __init__(self, especie, x, y, peso_producto):
        self.especie = especie
        self.pos = (x, y)
        self.peso_producto = peso_producto

    def alimentar(self):
        self.hambre = 0
        print(f"El animal {self.especie} ha sido alimentado.")