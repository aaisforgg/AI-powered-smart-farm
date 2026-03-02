from .goals import GoalManager

class DecisionSystem:

    def __init__(self):
        self.goal_manager = GoalManager()

    def decide(self, grid, agent):
        return self.goal_manager.choose_goal(grid, agent)