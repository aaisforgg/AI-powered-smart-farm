from .decision import DecisionSystem
from .movement import Movement

class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.goal = None

        self.decision_system = DecisionSystem()
        self.movement = Movement()

    def update(self, grid):

        # Si no tiene meta, pensar
        if not self.goal:
            self.goal = self.decision_system.decide(grid, self)

        # Si tiene meta
        if self.goal:

            if (self.x, self.y) == self.goal:
                print("Llegó al cultivo!")
                self.goal = None
            else:
                moved = self.movement.move_towards(self, grid, self.goal)

                # Si no pudo moverse hacia meta, explorar
                if not moved:
                    self.movement.random_move(self, grid)

        else:
            # Si no hay meta, explorar
            self.movement.random_move(self, grid)