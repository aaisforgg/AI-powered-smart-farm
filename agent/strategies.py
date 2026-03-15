
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

        # Fase 1: regar si humedad < 85 (mantiene al agente ocupado mientras madura)
        if goal.fase == 1 and goal.humedad < 85:
            return "WATER"

        # Fase 1 con humedad >= 85: suficientemente regado por ahora
        return None