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

        if not self.goal:
            self.goal, self.strategy = self.decision_system.decide(grid, self)

        if self.goal:

            if (self.x, self.y) == self.goal:
                print("Llegó al cultivo!")
                self.goal = None
                self.strategy = None
            else:
                moved = self.movement.move_towards(self, grid, self.goal)

                if not moved:
                    self.movement.random_move(self, grid)

        else:
            self.movement.random_move(self, grid)