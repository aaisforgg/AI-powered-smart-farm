# farm_grid.py

from dataclasses import dataclass

@dataclass
class Node:
    x: int
    y: int
    walkable: bool
    cost: float
    entity: str

# 1. Definimos la configuración física basada en tus TILE_TYPES
# Aquí es donde integramos el multiplicador de costo (agua x3, etc.)
TILE_CONFIG = {
    0: {"name": "pasto",      "walkable": True,  "cost": 1.0},
    1: {"name": "agua",       "walkable": False, "cost": 3.0}, # Multiplicador 3.0
    2: {"name": "acantilado", "walkable": False, "cost": float('inf')},
    3: {"name": "edificio",   "walkable": False, "cost": float('inf')},
    4: {"name": "cultivo",    "walkable": True,  "cost": 1.5},
    5: {"name": "puente",     "walkable": True,  "cost": 1.0}
}

WIDTH = 80
HEIGHT = 72

def generate_farm_grid():
    grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # --- AQUÍ VA TU LÓGICA DE DISEÑO EXACTA ---
            tile_id = 0
            if x < 2 or x > WIDTH-3 or y < 2 or y > HEIGHT-3:
                tile_id = 2
            elif 37 <= x <= 42 or (30 <= y <= 35 and 20 <= x <= 60) or (50 <= y <= 55 and 40 <= x <= 75):
                tile_id = 1
            
            # Puentes sobreescriben agua
            if (39 <= x <= 40 and 32 <= y <= 33) or (39 <= x <= 40 and 52 <= y <= 53) or (28 <= x <= 29 and 32 <= y <= 33):
                tile_id = 5
            elif (10 <= x <= 18 and 8 <= y <= 15) or (55 <= x <= 65 and 10 <= y <= 18) or (8 <= x <= 20 and 45 <= y <= 58):
                tile_id = 3
            elif (45 <= x <= 75 and 35 <= y <= 60) or (20 <= x <= 30 and 38 <= y <= 65):
                tile_id = 4

            # --- CONVERSIÓN A NODO PROFESIONAL ---
            # En lugar de guardar un número, guardamos el objeto que la IA entiende
            conf = TILE_CONFIG[tile_id]
            row.append(Node(
                x=x, 
                y=y, 
                walkable=conf["walkable"], 
                cost=conf["cost"], 
                entity=conf["name"]
            ))
        grid.append(row)
    return grid

# Para cumplir con el reporte, el acceso al costo queda aquí:
def get_cost(grid, x, y):
    return grid[x][y].cost


"""
 TILE_TYPES = {
    0: "pasto",
    1: "agua",
    2: "acantilado",
    3: "edificio",
    4: "cultivo",
    5: "puente"
}

MAP_DATA = []

for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):

        # --- BORDES ACANTILADO ---
        if x < 2 or x > WIDTH-3 or y < 2 or y > HEIGHT-3:
            row.append(2)

        # --- RÍO EN FORMA DE S ---
        elif 37 <= x <= 42:
            row.append(1)

        elif 30 <= y <= 35 and 20 <= x <= 60:
            row.append(1)

        elif 50 <= y <= 55 and 40 <= x <= 75:
            row.append(1)

        # --- PUENTES ---
        elif (39 <= x <= 40 and 32 <= y <= 33):
            row.append(5)

        elif (39 <= x <= 40 and 52 <= y <= 53):
            row.append(5)

        elif (28 <= x <= 29 and 32 <= y <= 33):
            row.append(5)

        # --- INVERNADERO (arriba izquierda) ---
        elif 10 <= x <= 18 and 8 <= y <= 15:
            row.append(3)

        # --- CASA (arriba derecha) ---
        elif 55 <= x <= 65 and 10 <= y <= 18:
            row.append(3)

        # --- GRANERO (abajo izquierda) ---
        elif 8 <= x <= 20 and 45 <= y <= 58:
            row.append(3)

        # --- CULTIVO GRANDE CENTRAL DERECHA ---
        elif 45 <= x <= 75 and 35 <= y <= 60:
            row.append(4)

        # --- CULTIVO VERTICAL CENTRAL IZQUIERDA ---
        elif 20 <= x <= 30 and 38 <= y <= 65:
            row.append(4)

        else:
            row.append(0)

    MAP_DATA.append(row)"""
