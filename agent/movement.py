import random

class Movement:

    BLOCKED_TILES = [1, 2, 3]

    def follow_path(self, agent):
        if agent.current_path:
            nx, ny = agent.current_path.popleft()
            agent.x = nx
            agent.y = ny

    def move_towards(self, agent, grid, goal):
        if not goal:
            return False

        goal_x, goal_y = goal
        dx = goal_x - agent.x
        dy = goal_y - agent.y
        move_x = 0
        move_y = 0

        if dx != 0:
            move_x = int(dx / abs(dx))
        elif dy != 0:
            move_y = int(dy / abs(dy))

        new_x = agent.x + move_x
        new_y = agent.y + move_y

        if 0 <= new_x < 80 and 0 <= new_y < 72:
            tile = grid[new_y][new_x]
            if tile in self.BLOCKED_TILES:
                return self.change_direction(agent, grid)
            agent.x = new_x
            agent.y = new_y
            return True

        return False

    def change_direction(self, agent, grid):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < 80 and 0 <= ny < 72:
                if grid[ny][nx] not in self.BLOCKED_TILES:
                    agent.x = nx
                    agent.y = ny
                    return True

        return False

    def random_move(self, agent, grid):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < 80 and 0 <= ny < 72:
                if grid[ny][nx] not in self.BLOCKED_TILES:
                    agent.x = nx
                    agent.y = ny
                    return