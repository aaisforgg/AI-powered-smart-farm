from collections import deque
from math import dist
import random

from agent.strategies import StrategyManager
from core import state
from entities import crop
from .decision import DecisionSystem
from .movement import Movement
from pathfinding.astar import AStarPathfinder
from .genetics import Genes
from .evolution import EvolutionEngine

class Agent:

    def __init__(self, x, y, crop_factory=None):
        self.x = x
        self.y = y
        # Guardar spawn para reiniciar cada vida
        self._spawn_x = x
        self._spawn_y = y
        # Función que genera cultivos nuevos al inicio de cada vida
        self._crop_factory = crop_factory

        self.dir = (0, 0)

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

        # Motor evolutivo
        self.evolution = EvolutionEngine()

        # Estadísticas de la vida actual (se resetean cada generación)
        self.life_stats = {
            "harvests":       0,
            "steps":          0,
            "energy_on_rest": None,
            "starved":        False
        }

        self.memory = {
            "visited_tiles": set(),
            "known_walkable": set(),
            "known_blocked": set(),
            "known_crops": {},
            "home_tiles": set(),
            "episodes": deque(maxlen=50),
            "last_actions": deque(maxlen=10)
        }

    def reset_life_stats(self):
        self.life_stats = {
            "harvests":       0,
            "steps":          0,
            "energy_on_rest": None,
            "starved":        False
        }

    def update(self, state):

        tile = state.grid[self.y][self.x]

        # DESCANSO EN CASA
        if self.resting and tile.type_name == "casa":
            # Registrar energía al llegar a casa (solo la primera vez)
            if self.life_stats["energy_on_rest"] is None:
                self.life_stats["energy_on_rest"] = self.energy

            self.energy += self.genes.rest_efficiency
            print(f"[Agent] Descansando... energia={self.energy:.1f}")

            if self.energy >= self.max_energy:
                self.energy = self.max_energy
                self.resting = False
                print("[Agent] Energia completa. Volviendo al trabajo")

                # ── FIN DE VIDA: evaluar y evolucionar ──
                self.evolution.end_life(self)
                print(f"[Agent] Generación {self.evolution.generation} | "
                      f"Mejor fitness histórico: {self.evolution.best_fitness:.2f}")

                # Reiniciar estado interno para la nueva vida
                self._reset_for_new_life(state)

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
            print(f"[Agent] Decisión → goal={self.goal} strategy={self.strategy}")
            print(f"[Agent] Crops conocidos: {list(self.memory['known_crops'].keys())}")
            if self.goal:
                gx, gy = self.goal.pos
                path = self.pathfinder.find_path(self.x, self.y, gx, gy, state.grid)
                if path:
                    path = self._centralize_path(path, state.grid)
                    self.current_path = deque(path[1:])
                    print(f"[Agent] Ruta calculada a {self.goal.pos} — {len(self.current_path)} pasos")
                else:
                    print(f"[Agent] Sin ruta a {self.goal.pos}")
                    self._reset_goal()
         
        if self.goal and not self.current_path:
            gx, gy = self.goal.pos
            dist = abs(self.x - gx) + abs(self.y - gy)
            if dist <= 1:
                self._execute_strategy(state)
                self._reset_goal()
                return

        # MOVIMIENTO
        if self.current_path:
            self.movement.follow_path(self)
            self.life_stats["steps"] += 1

            tile = state.grid[self.y][self.x]
            self.energy -= tile.cost * self.genes.energy_consumption
            if self.energy <= 0:
                self.energy = 0
                self.life_stats["starved"] = True

            if not self.current_path and self.goal:
                gx, gy = self.goal.pos
                dist = abs(self.x - gx) + abs(self.y - gy)
                print(f"[Agent] Llegué al final del path. Pos=({self.x},{self.y}) Goal={self.goal.pos} dist={dist}")
                if dist <= 1:
                    self._execute_strategy(state)
                    self._reset_goal()
            return

                # intentar ir a zona no explorada
        target = self._find_unvisited_target(state.grid)

        if target:

            tx, ty = target

            path = self.pathfinder.find_path(self.x, self.y, tx, ty, state.grid)

            if path:
                path = self._centralize_path(path, state.grid)
                self.current_path = deque(path[1:])
                return

        # si no hay zonas nuevas, explorar normal
        self.movement.explore(self, state.grid)

        if not self.current_path:
            self.movement.explore(self, state.grid)

    def _execute_strategy(self, state):

        if not self.goal:
            return

        crop = self.goal

        # Recalcular por si el estado del crop cambió desde que se planificó
        from .strategies import StrategyManager
        strategy = StrategyManager().choose_strategy(state, crop)
    
        if strategy is None:
            return

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
            self.life_stats["harvests"] += 1
            print(f"[Agent] Cosechado {crop.pos} | inventario: {len(state.farmer_inventory)}")
            if crop.pos in self.memory["known_crops"]:
                del self.memory["known_crops"][crop.pos]

    def _centralize_path(self, path, grid):

        if not path:
            return path

        rows = len(grid)
        cols = len(grid[0])

        new_path = []

        for x, y in path:

            best = (x, y)
            best_score = -999

            # revisar vecinos posibles (incluyendo quedarse en el mismo)
            for dx, dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:

                nx = x + dx
                ny = y + dy

                if not (0 <= nx < cols and 0 <= ny < rows):
                    continue

                if not grid[ny][nx].walkable:
                    continue

                # calcular distancia a obstáculos cercanos
                score = 0

                for ax, ay in [
                    (-1,0),(1,0),(0,-1),(0,1),
                    (-1,-1),(1,-1),(-1,1),(1,1)
                ]:
                    ox = nx + ax
                    oy = ny + ay

                    if 0 <= ox < cols and 0 <= oy < rows:
                        if not grid[oy][ox].walkable:
                            score -= 2
                        else:
                            score += 1

                if score > best_score:
                    best_score = score
                    best = (nx, ny)

            new_path.append(best)

        return new_path

    def _find_unvisited_target(self, grid):

        rows = len(grid)
        cols = len(grid[0])

        candidates = []

        for y in range(rows):
            for x in range(cols):

                if not grid[y][x].walkable:
                    continue

                if (x, y) not in self.memory["visited_tiles"]:
                    candidates.append((x, y))

        if not candidates:
            return None

        return random.choice(candidates)

    def _reset_for_new_life(self, state):
        """
        Reinicia todo lo necesario para empezar una nueva vida limpia.
        Se llama justo después de que end_life() muta los genes.
        """
        # Volver al spawn (posición inicial guardada)
        self.x = self._spawn_x
        self.y = self._spawn_y

        # Limpiar navegación
        self.goal = None
        self.strategy = None
        self.current_path = deque()
        self.needs_replan = False
        self.resting = False

        # Limpiar memoria (nueva vida = nueva exploración)
        self.memory = {
            "visited_tiles":  set(),
            "known_walkable": set(),
            "known_blocked":  set(),
            "known_crops":    {},
            "home_tiles":     set(),
            "episodes":       deque(maxlen=50),
            "last_actions":   deque(maxlen=10)
        }

        # Regenerar cultivos y limpiar inventario
        if self._crop_factory:
            state.crops = self._crop_factory()
        state.farmer_inventory = []
        state.generation = self.evolution.generation

    def _reset_goal(self):
        self.goal = None
        self.strategy = None
        self.current_path = deque()
        self.needs_replan = False

    def interrupt(self):
        self.needs_replan = True