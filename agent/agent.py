from collections import deque
from .decision import DecisionSystem
from .movement import Movement
from pathfinding.astar import AStarPathfinder

REPLAN_INTERVAL = 5

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
    
    def update(self, state):
        if self.needs_replan:
            self._reset_goal()

        if self.goal and state.tick % REPLAN_INTERVAL == 0:
            mejor, _ = self.decision_system.decide(state, self)
            if mejor and mejor != self.goal:
                self._reset_goal()

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

        if self.current_path:
            self.movement.follow_path(self)
            if not self.current_path and self.goal:
                gx, gy = self.goal.pos
                if (self.x, self.y) == (gx, gy):
                    self._execute_strategy(state)
                    self._reset_goal()
            return
        
        self.movement.random_move(self, state.grid)

    def _execute_strategy(self, state):
        if not self.strategy or not self.goal:
            return
        crop = self.goal
        print(f"[Agent] Ejecutando '{self.strategy}' en {crop.pos} | humedad={crop.humedad:.1f} fase={crop.fase}")
        if self.strategy == "WATER":
            crop.humedad = min(100.0, crop.humedad + 50.0)
        elif self.strategy == "PLANT":
            crop.fase = 1
        elif self.strategy == "HARVEST":
            state.farmer_inventory.append(crop)
            state.crops.remove(crop)
            print(f"[Agent] Cosechado {crop.pos} | inventario: {len(state.farmer_inventory)}")

    def _reset_goal(self):
        self.goal = None
        self.strategy = None
        self.current_path = deque()
        self.needs_replan = False

    def interrupt(self):
        self.needs_replan = True