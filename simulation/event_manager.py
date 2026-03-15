import random

class EventManager:
    """
    Gestiona eventos climáticos/ambientales.

    REGLA: Este manager NUNCA toca al agente directamente.
           Solo escribe efectos en state.active_effects.
           El agente los lee y reacciona por su cuenta.
    """

    SEASONAL_EVENTS = {
        "Primavera": {
            "positivos": ["lluvia_suave", "sol_ideal"],
            "negativos": ["plaga", "inundacion"],
        },
        "Verano": {
            "positivos": ["sol_ideal"],
            "negativos": ["sequia", "tormenta", "plaga_de_insectos"],
        },
        "Otoño": {
            "positivos": ["lluvia_suave", "cosecha_doble"],
            "negativos": ["tormenta", "gran_deslave", "plaga"],
        },
        "Invierno": {
            "positivos": [],
            "negativos": ["nevada", "nevada_paralizante", "tormenta"],
        },
    }

    def __init__(self):
        self.active_event = None
        self.duration_remaining = 0

    def check_for_event(self, current_season, state):
        """Llamado por SeasonManager cada día. Decide si lanzar un evento."""

        if self.duration_remaining > 0:
            self.duration_remaining -= 1
            if self.duration_remaining == 0:
                self._clear_event(state)
            return

        prob = 0.03
        if current_season == "Invierno":
            prob = 0.06

        if random.random() < prob:
            seasonal = self.SEASONAL_EVENTS.get(current_season, {"positivos": [], "negativos": []})

            # 30% positivo, 70% negativo
            if seasonal["positivos"] and random.random() < 0.30:
                event = random.choice(seasonal["positivos"])
            elif seasonal["negativos"]:
                event = random.choice(seasonal["negativos"])
            else:
                return

            self._trigger_event(state, event)

    def _trigger_event(self, state, event_name=None):
        """Activa un evento escribiendo efectos en state."""
        self.active_event = event_name or random.choice(["sequia", "tormenta"])
        self.duration_remaining = random.randint(5, 15)

        print(f"[Evento] {self.active_event.upper()} por {self.duration_remaining} días")

        effects = state.active_effects
        effects["event_name"] = self.active_event

        if self.active_event == "sequia":
            effects["crop_dry_multiplier"] = 3.0

        elif self.active_event == "tormenta":
            effects["movement_cost_multiplier"] = 2.0
            effects["energy_drain_per_tick"] = 3.0

        elif self.active_event == "nevada":
            effects["movement_cost_multiplier"] = 3.0
            effects["energy_drain_per_tick"] = 1.5

        elif self.active_event == "inundacion":
            effects["movement_cost_multiplier"] = 2.5
            self._damage_random_crops(state, count=2)

        elif self.active_event == "plaga":
            effects["crop_dry_multiplier"] = 5.0

        elif self.active_event == "gran_deslave":
            effects["movement_cost_multiplier"] = 4.0
            effects["energy_drain_per_tick"] = 2.0
            self._damage_random_crops(state, count=3)

        elif self.active_event == "nevada_paralizante":
            effects["movement_cost_multiplier"] = 5.0
            effects["energy_drain_per_tick"] = 3.0

        elif self.active_event == "plaga_de_insectos":
            effects["crop_dry_multiplier"] = 4.0
            effects["energy_drain_per_tick"] = 1.0
            self._damage_random_crops(state, count=2)

        elif self.active_event == "lluvia_suave":
            for crop in state.crops:
                crop.humedad = min(100.0, crop.humedad + 20.0)
            effects["crop_dry_multiplier"] = 0.3

        elif self.active_event == "sol_ideal":
            effects["growth_multiplier_bonus"] = 2.0

        elif self.active_event == "cosecha_doble":
            effects["harvest_bonus"] = 2

    def _clear_event(self, state):
        """Limpia todos los efectos cuando el evento termina."""
        print(f"[Evento] {(self.active_event or 'desconocido').upper()} terminó")
        self.active_event = None
        state.active_effects.clear()

    def _damage_random_crops(self, state, count):
        """Elimina algunos cultivos al azar."""
        if not state.crops:
            return
        for _ in range(min(count, len(state.crops))):
            crop = random.choice(state.crops)
            state.crops.remove(crop)
            print(f"[Evento] Cultivo en {crop.pos} destruido")

    def apply_active_effects(self, state):
        """
        Llamado cada tick por tick_events.
        Los efectos se leen directamente del dict en agent.update() y tick_crops.
        """
        pass
