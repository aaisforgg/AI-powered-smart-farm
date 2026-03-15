class SeasonManager:

    SEASONS = ["Primavera", "Verano", "Otoño", "Invierno"]

    def __init__(self, days_per_season=30):
        self.current_season_idx = 0
        self.days_passed = 0
        self.days_per_season = days_per_season

    @property
    def current_season(self):
        return self.SEASONS[self.current_season_idx]

    def update(self, event_manager, state):
        """Se llama cada tick desde el Pipeline via tick_season."""
        self.days_passed += 1

        if self.days_passed >= self.days_per_season:
            self.days_passed = 0
            self.current_season_idx = (self.current_season_idx + 1) % len(self.SEASONS)
            print(f"La estación ha cambiado a: {self.current_season}")

        # Actualizar la estación en el state
        state.season = self.current_season

        # Dejar que EventManager decida si lanza un evento
        event_manager.check_for_event(self.current_season, state)