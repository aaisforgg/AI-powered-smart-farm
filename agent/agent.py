from collections import deque
from math import dist
import random

from agent.strategies import StrategyManager
from core import state
from core.constants import REST_TICKS_MAX
from core.debug import debug_tick
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
        self._spawn_x = x
        self._spawn_y = y
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
        self.energy_threshold = self.genes.energy_max * self.genes.risk_tolerance
        self.energy_recovery = 4.0
        self.resting = False
        self.rest_ticks = 0
        self._rest_start_energy = 0.0

        self.evolution = EvolutionEngine()

        self.debug = False

        self.life_stats = {
            "harvests":       0,
            "steps":          0,
            "energy_on_rest": None,
            "starved":        False
        }

        self.memory = {
            "visited_tiles":  set(),
            "known_walkable": set(),
            "known_blocked":  set(),
            "known_crops":    {},
            "home_tiles":     set(),
            "episodes":       deque(maxlen=50),
            "last_actions":   deque(maxlen=10)
        }

    def reset_life_stats(self):
        self.life_stats = {
            "harvests":       0,
            "steps":          0,
            "energy_on_rest": None,
            "starved":        False
        }

    # ── LOOP PRINCIPAL ──────────────────────────────────────────────────────

    def update(self, state):
        tile = state.grid[self.y][self.x]

        # DESCANSO EN CASA
        if self._handle_resting(state, tile):
            return

        # Si resting=True pero no estamos en casa, ir a casa y nada más
        if self.resting:
            if self.current_path:
                self._follow_current_path(state)
            else:
                if self.memory["home_tiles"]:
                    hx, hy = next(iter(self.memory["home_tiles"]))
                    path = self.pathfinder.find_path(self.x, self.y, hx, hy, state.grid)
                    if path:
                        path = self._centralize_path(path, state.grid)
                        self.current_path = deque(path[1:])
            return

        # MEMORIA
        self._update_memory(state, tile)
        self._sync_known_crops(state)

        if self._handle_no_crops_go_home(state):
            return

        if self._handle_low_energy(state):
            return

        if self.needs_replan:
            self._reset_goal()

        if not self.goal:
            self._make_decision(state)

        if self._try_execute_adjacent(state):
            return

        if self._follow_current_path(state):
            return

        self._explore_or_wander(state)

        if self.debug:
            debug_tick(state, self)

    # ── SUB-MÉTODOS DE update() ─────────────────────────────────────────────

    def _handle_resting(self, state, tile):
        """Gestiona el descanso en casa. Retorna True si el agente está descansando."""
        if not (self.resting and tile.type_name == "casa"):
            return False

        # Registrar energía al inicio del descanso
        if self.life_stats["energy_on_rest"] is None:
            self.life_stats["energy_on_rest"] = self.energy
            self._rest_start_energy = self.energy

        # Recuperación lineal: de energía inicial → max_energy en REST_TICKS_MAX ticks
        recovery_per_tick = (self.max_energy - self._rest_start_energy) / REST_TICKS_MAX
        self.energy = min(self.max_energy, self.energy + recovery_per_tick)
        self.rest_ticks += 1

        day = (self.rest_ticks - 1) // (REST_TICKS_MAX // 3) + 1
        print(f"[Agent] Descansando día {day}/3 — tick {self.rest_ticks}/{REST_TICKS_MAX} "
              f"— energía {self.energy:.1f}/{self.max_energy:.0f}")

        if self.rest_ticks >= REST_TICKS_MAX:
            self.energy = self.max_energy
            self.resting = False
            self.rest_ticks = 0
            self._rest_start_energy = 0.0
            print("[Agent] Descanso de 3 días completado. Volviendo al trabajo")

            self.evolution.end_life(self)
            print(f"[Agent] Generación {self.evolution.generation} | "
                  f"Mejor fitness histórico: {self.evolution.best_fitness:.2f}")

            self._reset_for_new_life(state)

        return True

    def _update_memory(self, state, tile):
        """Registra posición actual y crops visibles en memoria."""
        self.memory["visited_tiles"].add((self.x, self.y))
        if tile.walkable:
            self.memory["known_walkable"].add((self.x, self.y))
        else:
            self.memory["known_blocked"].add((self.x, self.y))
        if tile.type_name == "casa":
            self.memory["home_tiles"].add((self.x, self.y))

        for crop in state.crops:
            dx = abs(crop.x - self.x)
            dy = abs(crop.y - self.y)
            if dx + dy <= self.genes.vision_radius:
                self.memory["known_crops"][crop.pos] = crop

    def _sync_known_crops(self, state):
        """Elimina de known_crops los crops destruidos por eventos (Fix B)."""
        stale_keys = [pos for pos in self.memory["known_crops"]
                      if self.memory["known_crops"][pos] not in state.crops]
        for key in stale_keys:
            del self.memory["known_crops"][key]

    def _handle_no_crops_go_home(self, state):
        """Si no hay cultivos y hay inventario, ir a casa. Retorna True si redirigió."""
        if self.memory["known_crops"] or not state.farmer_inventory or self.current_path:
            return False

        if not self.memory["home_tiles"]:
            return False

        hx, hy = next(iter(self.memory["home_tiles"]))
        print("[Agent] No hay cultivos → regresando a casa a descargar")

        self.goal = None
        self.strategy = None
        self.current_path.clear()

        path = self.pathfinder.find_path(self.x, self.y, hx, hy, state.grid)
        if path:
            path = self._centralize_path(path, state.grid)
            self.current_path = deque(path[1:])
            self.resting = True

        return True

    def _handle_low_energy(self, state):
        if self.energy > self.energy_threshold or self.resting:
            return False

        if self.memory["home_tiles"]:
            hx, hy = next(iter(self.memory["home_tiles"]))
            print("[Agent] Energia baja → volviendo a casa")
            self.goal = None        # ← limpiar goal
            self.strategy = None    # ← limpiar strategy
            self.current_path.clear()
            path = self.pathfinder.find_path(self.x, self.y, hx, hy, state.grid)
            if path:
                path = self._centralize_path(path, state.grid)
                self.current_path = deque(path[1:])
                self.resting = True
        else:
            self.energy = min(self.energy + self.genes.rest_efficiency, self.max_energy)
            print("[Agent] Sin casa conocida — recuperando energía lentamente")

        return True

    def _make_decision(self, state):
        """Decide goal y calcula path hacia él."""
        self.goal, self.strategy = self.decision_system.decide(state, self)
        if not self.goal:
            reason = self.decision_system.goal_manager.last_reject_reason
            known = list(self.memory["known_crops"].keys())
            print(f"[Agent] Sin goal — razón: {reason} | crops conocidos: {known}")

        if not self.goal:
            return

        gx, gy = self.goal.pos
        path = self.pathfinder.find_path(self.x, self.y, gx, gy, state.grid)
        if path:
            path = self._centralize_path(path, state.grid)
            self.current_path = deque(path[1:])
            print(f"[Agent] Ruta calculada a {self.goal.pos} — {len(self.current_path)} pasos")
        else:
            print(f"[Agent] Sin ruta a {self.goal.pos}")
            self.goal = None
            self.strategy = None
            self.needs_replan = False

    def _try_execute_adjacent(self, state):
        """Si hay goal sin path y estamos adyacentes, ejecutar. Retorna True si actuó."""
        if not self.goal or self.current_path:
            return False

        gx, gy = self.goal.pos
        if abs(self.x - gx) + abs(self.y - gy) <= 1:
            self._execute_strategy(state)
            self._reset_goal()
            return True

        return False

    def _follow_current_path(self, state):
        """Avanza por el path actual. Retorna True si había path."""
        if not self.current_path:
            return False

        self.movement.follow_path(self)
        self.life_stats["steps"] += 1

        tile = state.grid[self.y][self.x]

        move_cost = tile.cost * self.genes.energy_consumption
        move_multiplier = state.active_effects.get("movement_cost_multiplier", 1.0)
        move_cost *= move_multiplier

        energy_drain = state.active_effects.get("energy_drain_per_tick", 0.0)
        self.energy -= (move_cost + energy_drain)

        if self.energy <= 0:
            self.energy = 0
            self.life_stats["starved"] = True

        if not self.current_path and self.goal:
            gx, gy = self.goal.pos
            dist = abs(self.x - gx) + abs(self.y - gy)
            print(f"[Agent] Llegué al final del path. Pos=({self.x},{self.y}) Goal={self.goal.pos} dist={dist}")
            if self.debug:
                print(f"[PATH_END] llegué a ({self.x},{self.y}), goal en {self.goal.pos}, dist={dist}")
            if dist <= 1:
                self._execute_strategy(state)
                self._reset_goal()
            else:
                # Path agotado pero no llegamos al goal — replanificar
                print(f"[Agent] Path exhausto con dist={dist} > 1, forzando replan")
                self.needs_replan = True

        return True

    def _explore_or_wander(self, state):
        """Busca zona no explorada o hace exploración local."""
        target = self._find_unvisited_target(state.grid)

        if target:
            tx, ty = target
            path = self.pathfinder.find_path(self.x, self.y, tx, ty, state.grid)
            if path:
                path = self._centralize_path(path, state.grid)
                self.current_path = deque(path[1:])
                return

        self.movement.explore(self, state.grid)

    # ── ESTRATEGIA ──────────────────────────────────────────────────────────

    def _execute_strategy(self, state):
        """Ejecuta la acción planeada sobre el goal (crop o animal)."""
        if not self.goal or not self.strategy:
            return

        goal = self.goal
        is_animal = self.strategy in ("FEED", "COLLECT")

        # Guard: verificar que el objetivo sigue existiendo
        if is_animal:
            if goal not in state.animals:
                return
        elif self.strategy != "HARVEST":
            if goal not in state.crops:
                if goal.pos in self.memory["known_crops"]:
                    del self.memory["known_crops"][goal.pos]
                return

        self.memory["episodes"].append({
            "pos": (self.x, self.y),
            "action": self.strategy,
            "target": goal.pos
        })
        self.memory["last_actions"].append((self.strategy, goal.pos))

        # Actualizar dirección visual hacia el objetivo
        if hasattr(goal, 'x') and hasattr(goal, 'y'):
            dx = goal.x - self.x
            dy = goal.y - self.y
            if abs(dx) >= abs(dy):
                self.dir = (1 if dx > 0 else -1, 0)
            elif dy != 0:
                self.dir = (0, 1 if dy > 0 else -1)

        if is_animal:
            print(f"[Agent] Ejecutando '{self.strategy}' en {goal.pos} ({goal.especie})")
        else:
            print(f"[Agent] Ejecutando '{self.strategy}' en {goal.pos} | "
                  f"humedad={goal.humedad:.1f} fase={goal.fase}")
        if self.debug:
            d = abs(self.x - goal.x) + abs(self.y - goal.y)
            print(f"[EXECUTE] strategy={self.strategy} en pos={goal.pos} dist={d}")

        if self.strategy == "WATER":
            goal.humedad = min(100.0, goal.humedad + self.genes.water_efficiency)

        elif self.strategy == "PLANT":
            goal.fase = 1

        elif self.strategy == "HARVEST":
            if goal not in state.crops:
                if goal.pos in self.memory["known_crops"]:
                    del self.memory["known_crops"][goal.pos]
                return
            harvest_bonus = state.active_effects.get("harvest_bonus", 1)
            valor = goal.valor * harvest_bonus
            state.farmer_inventory.append(("crop", goal.pos, goal.tipo, valor))
            state.crops.remove(goal)
            self.life_stats["harvests"] += 1
            self.life_stats["harvest_value"] = self.life_stats.get("harvest_value", 0) + valor
            state.score += valor
            print(f"[Agent] Cosechado {goal.tipo} en {goal.pos} (valor={valor})")
            if goal.pos in self.memory["known_crops"]:
                del self.memory["known_crops"][goal.pos]

        elif self.strategy == "FEED":
            goal.alimentar()
            print(f"[Agent] Alimentado {goal.especie} en {goal.pos}")

        elif self.strategy == "COLLECT":
            producto = goal.recoger_producto()
            if producto:
                nombre, valor = producto
                state.farmer_inventory.append(("animal_product", goal.pos, nombre, valor))
                self.life_stats["harvests"] += 1
                self.life_stats["harvest_value"] = self.life_stats.get("harvest_value", 0) + valor
                state.score += valor
                print(f"[Agent] Recogido {nombre} de {goal.especie} (valor={valor})")

    # ── PATH HELPERS ────────────────────────────────────────────────────────

    def _centralize_path(self, path, grid):
        """Ajusta el path para alejarse de obstáculos SIN crear diagonales.

        Si en cualquier paso no se puede ajustar manteniendo adyacencia
        cardinal con el nodo previo ajustado, devuelve el path original
        intacto — garantizando que follow_path nunca encuentre un salto > 1.
        """
        if not path:
            return path

        rows = len(grid)
        cols = len(grid[0])

        new_path = [path[0]]

        for i in range(1, len(path)):
            x, y = path[i]
            prev = new_path[-1]

            best = None
            best_score = -999

            for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx = x + dx
                ny = y + dy

                if not (0 <= nx < cols and 0 <= ny < rows):
                    continue
                if not grid[ny][nx].walkable:
                    continue

                distancia_al_previo = abs(nx - prev[0]) + abs(ny - prev[1])
                if distancia_al_previo != 1:
                    continue

                score = 0
                for ax, ay in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
                    ox, oy = nx + ax, ny + ay
                    if 0 <= ox < cols and 0 <= oy < rows:
                        if not grid[oy][ox].walkable:
                            score -= 2
                        else:
                            score += 1

                if score > best_score:
                    best_score = score
                    best = (nx, ny)

            if best is not None:
                new_path.append(best)
            else:
                # Ajuste previo causó cascada — el nodo original ya no es
                # adyacente al prev ajustado. Devolver path original intacto.
                return path

        # Validación final: confirmar que todos los pasos son cardinales
        for i in range(1, len(new_path)):
            if abs(new_path[i][0] - new_path[i-1][0]) + abs(new_path[i][1] - new_path[i-1][1]) != 1:
                return path

        return new_path

    def _find_unvisited_target(self, grid):
        """Fix C: muestreo aleatorio O(50) en lugar de iterar todo el grid O(5200)."""
        rows = len(grid)
        cols = len(grid[0])

        for _ in range(50):
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            if grid[y][x].walkable and (x, y) not in self.memory["visited_tiles"]:
                return (x, y)

        return None

    # ── CICLO DE VIDA ───────────────────────────────────────────────────────

    def _reset_for_new_life(self, state):
        if self.memory["home_tiles"]:
            hx, hy = next(iter(self.memory["home_tiles"]))
            self.x = hx
            self.y = hy
        else:
            self.x = self._spawn_x
            self.y = self._spawn_y

        self.goal = None
        self.strategy = None
        self.current_path = deque()
        self.needs_replan = False
        self.resting = False
        self.rest_ticks = 0
        self._rest_start_energy = 0.0

        self.memory = {
            "visited_tiles":  set(),
            "known_walkable": set(),
            "known_blocked":  set(),
            "known_crops":    {},
            "home_tiles":     set(),
            "episodes":       deque(maxlen=50),
            "last_actions":   deque(maxlen=10)
        }

        # Reinyectar casas — el agente ya las conoce de la vida anterior
        for fila in state.grid:
            for nodo in fila:
                if nodo.type_name == "casa":
                    self.memory["home_tiles"].add((nodo.x, nodo.y))

        if self._crop_factory:
            state.crops = self._crop_factory(state.grid)
        state.farmer_inventory = []
        state.generation = self.evolution.generation

    def _reset_goal(self):
        self.goal = None
        self.strategy = None
        self.current_path = deque()
        self.needs_replan = False

    def interrupt(self):
        self.needs_replan = True
