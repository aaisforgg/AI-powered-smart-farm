
class StrategyManager:
    """
    Fuente única de verdad para decidir qué hacer con un Crop.
    Tanto GoalManager como _execute_strategy consultan aquí.
    """

    def choose_strategy(self, state, goal):
        """Retorna 'WATER' | 'PLANT' | 'HARVEST' | None."""
        if goal is None:
            return None

        if not (hasattr(goal, "humedad") and hasattr(goal, "fase")):
            return None

        # Fase 2+: listo para cosechar
        if goal.fase >= 2:
            return "HARVEST"

        # Cualquier fase < 2 con humedad baja: regar urgente
        if goal.humedad < 30:
            return "WATER"

        # Fase 0: plantar
        if goal.fase == 0:
            return "PLANT"

        # Fase 1 con humedad entre 30-60: riego preventivo
        if goal.fase == 1 and goal.humedad < 60:
            return "WATER"

        # Fase 1 con humedad >= 60: no necesita nada por ahora
        return None