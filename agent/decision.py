from .goals import GoalManager
from .strategies import StrategyManager


class DecisionSystem:

    def __init__(self):
        self.goal_manager     = GoalManager()
        self.strategy_manager = StrategyManager()

    def decide(self, state, agent):
        """
        Retorna (goal, strategy).
        Si no hay nada que hacer retorna (None, None).
        """
        goal = self.goal_manager.choose_goal(state, agent)

        if goal is None:
            return None, None

        strategy = self.strategy_manager.choose_strategy(state, goal)

        if strategy is None:
            # El crop existe pero no necesita acción ahora mismo
            return None, None

        return goal, strategy