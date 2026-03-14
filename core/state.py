from dataclasses import dataclass, field

@dataclass
class GameState:
    farmer_pos: tuple[int, int] = (0, 0)
    farmer_energy: float = 100.0
    farmer_inventory: list = field(default_factory=list)
    grid: list[list] = field(default_factory=list)
    crops: list = field(default_factory=list)
    animals: list = field(default_factory=list)
    season: str = 'spring'
    tick: int = 0
    generation: int = 0
    best_fitness: float = 0.0