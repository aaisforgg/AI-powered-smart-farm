class GoalManager:
    """
    Elige el cultivo más urgente para el agente.
    Trabaja con objetos Crop que tienen .pos, .humedad y .fase.
    """

    PRIORITY = {
        "WATER":   1,
        "PLANT":   2,
        "HARVEST": 3,
    }

    def choose_goal(self, state, agent):
        """
        Retorna el Crop más prioritario y cercano, o None si no hay nada que hacer.
        """
        if not state.crops:
            return None

        candidates = []

        for crop in state.crops:
            strategy = self._evaluate_crop(crop)
            if strategy is None:
                continue

            cx, cy  = crop.pos
            dist    = abs(cx - agent.x) + abs(cy - agent.y)
            priority = self.PRIORITY.get(strategy, 99)
            candidates.append((priority, dist, crop))

        if not candidates:
            return None

        # Primero por urgencia, luego por cercanía
        candidates.sort(key=lambda c: (c[0], c[1]))
        return candidates[0][2]

    # ------------------------------------------------------------------
    def _evaluate_crop(self, crop):
        """
        Devuelve la estrategia que necesita el cultivo, o None si está bien.
        Basado en los atributos reales de Crop: .humedad y .fase
        """
        if crop.humedad < 30:
            return "WATER"

        if crop.fase >= 2:
            return "HARVEST"

        if crop.fase == 0:
            return "PLANT"

        return "WATER"