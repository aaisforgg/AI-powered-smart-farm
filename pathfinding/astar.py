import heapq
from typing import Optional
from pathfinding.base import Pathfinder, HeuristicStrategy
from pathfinding.heuristics import ManhattanHeuristic

class AStarPathfinder(Pathfinder):
    """
    Implementación de A* para grids 2D.
    Recibe cualquier heurística — por defecto usa Manhattan.
    """
    
    def __init__(self, heuristic: Optional[HeuristicStrategy] = None):
        self.heuristic = heuristic or ManhattanHeuristic()

    def find_path(
        self, 
        start_x: int,
        start_y: int,
        goal_x: int,
        goal_y: int, 
        grid: list[list],
    ) -> Optional[list[tuple[int, int]]]:
        
        # En una lista de listas, rows es la altura (y) y cols el ancho (x)
        rows = len(grid)
        cols = len(grid[0])
        
        open_heap = []
        # El heap guarda (f_cost, x, y)
        heapq.heappush(open_heap, (0, start_x, start_y))
        
        came_from: dict[tuple, Optional[tuple]] = {(start_x, start_y): None}
        g_cost: dict[tuple, float] = {(start_x, start_y): 0}
        
        while open_heap:
            _, cx, cy = heapq.heappop(open_heap)
            
            # Si llegamos a la meta
            if (cx, cy) == (goal_x, goal_y):
                return self._reconstruct_path(came_from, goal_x, goal_y)
            
            for nx, ny, step_cost in self._get_neighbors(cx, cy, rows, cols, grid):
                new_g = g_cost[(cx, cy)] + step_cost
                
                if (nx, ny) not in g_cost or new_g < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = new_g
                    
                    h = self.heuristic.calculate(nx, ny, goal_x, goal_y)
                    f = new_g + h
                    
                    heapq.heappush(open_heap, (f, nx, ny))
                    came_from[(nx, ny)] = (cx, cy)
        
        return None
    
    def _get_neighbors(
        self, x: int, y: int, rows: int, cols: int, grid: list[list]
    ) -> list[tuple[int, int, float]]:
        """
        Devuelve vecinos válidos como (x, y, costo).
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Verificamos límites: nx debe estar en cols (ancho) y ny en rows (alto)
            if 0 <= nx < cols and 0 <= ny < rows:
                # Obtenemos el nodo del grid
                node = grid[ny][nx]
                
                # Verificamos si es caminable usando el atributo del objeto Node
                if node.walkable:
                    # Usamos el costo del nodo si existe, si no, por defecto 1.0
                    cost = getattr(node, 'cost', 1.0)
                    neighbors.append((nx, ny, cost))
                    
        return neighbors
    
    def _reconstruct_path(
        self,
        came_from: dict,
        goal_x: int, 
        goal_y: int,
    ) -> list[tuple[int, int]]:
        """
        Reconstruye la ruta de atrás hacia adelante. 
        """
        path = []
        current = (goal_x, goal_y)
        
        while current is not None:
            path.append(current)
            current = came_from.get(current)
            
        path.reverse()
        return path