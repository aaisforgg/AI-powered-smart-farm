"""Salida de debug estructurada por consola.
Activar con: python main.py --debug
"""


def debug_tick(state, agent):
    tick = state.tick

    # ── ENERGY ──────────────────────────────────────────────────────────────
    pct = int(agent.energy / agent.max_energy * 100) if agent.max_energy > 0 else 0
    energy_label = "— CRÍTICA" if agent.energy <= agent.energy_threshold else ""

    # ── STATE narrative ──────────────────────────────────────────────────────
    if agent.resting:
        estado = "Descansando"
    elif agent.current_path and agent.goal:
        estado = f"Siguiendo path → {agent.goal.pos}"
    elif agent.goal:
        estado = f"Ejecutando goal → {agent.goal.pos}"
    elif agent.current_path:
        estado = "Explorando (path activo)"
    else:
        estado = "Explorando"

    # ── GOAL display ─────────────────────────────────────────────────────────
    if agent.goal:
        g = agent.goal
        goal_str = f"{g.pos} fase={g.fase} hum={g.humedad:.1f}"
    else:
        goal_str = "None"

    # ── CROPS list (state.crops, máx 6) ─────────────────────────────────────
    MAX_SHOW = 6
    crop_parts = [
        f"({c.x},{c.y}) f={c.fase} h={c.humedad:.0f}"
        for c in state.crops[:MAX_SHOW]
    ]
    crops_str = " | ".join(crop_parts) if crop_parts else "ninguno"
    if len(state.crops) > MAX_SHOW:
        crops_str += f" ... +{len(state.crops) - MAX_SHOW} más"

    # ── DECISION reason (de la última llamada a choose_goal) ─────────────────
    reason = getattr(
        agent.decision_system.goal_manager, "last_reject_reason", "—"
    )

    # ── ENERGY FLOW ──────────────────────────────────────────────────────────
    tile       = state.grid[agent.y][agent.x]
    tile_cost  = tile.cost
    gene_cons  = agent.genes.energy_consumption
    event_mult = state.active_effects.get("movement_cost_multiplier", 1.0)
    drain      = state.active_effects.get("energy_drain_per_tick", 0.0)
    flow_total = tile_cost * gene_cons * event_mult + drain

    # ── OUTPUT ───────────────────────────────────────────────────────────────
    print(f"\n=== TICK {tick} ===")
    print(f"[ENERGY]       {agent.energy:.1f} / {agent.max_energy:.1f}  ({pct}%)  {energy_label}")
    print(f"[STATE]        {estado} | resting={agent.resting} | needs_replan={agent.needs_replan}")
    print(f"[GOAL]         {goal_str} | strategy={agent.strategy}")
    print(f"[PATH]         {len(agent.current_path)} pasos")
    print(f"[MEMORY]       known_crops={len(agent.memory['known_crops'])} | "
          f"home_tiles={len(agent.memory['home_tiles'])} | "
          f"visited={len(agent.memory['visited_tiles'])}")
    print(f"[CROPS]        {crops_str}")
    print(f"[DECISION]     GoalManager devolvió: {goal_str if agent.goal else 'None'} — razón: {reason}")
    print(f"[ENERGY_FLOW]  tile_cost={tile_cost} × gene_cons={gene_cons:.2f} "
          f"× event_mult={event_mult:.1f} + drain={drain:.2f} = -{flow_total:.2f}/tick")
