class SeasonManager:
    def __init__(self):
        self.seasons = ["Primavera", "Verano", "Otoño", "Invierno"]
        self.current_season_idx = 0
        self.days_passed = 0
        self.days_per_season = 100

    @property
    def current_season(self):
        return self.seasons[self.current_season_idx]

    def get_season(self):
        """Devuelve el nombre de la estación actual"""
        return self.current_season

    def update(self):
        self.days_passed += 1
        if self.days_passed >= self.days_per_season:
            self.days_passed = 0
            self.current_season_idx = (self.current_season_idx + 1) % len(self.seasons)
            print(f"🍂 Cambio de estación: {self.current_season}")
            return True
        return False