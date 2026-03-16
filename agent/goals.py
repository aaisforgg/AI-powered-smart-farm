from .strategies import StrategyManager


class GoalManager:

    PRIORITY = {
        "HARVEST": 1,
        "COLLECT": 1,
        "WATER":   2,
        "FEED":    2,
        "PLANT":   3,
    }

    def __init__(self):
        self._strategy = StrategyManager()
        self.last_reject_reason = "—"

    def choose_goal(self, state, agent):
        crops   = list(agent.memory["known_crops"].values())
        animals = [a for a in state.animals
                   if abs(a.x - agent.x) + abs(a.y - agent.y)
                   <= getattr(agent.genes, "vision_radius", 10)]

        if not crops and not animals:
            self.last_reject_reason = "no_crops_known"
            return None

        recent_actions  = set(list(agent.memory["last_actions"])[-2:])
        candidates      = []
        had_valid_strategy = False

        # — Crops —
        for crop in crops:
            strategy = self._strategy.choose_strategy(state, crop)
            if strategy is None:
                continue
            had_valid_strategy = True
            is_urgent_water = strategy == "WATER" and crop.humedad < 30
            if strategy not in ("HARVEST", "PLANT") and not is_urgent_water \
                    and (strategy, crop.pos) in recent_actions:
                continue
            cx, cy = crop.pos
            dist = abs(cx - agent.x) + abs(cy - agent.y)
            candidates.append((self.PRIORITY.get(strategy, 99), dist, crop, strategy))

        # — Animales —
        for animal in animals:
            strategy = self._strategy.choose_animal_strategy(state, animal)
            if strategy is None:
                continue
            had_valid_strategy = True
            if (strategy, animal.pos) in recent_actions:
                continue
            dist = abs(animal.x - agent.x) + abs(animal.y - agent.y)
            candidates.append((self.PRIORITY.get(strategy, 99), dist, animal, strategy))

        if not candidates:
            self.last_reject_reason = "all_blocked_by_recent" if had_valid_strategy else "no_candidates"
            return None

        candidates.sort(key=lambda c: (c[0], c[1]))
        winner = candidates[0]
        self.last_reject_reason = f"ok: {winner[3]} → {winner[2].pos}"
        return winner[2]
