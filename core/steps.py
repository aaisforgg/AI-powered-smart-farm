"""
Pasos del game loop. Cada uno recibe GameState y hace una sola cosa.
Pipeline los ejecuta en orden.

REGLA: Estos pasos no importan de agent/, simulation/, ni world/.
       Solo manipulan GameState y llaman métodos via las referencias opacas.
"""


def tick_agent(state):
    """Actualiza al agente: decisión, movimiento, acción."""
    agent = state._agent_ref
    if agent is None:
        return

    agent.update(state)
    state.farmer_pos = (agent.x, agent.y)
    state.farmer_energy = agent.energy


def tick_crops(state):
    """Crecimiento y secado de todos los cultivos."""
    dry_multiplier = state.active_effects.get("crop_dry_multiplier", 1.0)

    for crop in state.crops:
        crop.crecer(
            tasa_secado=1.0,
            umbral_crecimiento=20.0,
            dry_multiplier=dry_multiplier
        )


def tick_season(state):
    """Avanza estaciones. Si hay EventManager, le pasa la estación actual."""
    season_mgr = state._season_mgr
    event_mgr = state._event_mgr

    if season_mgr is not None and event_mgr is not None:
        season_mgr.update(event_mgr, state)


def tick_events(state):
    """Aplica/limpia efectos de eventos activos."""
    event_mgr = state._event_mgr
    if event_mgr is not None:
        event_mgr.apply_active_effects(state)


def tick_counter(state):
    """Incrementa el contador global de ticks."""
    state.tick += 1