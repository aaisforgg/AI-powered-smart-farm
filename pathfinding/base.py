from abc import ABC, abstractmethod
from typing import Optional

class HeuristicStrategy(ABC):
    """
        Contrato para cualqiuer heuristica de estimacion de distancia.
    """
    
    @abstractmethod
    def calculate(self, ax: int, ay: int, bx: int, by: int) -> float:
        """
            Estima el costo de ir del punto (ax, ay) al punto (bx, by).
        """
        ...
    
class Pathfinder(ABC):
    """
        Contrato para cualqiuer algoritmo de busqueda de rutas.
    """
    
    @abstractmethod
    def find_path(
        self, 
        start_x: int,
        start_y: int,
        goal_x: int,
        goal_y: int, 
        grid: list[list],
    ) -> Optional[list[tuple[int, int]]]:
        """
            Busca una ruta desde start hasta goal dentro del grid.
            Devuelve lista de (x, y) y si encuentra ruta, None si no existe.
        """
        ...