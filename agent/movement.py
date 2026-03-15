import random

class Movement:

    CARDINAL = [(1,0),(-1,0),(0,1),(0,-1)]

    def follow_path(self, agent):
        if agent.current_path:
            nx, ny = agent.current_path.popleft()
            if abs(nx - agent.x) + abs(ny - agent.y) != 1:
                agent.current_path.clear()
                return
            agent.x = nx
            agent.y = ny

    def explore(self, agent, grid):
        rows = len(grid)
        cols = len(grid[0])

        if agent.dir in self.CARDINAL:
            directions = [agent.dir] + self.CARDINAL
        else:
            directions = list(self.CARDINAL)

        directions = list(dict.fromkeys(directions))

        exploration_rate = getattr(agent.genes, 'exploration_rate', 0.3)
        if random.random() < exploration_rate:
            random.shuffle(directions)

        for dx, dy in directions:
            nx = agent.x + dx
            ny = agent.y + dy
            if not (0 <= nx < cols and 0 <= ny < rows):
                continue
            if not grid[ny][nx].walkable:
                continue
            if (nx, ny) in agent.memory["visited_tiles"]:
                continue
            agent.x = nx
            agent.y = ny
            agent.dir = (dx, dy)
            return

        for dx, dy in directions:
            nx = agent.x + dx
            ny = agent.y + dy
            if not (0 <= nx < cols and 0 <= ny < rows):
                continue
            if not grid[ny][nx].walkable:
                continue
            agent.x = nx
            agent.y = ny
            agent.dir = (dx, dy)
            return