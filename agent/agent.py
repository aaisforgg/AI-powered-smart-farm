from collections import deque
from .decision import DecisionSystem
from .movement import Movement
from pathfinding.astar import AStarPathfinder
from .genetics import Genes

class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.goal = None
        self.strategy = None

        self.current_path = deque()
        self.needs_replan = False

        self.decision_system = DecisionSystem()
        self.movement = Movement()
        self.pathfinder = AStarPathfinder()

        self.genes = Genes()

        self.energy = self.genes.energy_max
        self.max_energy = self.genes.energy_max
        self.energy_threshold = 25.0
        self.energy_recovery = 4.0
        self.resting = False

        self.memory = {
            "visited_tiles": set(),
            "known_walkable": set(),
            "known_blocked": set(),
            "known_crops": {},
            "home_tiles": set(),
            "episodes": deque(maxlen=50),
            "last_actions": deque(maxlen=10)
        }

    def update(self, state):

        tile = state.grid[self.y][self.x]

        # DESCANSO EN CASA
        if self.resting and tile.type_name == "casa":
            self.energy += self.genes.rest_efficiency
            print(f"[Agent] Descansando... energia={self.energy:.1f}")
            if self.energy >= self.max_energy:
                self.energy = self.max_energy
                self.resting = False
                print("[Agent] Energia completa. Volviendo al trabajo")
            return

        # MEMORIA ESPACIAL
        self.memory["visited_tiles"].add((self.x, self.y))
        if tile.walkable:
            self.memory["known_walkable"].add((self.x, self.y))
        else:
            self.memory["known_blocked"].add((self.x, self.y))
        if tile.type_name == "casa":
            self.memory["home_tiles"].add((self.x, self.y))

        # MEMORIA DE RECURSOS
        for crop in state.crops:
            self.memory["known_crops"][crop.pos] = crop

        # ENERGIA BAJA → VOLVER A CASA
        if self.energy <= self.energy_threshold and not self.resting:
            if self.memory["home_tiles"]:
                hx, hy = next(iter(self.memory["home_tiles"]))
                print("[Agent] Energia baja → volviendo a casa")
                self.goal = None
                self.strategy = None
                self.current_path.clear()
                path = self.pathfinder.find_path(self.x, self.y, hx, hy, state.grid)
                if path:
                    self.current_path = deque(path[1:])
                    self.resting = True
                return

        # REPLAN
        if self.needs_replan:
            self._reset_goal()

        # DECISION
        if not self.goal:
            self.goal, self.strategy = self.decision_system.decide(state, self)
            if self.goal:
                gx, gy = self.goal.pos
                path = self.pathfinder.find_path(self.x, self.y, gx, gy, state.grid)
                if path:
                    self.current_path = deque(path[1:])
                    print(f"[Agent] Ruta calculada a {self.goal.pos} — {len(self.current_path)} pasos")
                else:
                    print(f"[Agent] Sin ruta a {self.goal.pos}")
                    self._reset_goal()

        # MOVIMIENTO
        if self.current_path:
            self.movement.follow_path(self)

            tile = state.grid[self.y][self.x]
            self.energy -= tile.cost * self.genes.energy_consumption
            if self.energy < 0:
                self.energy = 0

            if not self.current_path and self.goal:
                gx, gy = self.goal.pos
                if (self.x, self.y) == (gx, gy):
                    self._execute_strategy(state)
                    self._reset_goal()
            return

        self.movement.explore(self, state.grid)

    def _execute_strategy(self, state):

        if not self.strategy or not self.goal:
            return

        crop = self.goal

        self.memory["episodes"].append({
            "pos": (self.x, self.y),
            "action": self.strategy,
            "target": crop.pos
        })
        self.memory["last_actions"].append((self.strategy, crop.pos))

        print(f"[Agent] Ejecutando '{self.strategy}' en {crop.pos} | humedad={crop.humedad:.1f} fase={crop.fase}")

        if self.strategy == "WATER":
            crop.humedad = min(100.0, crop.humedad + 50.0)

        elif self.strategy == "PLANT":
            crop.fase = 1

        elif self.strategy == "HARVEST":
            state.farmer_inventory.append(("crop", crop.pos))
            state.crops.remove(crop)
            print(f"[Agent] Cosechado {crop.pos} | inventario: {len(state.farmer_inventory)}")
            if crop.pos in self.memory["known_crops"]:
                del self.memory["known_crops"][crop.pos]

    def _reset_goal(self):
        self.goal = None
        self.strategy = None
        self.current_path = deque()
        self.needs_replan = False

    def interrupt(self):
        self.needs_replan = True