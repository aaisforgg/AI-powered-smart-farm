class SeasonManager:
    def __init__(self):
        self.seasons = ["Primavera", "Verano", "Otoño", "Invierno"]
        self.current_season_idx = 0
        self.days_passed = 0
        self.days_per_season = 30 

    @property
    def current_season(self):
        return self.seasons[self.current_season_idx]

    def update(self):
       
        self.days_passed += 1
        
        # Cambiar de estación si pasó el tiempo
        if self.days_passed >= self.days_per_season:
            self.days_passed = 0
            self.current_season_idx = (self.current_season_idx + 1) % len(self.seasons)
            print(f"🍂 La estación ha cambiado a: {self.current_season}")
            return True # Opcional: avisar que hubo un cambio de estación
        
        return False