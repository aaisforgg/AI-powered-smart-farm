from .goals import GoalManager
from .strategies import StrategyManager

class DecisionSystem:

    def __init__(self):
        self.goal_manager = GoalManager()
        self.strategy_manager = StrategyManager()

    def decide(self, grid, agent):
        goal = self.goal_manager.choose_goal(grid, agent)
        strategy = self.strategy_manager.choose_strategy(grid, goal)

        return goal, strategy