from .goals import GoalManager
from .strategies import StrategyManager

class DecisionSystem:

    def __init__(self):
        self.goal_manager = GoalManager()
        self.strategy_manager = StrategyManager()

    def decide(self, grid, agent):

        # -------------------------
        # 1️⃣ Sin energía
        # -------------------------
        if agent.energy <= 0:
            print("Agente agotado.")
            return None, "EXHAUSTED"

        # -------------------------
        # 2️⃣ Energía baja
        # -------------------------
        if agent.energy < 30:
            print("Energía baja → descansar.")
            return None, "REST"

        # -------------------------
        # 3️⃣ Energía media
        # -------------------------
        if 30 <= agent.energy < 60:
            print("Energía media → comportamiento conservador.")
            goal = self.goal_manager.choose_goal(grid, agent)
            strategy = "CAUTIOUS"
            return goal, strategy

        # -------------------------
        # 4️⃣ Energía alta
        # -------------------------
        print("Energía alta → comportamiento normal.")
        goal = self.goal_manager.choose_goal(grid, agent)
        strategy = self.strategy_manager.choose_strategy(grid, goal)

        return goal, strategy