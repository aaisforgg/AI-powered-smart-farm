from .strategies import StrategyManager


class GoalManager:

    PRIORITY = {
        "HARVEST": 1,
        "WATER":   2,
        "PLANT":   3,
    }

    def __init__(self):
        self._strategy = StrategyManager()
        self.last_reject_reason = "—"

    def choose_goal(self, state, agent):
        crops = list(agent.memory["known_crops"].values())

        if not crops:
            self.last_reject_reason = "no_crops_known"
            return None

        # Solo considerar las últimas 2 acciones para evitar bloquear candidatos válidos
        recent_actions = set(list(agent.memory["last_actions"])[-2:])

        candidates = []
        had_valid_strategy = False

        for crop in crops:
            # Delegar a StrategyManager (fuente única de verdad)
            strategy = self._strategy.choose_strategy(state, crop)

            if strategy is None:
                continue

            had_valid_strategy = True

            # HARVEST y WATER urgente (humedad < 30) nunca se bloquean por acciones recientes
            is_urgent_water = strategy == "WATER" and crop.humedad < 30
            if strategy != "HARVEST" and not is_urgent_water and (strategy, crop.pos) in recent_actions:
                continue

            cx, cy = crop.pos
            dist = abs(cx - agent.x) + abs(cy - agent.y)
            priority = self.PRIORITY.get(strategy, 99)

            candidates.append((priority, dist, crop, strategy))

        if not candidates:
            if not had_valid_strategy:
                self.last_reject_reason = "no_candidates"
            else:
                self.last_reject_reason = "all_blocked_by_recent"
            return None

        candidates.sort(key=lambda c: (c[0], c[1]))
        winner = candidates[0]
        self.last_reject_reason = f"ok: {winner[3]} → {winner[2].pos}"
        return winner[2]
