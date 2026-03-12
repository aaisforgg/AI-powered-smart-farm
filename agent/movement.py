import random


class Movement:

    def follow_path(self, agent):

        if agent.current_path:

            nx, ny = agent.current_path.popleft()

            agent.x = nx
            agent.y = ny

    def explore(self, agent, grid):

        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        random.shuffle(directions)

        # buscar tiles no visitados

        for dx, dy in directions:

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < 80 and 0 <= ny < 72:

                if not grid[ny][nx].walkable:
                    continue

                if (nx,ny) not in agent.memory["visited_tiles"]:

                    agent.x = nx
                    agent.y = ny
                    return

        # si todo fue visitado moverse normal

        for dx, dy in directions:

            nx = agent.x + dx
            ny = agent.y + dy

            if 0 <= nx < 80 and 0 <= ny < 72:

                if grid[ny][nx].walkable:

                    agent.x = nx
                    agent.y = ny
                    return