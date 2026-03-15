class Node:
    def __init__(self, x, y, terrain_id, terrain_name):
        self.x = x
        self.y = y
        self.type_id = terrain_id
        self.type_name = terrain_name
        self.walkable = terrain_name not in ["agua", "acantilado", "edificio"]
        self.cost = 2 if terrain_name == "cultivo" else 1