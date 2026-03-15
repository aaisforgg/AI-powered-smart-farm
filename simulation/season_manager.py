from core.constants import TICKS_PER_DAY


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
        self._tick_in_day = 0   # subtick interno — no expuesto al HUD

    @property
    def current_season(self):
        return self.SEASONS[self.current_season_idx]

    @property
    def days_per_season(self):
        return self.DAYS_PER_SEASON[self.current_season]

    SEASON_MODIFIERS = {
        "Primavera": {"growth_multiplier": 1.5, "dry_season_multiplier": 0.8},
        "Verano":    {"growth_multiplier": 1.0, "dry_season_multiplier": 1.5},
        "Otoño":     {"growth_multiplier": 0.7, "dry_season_multiplier": 1.0},
        "Invierno":  {"growth_multiplier": 0.3, "dry_season_multiplier": 0.5},
    }

    def update(self, event_manager, state):
        """Se llama cada tick. Un día avanza cada TICKS_PER_DAY ticks."""
        state.season = self.current_season

        # Escribir multiplicadores estacionales cada tick
        mods = self.SEASON_MODIFIERS.get(self.current_season, {})
        state.active_effects["growth_multiplier"] = mods.get("growth_multiplier", 1.0)
        state.active_effects["dry_season_multiplier"] = mods.get("dry_season_multiplier", 1.0)

        self._tick_in_day += 1
        if self._tick_in_day < TICKS_PER_DAY:
            return  # día aún no completo

        # — Nuevo día —
        self._tick_in_day = 0
        self.days_passed += 1
        event_manager.check_for_event(self.current_season, state)

        if self.days_passed >= self.days_per_season:
            self.days_passed = 0
            self.current_season_idx = (self.current_season_idx + 1) % len(self.SEASONS)
            state.season = self.current_season
            print(f"La estación ha cambiado a: {self.current_season}")
