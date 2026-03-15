from .strategies import StrategyManager

class GoalManager:

    PRIORITY = {
        "HARVEST": 1,
        "WATER":   2,
        "PLANT":   3,
    }

    def __init__(self):
        self._strategy = StrategyManager()

    def choose_goal(self, state, agent):
        crops = list(agent.memory["known_crops"].values())

        if not crops:
            return None

        # Solo considerar las últimas 3 acciones, no 10
        recent_actions = set(list(agent.memory["last_actions"])[-3:])

        candidates = []

        for crop in crops:
            # Delegar a StrategyManager (fuente única de verdad)
            strategy = self._strategy.choose_strategy(state, crop)

            if strategy is None:
                continue

            # HARVEST nunca se bloquea por acciones recientes
            if strategy != "HARVEST" and (strategy, crop.pos) in recent_actions:
                continue

            cx, cy = crop.pos
            dist = abs(cx - agent.x) + abs(cy - agent.y)
            priority = self.PRIORITY.get(strategy, 99)

            candidates.append((priority, dist, crop))

        if not candidates:
            return None

        candidates.sort(key=lambda c: (c[0], c[1]))
        return candidates[0][2]