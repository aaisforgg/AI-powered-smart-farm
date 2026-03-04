#agent
#agent.py
from .decision import DecisionSystem
from .movement import Movement

class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.goal = None
        self.strategy = None

        self.decision_system = DecisionSystem()
        self.movement = Movement()

    def update(self, grid):

        # Si no tiene meta, pensar
        if not self.goal:
            self.goal, self.strategy = self.decision_system.decide(grid)

        # Si tiene meta, moverse
        if self.goal:
            if (self.x, self.y) != self.goal:
                self.movement.move_towards(self, grid, self.goal)

            else:
                self.act(grid)

    def act(self, grid):

        x, y = self.goal

        if self.strategy == "WATER":
            grid[y][x] = 3  # regado

        elif self.strategy == "PLANT":
            grid[y][x] = 2  # sembrado

        self.goal = None
        self.strategy = None