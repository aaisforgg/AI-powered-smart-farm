class StrategyManager:
    """
    Determina qué acción ejecutar sobre un Crop dado.
    Misma lógica que GoalManager._evaluate_crop pero desde el punto
    de vista de la estrategia: se llama DESPUÉS de elegir el goal.
    """

    def choose_strategy(self, state, goal):
        """
        Retorna "WATER" | "PLANT" | "HARVEST" | None.
        goal es un objeto Crop con .humedad y .fase.
        """
        if goal is None:
            return None

        # Verificar que sea un Crop válido
        if not (hasattr(goal, "humedad") and hasattr(goal, "fase")):
            return None

        if goal.humedad < 30:
            return "WATER"

        if goal.fase == 0:
            return "PLANT"

        if goal.fase >= 2:
            return "HARVEST"

        return "WATER"   # en crecimiento, sin acción