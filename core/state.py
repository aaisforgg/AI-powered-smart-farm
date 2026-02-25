class State:
    def __init__(self):
        self.granjero_pos = [0, 0]
        self.granjero_energia = 100
        self.granjero_inventario = [] # Lista de objetos Crop o Animal
        self.capacidad_max = 20.0
        
        self.mapa = {} # (x, y): "AGUA", "OBSTACULO", "PASTO"
        self.cultivos = []
        self.animales = []

    def costo_movimiento(self, x, y):
        terreno = self.mapa.get((x, y), "PASTO")
        if terreno == "OBSTACULO": return float('inf')
        
        # Factor Terreno: Agua cansa 3 veces más
        multiplicador_suelo = 3.0 if terreno == "AGUA" else 1.0
        
        # Factor Peso: (Peso total / Capacidad)
        peso_total = sum(item.peso for item in self.granjero_inventario)
        factor_carga = 1 + (peso_total / self.capacidad_max)
        
        return 1.0 * multiplicador_suelo * factor_carga