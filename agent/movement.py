import random


class Movement:

    def follow_path(self, agent):

        if agent.current_path:

            nx, ny = agent.current_path.popleft()

            agent.x = nx
            agent.y = ny

    def explore(self, agent, grid):

        rows = len(grid)
        cols = len(grid[0])

        directions = [
            agent.dir,        # seguir igual
            (1,0),(-1,0),(0,1),(0,-1)
        ]

        # quitar duplicados
        directions = list(dict.fromkeys(directions))

        # aleatoriedad controlada por el gen exploration_rate
        exploration_rate = getattr(agent.genes, 'exploration_rate', 0.3)
        if random.random() < exploration_rate:
            random.shuffle(directions)

# ---------- Buscar tiles no visitados ----------
        for dx, dy in directions:

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < cols and 0 <= ny < rows:

                if not grid[ny][nx].walkable:
                    continue

                if (nx, ny) in agent.memory["visited_tiles"]:
                    continue

                agent.x = nx
                agent.y = ny

                agent.dir = (dx, dy)

                return
            
    # ---------- Si todo fue visitado ----------
        for dx, dy in directions:

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < cols and 0 <= ny < rows:

                if not grid[ny][nx].walkable:
                    continue

                agent.x = nx
                agent.y = ny
                agent.dir = (dx, dy)

                return