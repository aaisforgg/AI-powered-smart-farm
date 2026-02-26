# farm_grid.py

WIDTH = 80
HEIGHT = 72

TILE_TYPES = {
    0: "pasto",
    1: "agua",
    2: "acantilado",
    3: "edificio",
    4: "cultivo",
    5: "puente",
    6: "puerta"  # Transitable para entrar/salir de edificios
}

MAP_DATA = []

for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):

        # --- BORDES ACANTILADO ---
        if x < 2 or x > WIDTH-3 or y < 2 or y > HEIGHT-3:
            row.append(2)

        # --- PUERTAS (BASES DE EDIFICIOS COMPLETAS) ---
        # Prioridad alta para que el agente pueda salir/entrar libremente
        
        # Base del Invernadero (Toda la fila 15 entre X 10 y 18)
        elif 10 <= x <= 18 and y == 15:
            row.append(6)
            
        # Base de la Casa (Toda la fila 18 entre X 55 y 65)
        elif 55 <= x <= 65 and y == 18:
            row.append(6)
            
        # Base del Granero (Toda la fila 58 entre X 8 y 20)
        elif 8 <= x <= 20 and y == 58:
            row.append(6)

        # --- EDIFICIOS (PAREDES RESTANTES) ---
        elif 10 <= x <= 18 and 8 <= y <= 14: # Invernadero (8 al 14 son paredes)
            row.append(3)
        elif 55 <= x <= 65 and 10 <= y <= 17: # Casa (10 al 17 son paredes)
            row.append(3)
        elif 8 <= x <= 20 and 45 <= y <= 57: # Granero (45 al 57 son paredes)
            row.append(3)

        # --- PUENTES (Prioridad sobre el agua) ---
        elif (37 <= x <= 42) and (12 <= y <= 14): row.append(5)
        elif (39 <= x <= 40) and (30 <= y <= 35): row.append(5)
        elif (55 <= x <= 57) and (50 <= y <= 55): row.append(5)
        elif (39 <= x <= 40 and 32 <= y <= 33): row.append(5)
        elif (39 <= x <= 40 and 52 <= y <= 53): row.append(5)
        elif (28 <= x <= 29 and 32 <= y <= 33): row.append(5)

        # --- RÍO EN FORMA DE S ---
        elif 37 <= x <= 42:
            row.append(1)
        elif 30 <= y <= 35 and 20 <= x <= 60:
            row.append(1)
        elif 50 <= y <= 55 and 40 <= x <= 75:
            row.append(1)

        # --- CULTIVOS ---
        elif 45 <= x <= 75 and 35 <= y <= 60:
            row.append(4)
        elif 20 <= x <= 30 and 38 <= y <= 65:
            row.append(4)

        else:
            row.append(0)

    MAP_DATA.append(row)