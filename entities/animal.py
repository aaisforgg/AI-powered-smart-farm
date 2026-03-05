# entities/animal.py

class Animal:
    def __init__(self, especie, x, y, peso_producto):
        self.especie = especie
        self.pos = (x, y)
        self.peso_producto = peso_producto
        # Pedro: "agregar self.hambre = 0" - ¡Listo!
        self.hambre = 0

    def alimentar(self):
        """Reduce el hambre, pero nunca por debajo de 0."""
        self.hambre = max(0, self.hambre - 1)
        print(f"El animal {self.especie} ha sido alimentado. Hambre actual: {self.hambre}")

    def actualizar(self):
        """
        Pedro: "y método actualizar()" 
        Este método debe llamarse en cada ciclo del Pipeline.
        """
        self.hambre += 1
        print(f"Turno pasado: El {self.especie} en {self.pos} ahora tiene {self.hambre} de hambre.")