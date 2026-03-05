from dataclasses import dataclass, field

@dataclass
class GameState:
    # Ajustamos nombres a español para que el main.py no falle
    granjero_pos: tuple[int, int] = (0, 0)
    granjero_energia: float = 100.0
    granjero_inventario: list = field(default_factory=list)
    
    # Pedro: Limpiar comentario ""
    grid: list[list] = field(default_factory=list) 
    
    # Listas de entidades
    cultivos: list = field(default_factory=list)
    animales: list = field(default_factory=list)
    
    # Metadatos del mundo
    estacion: str = 'primavera'
    tick: int = 0

    def __post_init__(self):
        """
        Si el grid se pasa como una lista de strings (como en el main),
        aquí podrías convertirlo en objetos Node si fuera necesario.
        """
        if not self.grid:
            # Grid por defecto si no se proporciona uno
            self.grid = [["PASTO" for _ in range(5)] for _ in range(5)]