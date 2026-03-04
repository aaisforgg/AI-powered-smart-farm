#strategies.py
class StrategyManager:

    def choose_strategy(self, grid, goal):
        if not goal:
            return None

        x, y = goal

        if grid[y][x] == 2:
            return "WATER"

        if grid[y][x] == 0:
            return "PLANT"

        return None