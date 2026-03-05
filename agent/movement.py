import random
from collections import deque


class Movement:
    """
    Maneja el desplazamiento del agente en el grid.

    Convención de coordenadas (igual que AStarPathfinder):
        grid[x][y]  →  x = fila (primera dimensión = rows)
                        y = columna (segunda dimensión = cols)
    El agente guarda self.x, self.y con la misma convención.
    """

    def follow_path(self, agent):
        """
        Consume agent.current_path (deque) un nodo por tick.
        Retorna True si se movió, False si no había ruta.
        """
        path = getattr(agent, "current_path", None)
        if not path:
            return False

        try:
            next_node = path.popleft()   # O(1) con deque
        except IndexError:
            agent.current_path = deque()
            return False

        agent.x, agent.y = next_node
        return True

    def random_move(self, agent, grid):
        """
        Mueve al agente en una dirección aleatoria válida.
        Retorna True si se movió, False si está completamente bloqueado.
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        for dx, dy in directions:
            nx = agent.x + dx
            ny = agent.y + dy

            if self._is_walkable(nx, ny, grid, rows, cols):
                agent.x = nx
                agent.y = ny
                return True

        return False

    def _is_walkable(self, x, y, grid, rows, cols):
        """
        grid[x][y] — x=fila, y=columna. Node debe tener .walkable.
        """
        if not (0 <= x < rows and 0 <= y < cols):
            return False
        return grid[x][y].walkable