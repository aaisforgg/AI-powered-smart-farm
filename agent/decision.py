from .goals import GoalManager
from .strategies import StrategyManager

class DecisionSystem:

    def __init__(self):
        self.goal_manager = GoalManager()       # ← esto ya llama __init__
        self.strategy_manager = StrategyManager()

    def decide(self, state, agent):
        goal = self.goal_manager.choose_goal(state, agent)

        if goal is None:
            return None, None

        strategy = self.strategy_manager.choose_strategy(state, goal)

        if strategy is None:
            return None, None

        return goal, strategy