WIDTH = 80
HEIGHT = 72

TILE_TYPES = {
    0: "pasto",
    1: "agua",
    2: "acantilado",
    3: "edificio",
    4: "cultivo",
    5: "puente",
    6: "puerta"
}

MAP_DATA = []

for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        if x < 2 or x > WIDTH-3 or y < 2 or y > HEIGHT-3:
            row.append(2)
        elif 10 <= x <= 18 and y == 15:
            row.append(6)
        elif 55 <= x <= 65 and y == 18:
            row.append(6)
        elif 8 <= x <= 20 and y == 58:
            row.append(6)
        elif 10 <= x <= 18 and 8 <= y <= 14:
            row.append(3)
        elif 55 <= x <= 65 and 10 <= y <= 17:
            row.append(3)
        elif 8 <= x <= 20 and 45 <= y <= 57:
            row.append(3)
        elif (37 <= x <= 42) and (12 <= y <= 14):
            row.append(5)
        elif (39 <= x <= 40) and (30 <= y <= 35):
            row.append(5)
        elif (55 <= x <= 57) and (50 <= y <= 55):
            row.append(5)
        elif (39 <= x <= 40 and 32 <= y <= 33):
            row.append(5)
        elif (39 <= x <= 40 and 52 <= y <= 53):
            row.append(5)
        elif (28 <= x <= 29 and 32 <= y <= 33):
            row.append(5)
        elif 37 <= x <= 42:
            row.append(1)
        elif 30 <= y <= 35 and 20 <= x <= 60:
            row.append(1)
        elif 50 <= y <= 55 and 40 <= x <= 75:
            row.append(1)
        elif 45 <= x <= 75 and 35 <= y <= 60:
            row.append(4)
        elif 20 <= x <= 30 and 38 <= y <= 65:
            row.append(4)
        else:
            row.append(0)
    MAP_DATA.append(row)


class FarmGrid:
    def __init__(self, grid):
        self.grid = grid

    def get_neighbors(self, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                node = self.grid[ny][nx]
                if node.walkable:
                    neighbors.append(node)
        return neighbors

    def get_cost(self, x, y):
        return self.grid[y][x].cost