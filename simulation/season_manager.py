class SeasonManager:

    SEASONS = ["Primavera", "Verano", "Otoño", "Invierno"]

    # Días reales por estación en México
    DAYS_PER_SEASON = {
        "Primavera": 92,   # 20 mar – 20 jun
        "Verano":    94,   # 21 jun – 22 sep
        "Otoño":     89,   # 23 sep – 21 dic
        "Invierno":  88,   # 22 dic – 19 mar
    }

    def __init__(self):
        self.current_season_idx = 0
        self.days_passed = 0

    @property
    def current_season(self):
        return self.SEASONS[self.current_season_idx]

    @property
    def days_per_season(self):
        return self.DAYS_PER_SEASON[self.current_season]

    def update(self, event_manager, state):
        """Se llama cada tick desde el Pipeline via tick_season."""
        self.days_passed += 1

        if self.days_passed >= self.days_per_season:
            self.days_passed = 0
            self.current_season_idx = (self.current_season_idx + 1) % len(self.SEASONS)
            print(f"La estación ha cambiado a: {self.current_season}")

        state.season = self.current_season
        event_manager.check_for_event(self.current_season, state)
