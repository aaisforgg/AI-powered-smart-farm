import heapq
from typing import Optional
from pathfinding.base import Pathfinder, HeuristicStrategy
from pathfinding.heuristics import ManhattanHeuristic

class AStarPathfinder(Pathfinder):
    
    def __init__(self, heuristic: Optional[HeuristicStrategy] = None):
        self.heuristic = heuristic or ManhattanHeuristic()

    def find_path(self, start_x, start_y, goal_x, goal_y, grid):
        rows = len(grid)
        cols = len(grid[0])
        
        open_heap = []
        heapq.heappush(open_heap, (0, start_x, start_y))
        
        came_from = {(start_x, start_y): None}
        g_cost = {(start_x, start_y): 0}
        
        while open_heap:
            _, cx, cy = heapq.heappop(open_heap)
            
            if (cx, cy) == (goal_x, goal_y):
                return self._reconstruct_path(came_from, goal_x, goal_y)
            
            for nx, ny, step_cost in self._get_neighbors(cx, cy, rows, cols, grid):
                new_g = g_cost[(cx, cy)] + step_cost
                
                if (nx, ny) not in g_cost or new_g < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = new_g
                    h = self.heuristic.calculate(nx, ny, goal_x, goal_y)
                    f = new_g + h * 1.001
                    heapq.heappush(open_heap, (f, nx, ny))
                    came_from[(nx, ny)] = (cx, cy)
        
        return None

    def _get_neighbors(self, x, y, rows, cols, grid):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                node = grid[ny][nx]
                if node.walkable:
                    wall_penalty = 0
                    for ax, ay in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
                        ox, oy = nx + ax, ny + ay
                        if 0 <= ox < cols and 0 <= oy < rows:
                            if not grid[oy][ox].walkable:
                                wall_penalty += 0.5
                    neighbors.append((nx, ny, node.cost + wall_penalty))
        return neighbors

    def _reconstruct_path(self, came_from, goal_x, goal_y):
        path = []
        current = (goal_x, goal_y)
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path