"""
Salida de debug por consola. Solo se usa si se lanza con --debug.
Uso: python main.py --debug
"""


def print_tick(state, agente):
    print(f"--- Tick {state.tick} ---")
    print(
        f"Pos: ({agente.x}, {agente.y}) | "
        f"Energía: {agente.energy:.1f}/{agente.max_energy:.1f} | "
        f"Resting: {agente.resting}"
    )
    print(f"Goal: {agente.goal} | Path: {len(agente.current_path)}")
    if hasattr(agente, "genes"):
        g = agente.genes
        print(
            f"Genes → emax:{g.energy_max:.1f}  econs:{g.energy_consumption:.2f}  "
            f"rest:{g.rest_efficiency:.2f}  expl:{g.exploration_rate:.2f}"
        )
    if hasattr(agente, "evolution"):
        print(f"Generación: {agente.evolution.generation} | "
              f"Cosechas: {agente.life_stats.get('harvests', 0)}")
    if state.active_effects:
        print(f"Efectos activos: {state.active_effects}")
    print()
