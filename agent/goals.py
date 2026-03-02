class GoalManager:

    def choose_goal(self, grid, agent):
        crops = []

        for y in range(72):
            for x in range(80):
                if grid[y][x] == 4:
                    crops.append((x, y))

        if not crops:
            return None

        # Elegir el cultivo más cercano
        return min(crops, key=lambda pos: abs(pos[0] - agent.x) + abs(pos[1] - agent.y))