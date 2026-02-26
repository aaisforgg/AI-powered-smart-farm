# farm_grid.py

WIDTH = 80
HEIGHT = 72

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

    MAP_DATA.append(row)