class GoalManager:

    PRIORITY = {
        "WATER": 1,
        "PLANT": 2,
        "HARVEST": 3
    }

    def choose_goal(self, state, agent):

        crops = agent.memory["known_crops"].values()

        if not crops:
            return None

        recent_actions = set(agent.memory["last_actions"])

        candidates = []

        for crop in crops:

            strategy = self._evaluate_crop(crop)

            if strategy is None:
                continue

            if (strategy, crop.pos) in recent_actions:
                continue

            cx, cy = crop.pos

            dist = abs(cx - agent.x) + abs(cy - agent.y)

            priority = self.PRIORITY.get(strategy, 99)

            candidates.append((priority, dist, crop))

        if not candidates:
            return None

        candidates.sort(key=lambda c: (c[0], c[1]))

        return candidates[0][2]

    def _evaluate_crop(self, crop):

        if crop.humedad < 30:
            return "WATER"

        if crop.fase == 0:
            return "PLANT"

        if crop.fase >= 2:
            return "HARVEST"

        return None