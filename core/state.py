from dataclasses import dataclass, field


@dataclass
class GameState:
    farmer_pos: tuple[int, int] = (0, 0)
    farmer_energy: float = 100.0
    farmer_inventory: list = field(default_factory=list)
    grid: list[list] = field(default_factory=list)
    crops: list = field(default_factory=list)
    animals: list = field(default_factory=list)
    score: int = 0
    season: str = "Primavera"
    tick: int = 0
    generation: int = 0
    best_fitness: float = 0.0

    # --- Efectos globales (escritos por EventManager, leídos por Agent) ---
    # Ejemplos: {"movement_cost_multiplier": 3, "energy_drain_per_tick": 2}
    active_effects: dict = field(default_factory=dict)
    # Obstáculos temporales generados por eventos [(x, y, tipo_obstaculo)]
    temp_obstacles: list = field(default_factory=list)
    # Obstáculos ambientales persistentes por estación [(x, y, tipo_obstaculo)]
    seasonal_obstacles: list = field(default_factory=list)

    # --- Referencias opacas (se inyectan en main.py, Pipeline las usa) ---
    # Son `object` a propósito: core/ no conoce los tipos reales
    _agent_ref: object = None
    _season_mgr: object = None
    _event_mgr: object = None