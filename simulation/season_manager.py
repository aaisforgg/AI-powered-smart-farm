import random

class SeasonManager:
    def __init__(self):
        self.seasons = ["Primavera", "Verano", "Otoño", "Invierno"]
        self.current_season_idx = 0
        self.days_passed = 0
        self.days_per_season = 30 # Ajusta según tu proyecto

    @property
    def current_season(self):
        return self.seasons[self.current_season_idx]

    def update(self, event_manager):
        """Este método se llama en cada 'tick' o día de la simulación."""
        self.days_passed += 1
        
        # 1. Cambiar de estación si pasó el tiempo
        if self.days_passed >= self.days_per_season:
            self.days_passed = 0
            self.current_season_idx = (self.current_season_idx + 1) % len(self.seasons)
            print(f"🍂 La estación ha cambiado a: {self.current_season}")

        # 2. LA CLAVE: Llamar al EventManager
        # Le pasamos la estación actual para que decida qué tan probable es un desastre
        event_manager.update(self.current_season)