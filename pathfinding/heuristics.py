from pathfinding.base import HeuristicStrategy
import math

class ManhattanHeuristic(HeuristicStrategy):
    """
        Distancia Manhattan: suma de diferencias absolutas en x e y.
        Ideal para grids donde solo puedes moverte en 4 direcciones (arriba, abajo, izq, der).
    """
    
    def calculate(self, ax: int, ay: int, bx: int, by: int) -> float:
        return abs(ax - bx) + abs(ay - by)
    
class EuclideanHeuristic(HeuristicStrategy):
    """
        Distancia Euclidiana: línea recta entre dos puntos.
        Ideal si el agente puede moverse en 8 direcciones (incluye diagonales).
    """

    def calculate(self, ax: int, ay: int, bx: int, by: int) -> float:
        return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)