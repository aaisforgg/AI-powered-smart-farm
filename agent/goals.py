#goals.py
class GoalManager:

    def choose_goal(self, grid):
        dry_crops = []
        empty_tiles = []

        for y in range(72):
            for x in range(80):

                if grid[y][x] == 2:
                    dry_crops.append((x, y))

                elif grid[y][x] == 0:
                    empty_tiles.append((x, y))

        if dry_crops:
            return min(dry_crops, key=lambda pos: abs(pos[0]) + abs(pos[1]))

        if empty_tiles:
            return min(empty_tiles, key=lambda pos: abs(pos[0]) + abs(pos[1]))

        return None