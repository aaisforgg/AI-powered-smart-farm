from .movement import Movement
from .decision import Decision
from .strategies import Strategy


class Agent:
    def __init__(self, x, y, game_map, width, height):
        self.x = x
        self.y = y

        self.movement = Movement(game_map, width, height)
        self.decision = Decision()
        self.strategy = Strategy()

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.movement.can_move(new_x, new_y):
            self.x = new_x
            self.y = new_y