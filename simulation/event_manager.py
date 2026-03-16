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
        self.duration_remaining = random.randint(80, 150)

        print(f"[Evento] {self.active_event.upper()} por {self.duration_remaining} días")

        effects = state.active_effects
        effects["event_name"] = self.active_event

        if self.active_event == "sequia":
            effects["crop_dry_multiplier"] = 3.0

        elif self.active_event == "tormenta":
            effects["movement_cost_multiplier"] = 2.0
            effects["energy_drain_per_tick"] = 3.0
            self._spawn_obstacles(state, "escombro", random.randint(40, 60))

        elif self.active_event == "nevada":
            effects["movement_cost_multiplier"] = 3.0
            effects["energy_drain_per_tick"] = 1.5
            self._spawn_obstacles(state, "nieve", random.randint(50, 70))

        elif self.active_event == "inundacion":
            effects["movement_cost_multiplier"] = 2.5
            self._damage_random_crops(state, count=2)
            self._spawn_obstacles(state, "charco", random.randint(45, 65))

        elif self.active_event == "plaga":
            effects["crop_dry_multiplier"] = 5.0

        elif self.active_event == "gran_deslave":
            effects["movement_cost_multiplier"] = 4.0
            effects["energy_drain_per_tick"] = 2.0
            self._damage_random_crops(state, count=3)
            self._spawn_obstacles(state, "lodo", random.randint(70, 100))

        elif self.active_event == "nevada_paralizante":
            effects["movement_cost_multiplier"] = 5.0
            effects["energy_drain_per_tick"] = 3.0
            self._spawn_obstacles(state, "nieve", random.randint(80, 110))

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

        # Forzar replan — el path actual puede cruzar obstáculos nuevos
        agent = state._agent_ref
        if agent is not None:
            agent.current_path.clear()
            agent.interrupt()

    # Obstáculos ambientales por estación: (tipo, min, max)
    SEASONAL_AMBIENT = {
        "Invierno":  [("nieve",    60,  90)],
        "Primavera": [("charco",   25,  40)],
        "Verano":    [("escombro", 20,  30)],
        "Otoño":     [("lodo",     40,  60)],
    }

    def on_season_change(self, state, new_season):
        """Limpia obstáculos de la estación anterior y genera los nuevos."""
        event_blocked = {(x, y) for x, y, _ in state.temp_obstacles}
        for x, y, _ in state.seasonal_obstacles:
            if (x, y) not in event_blocked:
                state.grid[y][x].walkable = True
        state.seasonal_obstacles.clear()

        configs = self.SEASONAL_AMBIENT.get(new_season, [])
        for tipo, mn, mx in configs:
            self._spawn_seasonal_obstacles(state, tipo, random.randint(mn, mx))
        if configs:
            print(f"[Estación] Obstáculos ambientales de {new_season} generados")

    def _spawn_seasonal_obstacles(self, state, tipo, count):
        """Coloca obstáculos estacionales persistentes priorizando accesos a cultivos."""
        occupied = set()
        for ox, oy, _ in state.temp_obstacles:
            occupied.add((ox, oy))
        for ox, oy, _ in state.seasonal_obstacles:
            occupied.add((ox, oy))

        agent = state._agent_ref
        if agent is not None:
            occupied.add((agent.x, agent.y))
            occupied |= agent.memory.get("home_tiles", set())

        rows = len(state.grid)
        cols = len(state.grid[0])

        cerca_crops = set()
        for c in state.crops:
            cx, cy = c.pos
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < cols and 0 <= ny < rows
                        and state.grid[ny][nx].walkable
                        and state.grid[ny][nx].type_name in self._BLOQUEABLES
                        and (nx, ny) not in occupied):
                    cerca_crops.add((nx, ny))

        pool_general = [
            (nodo.x, nodo.y)
            for fila in state.grid
            for nodo in fila
            if nodo.type_name in self._BLOQUEABLES
            and nodo.walkable
            and (nodo.x, nodo.y) not in occupied
        ]

        n_cerca = min(count // 3, len(cerca_crops))
        cerca_sel = random.sample(list(cerca_crops), n_cerca)
        pool_resto = [p for p in pool_general if p not in cerca_crops]
        n_resto = min(count - n_cerca, len(pool_resto))
        resto_sel = random.sample(pool_resto, n_resto)

        posiciones = cerca_sel + resto_sel
        if not posiciones:
            return

        for x, y in posiciones:
            state.grid[y][x].walkable = False
            state.seasonal_obstacles.append((x, y, tipo))

        print(f"[Estación] {len(posiciones)} obstáculos '{tipo}' "
              f"({n_cerca} bloqueando acceso a cultivos)")

    # Keys escritas exclusivamente por EventManager (no por SeasonManager)
    EVENT_EFFECT_KEYS = {
        "event_name",
        "movement_cost_multiplier",
        "energy_drain_per_tick",
        "crop_dry_multiplier",
        "harvest_bonus",
        "growth_multiplier_bonus",
    }

    def _clear_event(self, state):
        """Limpia efectos y obstáculos de evento (respeta obstáculos estacionales)."""
        seasonal_blocked = {(x, y) for x, y, _ in state.seasonal_obstacles}
        for x, y, _ in state.temp_obstacles:
            if (x, y) not in seasonal_blocked:
                state.grid[y][x].walkable = True
        if state.temp_obstacles:
            print(f"[Evento] {len(state.temp_obstacles)} obstáculos de evento eliminados")
        state.temp_obstacles.clear()

        for k in self.EVENT_EFFECT_KEYS:
            state.active_effects.pop(k, None)

        print(f"[Evento] {(self.active_event or 'desconocido').upper()} terminó")
        self.active_event = None

    def _damage_random_crops(self, state, count):
        """Elimina algunos cultivos al azar."""
        if not state.crops:
            return
        for _ in range(min(count, len(state.crops))):
            crop = random.choice(state.crops)
            state.crops.remove(crop)
            print(f"[Evento] Cultivo en {crop.pos} destruido")

    # Tipos de tile que pueden ser bloqueados por obstáculos
    _BLOQUEABLES = {"pasto", "cultivo", "puente", "puerta"}

    def _spawn_obstacles(self, state, tipo, count):
        """Coloca obstáculos en tiles walkables priorizando accesos a cultivos."""
        occupied = set()

        for ox, oy, _ in state.temp_obstacles:
            occupied.add((ox, oy))

        agent = state._agent_ref
        if agent is not None:
            occupied.add((agent.x, agent.y))
            occupied |= agent.memory.get("home_tiles", set())

        rows = len(state.grid)
        cols = len(state.grid[0])

        # Tiles adyacentes a cultivos — bloquean el acceso directo
        cerca_crops = set()
        for c in state.crops:
            cx, cy = c.pos
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < cols and 0 <= ny < rows
                        and state.grid[ny][nx].walkable
                        and state.grid[ny][nx].type_name in self._BLOQUEABLES
                        and (nx, ny) not in occupied):
                    cerca_crops.add((nx, ny))

        # Pool general: todos los tiles bloqueables walkables
        pool_general = [
            (nodo.x, nodo.y)
            for fila in state.grid
            for nodo in fila
            if nodo.type_name in self._BLOQUEABLES
            and nodo.walkable
            and (nodo.x, nodo.y) not in occupied
        ]

        # Mitad de los obstáculos cerca de cultivos, resto en el mapa
        n_cerca = min(count // 2, len(cerca_crops))
        cerca_sel = random.sample(list(cerca_crops), n_cerca)

        pool_resto = [p for p in pool_general if p not in cerca_crops]
        n_resto = min(count - n_cerca, len(pool_resto))
        resto_sel = random.sample(pool_resto, n_resto)

        posiciones = cerca_sel + resto_sel
        if not posiciones:
            return

        for x, y in posiciones:
            state.grid[y][x].walkable = False
            state.temp_obstacles.append((x, y, tipo))

        print(f"[Evento] {len(posiciones)} obstáculos '{tipo}' "
              f"({n_cerca} bloqueando acceso a cultivos)")

    def apply_active_effects(self, state):
        """
        Llamado cada tick por tick_events.
        Los efectos se leen directamente del dict en agent.update() y tick_crops.
        """
        pass
