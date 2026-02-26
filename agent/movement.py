class Movement:
    def __init__(self, game_map, width, height):
        self.game_map = game_map
        self.width = width
        self.height = height

    def can_move(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.game_map[y][x]
            return tile != 2 and tile != 3  # bloquea agua y pared
        return False