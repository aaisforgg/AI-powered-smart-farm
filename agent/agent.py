from collections import deque
from .decision import DecisionSystem
from .movement import Movement
from pathfinding.astar import AStarPathfinder


class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.goal     = None   # objeto Crop
        self.strategy = None   # "WATER" | "PLANT" | "HARVEST"

        self.current_path = deque()  # deque de tuplas (x, y)
        self.needs_replan = False    # activado por eventos externos

        self.decision_system = DecisionSystem()
        self.movement        = Movement()
        self.pathfinder      = AStarPathfinder()   # usa ManhattanHeuristic por defecto

    # ------------------------------------------------------------------
    # UPDATE — llamar una vez por tick
    # ------------------------------------------------------------------
    def update(self, state):

        # Evento externo forzó replanning
        if self.needs_replan:
            self._reset_goal()

        # ── 1. Sin objetivo → decidir ──────────────────────────────────
        if not self.goal:
            self.goal, self.strategy = self.decision_system.decide(state, self)

            if self.goal:
                gx, gy = self.goal.pos

                path = self.pathfinder.find_path(
                    self.x, self.y,
                    gx, gy,
                    state.grid           # list[list[Node]]
                )

                if path:
                    # find_path incluye el nodo inicial → lo descartamos
                    self.current_path = deque(path[1:])
                else:
                    # A* no encontró camino → descartar objetivo
                    print(f"[Agent] Sin camino hacia {self.goal.pos}, descartando.")
                    self._reset_goal()

        # ── 2. Siguiendo ruta ──────────────────────────────────────────
        if self.current_path:
            self.movement.follow_path(self)
            return

        # ── 3. Ruta vacía → ¿llegué al destino? ───────────────────────
        if self.goal:
            gx, gy = self.goal.pos

            if (self.x, self.y) == (gx, gy):
                self._execute_strategy(state)
                self._reset_goal()
                return

            # Tengo goal, no hay ruta y no estoy en él → recalcular
            print("[Agent] Ruta perdida, recalculando...")
            path = self.pathfinder.find_path(self.x, self.y, gx, gy, state.grid)
            if path:
                self.current_path = deque(path[1:])
            else:
                self._reset_goal()

        # ── 4. Sin nada → movimiento aleatorio ────────────────────────
        else:
            self.movement.random_move(self, state.grid)

    # ------------------------------------------------------------------
    # Ejecutar acción al llegar al cultivo
    # ------------------------------------------------------------------
    def _execute_strategy(self, state):
        if not self.strategy or not self.goal:
            return

        crop = self.goal
        print(f"[Agent] '{self.strategy}' en cultivo {crop.pos} | "
              f"fase={crop.fase} humedad={crop.humedad:.1f}")

        if self.strategy == "WATER":
            crop.humedad = min(100.0, crop.humedad + 50.0)

        elif self.strategy == "PLANT":
            crop.fase = 1

        elif self.strategy == "HARVEST":
            state.farmer_inventory.append(("crop", crop.pos))
            state.crops.remove(crop)
            print(f"[Agent] Cosechado en {crop.pos} → inventario: {len(state.farmer_inventory)}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _reset_goal(self):
        self.goal         = None
        self.strategy     = None
        self.current_path = deque()
        self.needs_replan = False

    def interrupt(self):
        """Llamar desde el sistema de eventos para forzar replanning."""
        self.needs_replan = True