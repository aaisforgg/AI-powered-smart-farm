class Animal:
    def __init__(self, especie, x, y, peso_producto):
        self.especie = especie
        self.pos = (x, y)
        self.hambre = 0
        self.peso_producto = peso_producto

    def actualizar(self):
        self.hambre += 2

    def alimentar(self):
        self.hambre = 0
        print(f"El animal {self.especie} ha sido alimentado.")