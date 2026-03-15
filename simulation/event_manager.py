import random

class EventManager:
    """
    Gestiona eventos climáticos/ambientales.

    REGLA: Este manager NUNCA toca al agente directamente.
           Solo escribe efectos en state.active_effects.
           El agente los lee y reacciona por su cuenta.
    """

    EVENTS = [
        "sequia",
        "tormenta",
        "nevada",
        "inundacion",
        "plaga",
        "gran_deslave",
        "nevada_paralizante",
        "plaga_de_insectos",
    ]

    def __init__(self):
        self.active_event = None
        self.duration_remaining = 0

    def check_for_event(self, current_season, state):
        """Llamado por SeasonManager cada tick. Decide si lanzar un evento."""

        # Si hay un evento activo, reducir duración
        if self.duration_remaining > 0:
            self.duration_remaining -= 1
            if self.duration_remaining == 0:
                self._clear_event(state)
            return

        # Probabilidad base de evento (más alta en invierno)
        prob = 0.02
        if current_season == "Invierno":
            prob = 0.05

        if random.random() < prob:
            self._trigger_event(state)

    def _trigger_event(self, state):
        """Activa un evento aleatorio escribiendo efectos en state."""
        self.active_event = random.choice(self.EVENTS)
        self.duration_remaining = random.randint(5, 15)

        print(f"[Evento] {self.active_event.upper()} por {self.duration_remaining} ticks")

        effects = state.active_effects
        effects["event_name"] = self.active_event

        if self.active_event == "sequia":
            # Los cultivos se secan más rápido (el step tick_crops puede leer esto)
            effects["crop_dry_multiplier"] = 3.0

        elif self.active_event == "tormenta":
            # Moverse cuesta más energía
            effects["movement_cost_multiplier"] = 2.0
            # Posibilidad de daño por rayo (energía) cada tick
            effects["energy_drain_per_tick"] = 3.0

        elif self.active_event == "nevada":
            # Todo cuesta más moverse
            effects["movement_cost_multiplier"] = 3.0
            effects["energy_drain_per_tick"] = 1.5

        elif self.active_event == "inundacion":
            # Cultivos dañados + terreno pesado
            effects["movement_cost_multiplier"] = 2.5
            self._damage_random_crops(state, count=2)

        elif self.active_event == "plaga":
            # Cultivos pierden humedad extra
            effects["crop_dry_multiplier"] = 5.0

        elif self.active_event == "gran_deslave":
            # Terreno devastado: moverse es muy costoso y se pierden cultivos
            effects["movement_cost_multiplier"] = 4.0
            effects["energy_drain_per_tick"] = 2.0
            self._damage_random_crops(state, count=3)

        elif self.active_event == "nevada_paralizante":
            # Nieve extrema: movimiento casi imposible y drain severo
            effects["movement_cost_multiplier"] = 5.0
            effects["energy_drain_per_tick"] = 3.0

        elif self.active_event == "plaga_de_insectos":
            # Insectos destruyen cultivos directamente, aceleran el secado y dañan al agente
            effects["crop_dry_multiplier"] = 4.0
            effects["energy_drain_per_tick"] = 1.0
            self._damage_random_crops(state, count=2)

    def _clear_event(self, state):
        """Limpia todos los efectos cuando el evento termina."""
        print(f"[Evento] {(self.active_event or 'desconocido').upper()} terminó")
        self.active_event = None
        state.active_effects.clear()

    def _damage_random_crops(self, state, count):
        """Elimina algunos cultivos al azar (inundación, etc.)."""
        if not state.crops:
            return
        for _ in range(min(count, len(state.crops))):
            crop = random.choice(state.crops)
            state.crops.remove(crop)
            print(f"[Evento] Cultivo en {crop.pos} destruido")

    def apply_active_effects(self, state):
        """
        Llamado cada tick por tick_events.
        Aquí van efectos que necesitan aplicarse continuamente,
        no solo una vez al disparar el evento.
        """
        # Por ahora los efectos se leen directamente del dict
        # en agent.update() y tick_crops. Este método existe para
        # efectos más complejos que necesiten lógica cada tick.
        pass
