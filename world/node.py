# assets/nodes.py

class Node:
    def __init__(self, x, y, terrain_id, terrain_name):
        self.x = x
        self.y = y
        self.type_id = terrain_id
        self.type_name = terrain_name
        
        # Lógica de navegación para el Agente Racional
        self.walkable = terrain_name not in ["agua", "acantilado", "edificio"]
        
        # Costos para A* (cruzar cultivos es más "caro" que el pasto)
        self.cost = 5 if terrain_name == "cultivo" else 1
        
        # Variables para el algoritmo A*
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost