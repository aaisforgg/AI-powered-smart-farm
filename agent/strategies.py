
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

        # Fase 1: siempre regar (humedad se capea a 100, mejor que estar idle)
        return "WATER"

    def choose_animal_strategy(self, state, animal):
        """Retorna 'FEED' | 'COLLECT' | None."""
        if animal is None or not hasattr(animal, "hambre"):
            return None
        if animal.producto_listo:
            return "COLLECT"
        if animal.hambre >= 50:
            return "FEED"
        return None