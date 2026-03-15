import pygame

from rendering.theme import (
    C, SEASON_COLORS, EVENT_COLORS, GOAL_LABELS,
    CROP_PHASE_LABELS, CROP_PHASE_COLORS,
    GRID_W, HUD_W, WINDOW_H,
)
from rendering.helpers import _card, _label, _bar, _section_title


GENE_RANGES = {
    "energy_max":         (40,   200),
    "energy_consumption": (0.1,  2.0),
    "rest_efficiency":    (0.5,  8.0),
    "exploration_rate":   (0.01, 1.0),
}


def _gene_pct(value, gene_name):
    lo, hi = GENE_RANGES[gene_name]
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


class HUDLayout:
    """Apila secciones verticalmente con padding automático."""

    def __init__(self, x, width, start_y=10, gap=8):
        self.x   = x
        self.w   = width
        self.y   = start_y
        self.gap = gap
        self.pad = 10

    def next_section(self, height):
        """Reserva espacio para una sección. Retorna (x, y, w, h)."""
        rect   = (self.x, self.y, self.w, height)
        self.y += height + self.gap
        return rect


def dibujar_hud(pantalla, state, agente, fuentes):
    px  = GRID_W + 10
    pw  = HUD_W - 20
    pad = 10

    pygame.draw.rect(pantalla, C["bg"], (GRID_W, 0, HUD_W, WINDOW_H))
    pygame.draw.line(pantalla, C["card_border"], (GRID_W, 0), (GRID_W, WINDOW_H), 1)

    gen_num = agente.evolution.generation
    layout  = HUDLayout(px, pw)

    # ── Header ────────────────────────────────────────────────────────────
    hx, hy, hw, hh = layout.next_section(44)
    _card(pantalla, hx, hy, hw, hh, radius=8)
    _label(pantalla, fuentes, "AI SMART FARM",      hx + pad, hy + 10, C["accent"], "md")
    _label(pantalla, fuentes, "Simulación autónoma", hx + pad, hy + 26, C["txt_dim"], "xs")
    gen_txt = f"Gen. {gen_num}"
    gen_w   = fuentes["xs"].size(gen_txt)[0]
    _label(pantalla, fuentes, gen_txt, hx + hw - pad - gen_w, hy + 14, C["txt_dim"], "xs")

    # ── Estación ──────────────────────────────────────────────────────────
    sx, sy, sw, sh = layout.next_section(76)
    season  = getattr(state, "season", "—")
    s_color = SEASON_COLORS.get(season, C["txt_mid"])
    _card(pantalla, sx, sy, sw, sh, radius=6)
    _section_title(pantalla, fuentes, "ESTACIÓN", sx + pad, sy + pad, sw - pad * 2)
    _label(pantalla, fuentes, season, sx + pad, sy + 28, s_color, "sm")
    day_in_season = getattr(state, "_season_mgr", None)
    if day_in_season and hasattr(day_in_season, "days_passed"):
        dp  = day_in_season.days_passed
        dps = day_in_season.days_per_season
        _bar(pantalla, sx + pad, sy + 46, sw - pad * 2, 8, dp / dps, s_color, s_color)
        _label(pantalla, fuentes, f"Día {dp} de {dps}", sx + pad, sy + 58, C["txt_dim"], "xs")

    # ── Evento ────────────────────────────────────────────────────────────
    ex, ey, ew, eh = layout.next_section(72)
    event_name = state.active_effects.get("event_name", "")
    evt_label  = event_name.replace("_", " ").capitalize() if event_name else "Despejado"
    evt_color  = EVENT_COLORS.get(event_name, C["accent2"]) if event_name else C["txt_mid"]
    _card(pantalla, ex, ey, ew, eh, radius=6)
    _section_title(pantalla, fuentes, "EVENTO", ex + pad, ey + pad, ew - pad * 2)
    pygame.draw.circle(pantalla, evt_color, (ex + pad + 5, ey + 42), 5)
    _label(pantalla, fuentes, evt_label, ex + pad + 18, ey + 34, evt_color, "sm")

    # ── Agente ────────────────────────────────────────────────────────────
    ax, ay, aw, ah = layout.next_section(148)
    energy_pct  = agente.energy / max(agente.max_energy, 1)

    if agente.resting:
        estado_txt = "Descansando"
        estado_col = C["energy_mid"]
    elif agente.current_path:
        estado_txt = "En ruta"
        estado_col = C["accent"]
    elif agente.goal:
        estado_txt = "Trabajando"
        estado_col = C["energy_hi"]
    else:
        estado_txt = "Explorando"
        estado_col = C["accent2"]

    goal    = agente.goal
    if goal and hasattr(goal, "x") and hasattr(goal, "y"):
        goal_str = f"Crop ({goal.x},{goal.y})"
    else:
        goal_str = "—"

    accion_str = GOAL_LABELS.get(agente.strategy, str(agente.strategy) if agente.strategy else "—")
    path_len   = len(agente.current_path) if agente.current_path else 0
    path_str   = f"{path_len} pasos" if path_len > 0 else "—"
    cosechas   = agente.life_stats.get("harvests", 0)

    _card(pantalla, ax, ay, aw, ah, radius=6)
    _section_title(pantalla, fuentes, "AGENTE", ax + pad, ay + pad, aw - pad * 2)

    # Fila 1: Pos | Estado
    _label(pantalla, fuentes, "Pos",              ax + pad,        ay + 28, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"({agente.x},{agente.y})", ax + pad + 24, ay + 28, C["txt_hi"],  "xs")
    _label(pantalla, fuentes, estado_txt,          ax + aw // 2,    ay + 28, estado_col,  "xs")

    # Fila 2: Goal
    _label(pantalla, fuentes, "Goal",    ax + pad,        ay + 44, C["txt_dim"], "xs")
    _label(pantalla, fuentes, goal_str,  ax + pad + 30,   ay + 44, C["txt_hi"],  "xs")

    # Fila 3: Acción
    _label(pantalla, fuentes, "Acción",   ax + pad,        ay + 58, C["txt_dim"], "xs")
    _label(pantalla, fuentes, accion_str, ax + pad + 42,   ay + 58, C["accent"],  "xs")

    # Fila 4: Energía barra
    _label(pantalla, fuentes, "Energía", ax + pad, ay + 76, C["txt_dim"], "xs")
    _bar(pantalla, ax + pad + 52, ay + 74, aw - pad * 2 - 52, 10,
         energy_pct, C["energy_hi"], C["energy_lo"], C["energy_mid"])
    pct_txt = f"{int(energy_pct * 100)}%"
    _label(pantalla, fuentes, pct_txt,
           ax + aw - pad - fuentes["xs"].size(pct_txt)[0], ay + 76, C["txt_mid"], "xs")

    # Fila 5: valores de energía + path
    _label(pantalla, fuentes, f"{agente.energy:.0f}/{agente.max_energy:.0f}",
           ax + pad, ay + 92, C["txt_dim"], "xs")
    _label(pantalla, fuentes, "Path",     ax + aw // 2,      ay + 92, C["txt_dim"], "xs")
    _label(pantalla, fuentes, path_str,   ax + aw // 2 + 30, ay + 92, C["txt_hi"],  "xs")

    # Fila 6: Cosechas
    _label(pantalla, fuentes, f"Cosechas: {cosechas}", ax + pad, ay + 110, C["txt_dim"], "xs")

    # ── Genética ──────────────────────────────────────────────────────────
    gx, gy, gw, gh = layout.next_section(120)
    g = agente.genes
    _card(pantalla, gx, gy, gw, gh, radius=6)
    _section_title(pantalla, fuentes, f"GENÉTICA  —  Gen {gen_num}", gx + pad, gy + pad, gw - pad * 2)
    gene_stats = [
        ("E.Max",  f"{g.energy_max:.0f}",          _gene_pct(g.energy_max,         "energy_max")),
        ("Cons.",  f"{g.energy_consumption:.2f}",   _gene_pct(g.energy_consumption, "energy_consumption")),
        ("Rest.",  f"{g.rest_efficiency:.2f}",      _gene_pct(g.rest_efficiency,    "rest_efficiency")),
        ("Expl.",  f"{g.exploration_rate:.2f}",     _gene_pct(g.exploration_rate,   "exploration_rate")),
    ]
    col_w = (gw - pad * 2) // 2
    for i, (lbl, val, pct) in enumerate(gene_stats):
        col = i % 2
        row = i // 2
        bx  = gx + pad + col * col_w
        by  = gy + 30 + row * 46
        _label(pantalla, fuentes, lbl, bx,      by, C["txt_dim"], "xs")
        _label(pantalla, fuentes, val, bx + 36, by, C["txt_hi"],  "xs")
        _bar(pantalla, bx, by + 14, col_w - 8, 6, pct, C["accent"], C["accent"], None)

    # ── Evolución ─────────────────────────────────────────────────────────
    vx, vy, vw, vh = layout.next_section(78)
    evo          = agente.evolution
    last_fitness = evo.fitness_history[-1] if evo.fitness_history else 0.0
    best_fitness = evo.best_fitness

    if len(evo.fitness_history) >= 2:
        recent_avg = sum(evo.fitness_history[-3:]) / len(evo.fitness_history[-3:])
        trend      = "↑" if last_fitness >= recent_avg else "↓"
        trend_col  = C["energy_hi"] if trend == "↑" else C["energy_lo"]
    else:
        trend     = "—"
        trend_col = C["txt_dim"]

    _card(pantalla, vx, vy, vw, vh, radius=6)
    _section_title(pantalla, fuentes, "EVOLUCIÓN", vx + pad, vy + pad, vw - pad * 2)

    # Fila 1: Gen | Fitness actual
    _label(pantalla, fuentes, "Gen.",     vx + pad,        vy + 28, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(gen_num), vx + pad + 30, vy + 28, C["txt_hi"],  "xs")
    _label(pantalla, fuentes, "Actual",   vx + vw // 2,    vy + 28, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"{last_fitness:.1f}", vx + vw // 2 + 42, vy + 28, C["txt_hi"], "xs")

    # Fila 2: Mejor | Tendencia
    _label(pantalla, fuentes, "Mejor",    vx + pad,        vy + 44, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"{best_fitness:.1f}", vx + pad + 38, vy + 44, C["accent2"], "xs")
    _label(pantalla, fuentes, "Tend.",    vx + vw // 2,    vy + 44, C["txt_dim"], "xs")
    _label(pantalla, fuentes, trend,      vx + vw // 2 + 36, vy + 44, trend_col,   "sm")

    # ── Cultivos ──────────────────────────────────────────────────────────
    cx, cy_s, cw, ch = layout.next_section(100)
    fase_counts = {0: 0, 1: 0, 2: 0}
    for crop in state.crops:
        fase_counts[crop.fase] = fase_counts.get(crop.fase, 0) + 1
    total = len(state.crops)

    _card(pantalla, cx, cy_s, cw, ch, radius=6)
    _section_title(pantalla, fuentes, f"CULTIVOS  ({total} total)", cx + pad, cy_s + pad, cw - pad * 2)
    for i, (fase, label) in enumerate(CROP_PHASE_LABELS.items()):
        bx  = cx + pad
        by  = cy_s + 28 + i * 24
        cnt = fase_counts.get(fase, 0)
        pygame.draw.circle(pantalla, CROP_PHASE_COLORS[fase], (bx + 4, by + 6), 4)
        _label(pantalla, fuentes, label, bx + 14, by, C["txt_mid"], "xs")
        cnt_w = fuentes["xs"].size(str(cnt))[0]
        _label(pantalla, fuentes, str(cnt), cx + cw - pad - cnt_w, by, C["txt_hi"], "xs")
        if total > 0:
            _bar(pantalla, bx + 14, by + 14, cw - pad * 2 - 14, 5,
                 cnt / total, CROP_PHASE_COLORS[fase], CROP_PHASE_COLORS[fase])

    # ── Simulación ────────────────────────────────────────────────────────
    smx, smy, smw, smh = layout.next_section(66)
    visited = len(agente.memory.get("visited_tiles", set()))
    total_tiles = 80 * 65
    inventory   = len(agente.inventory) if hasattr(agente, "inventory") else 0

    _card(pantalla, smx, smy, smw, smh, radius=6)
    _section_title(pantalla, fuentes, "SIMULACIÓN", smx + pad, smy + pad, smw - pad * 2)

    # Fila 1: Tick | Gen.
    _label(pantalla, fuentes, "Tick",        smx + pad,        smy + 28, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(state.tick), smx + pad + 30,  smy + 28, C["txt_hi"],  "sm")
    _label(pantalla, fuentes, "Gen.",        smx + smw // 2,   smy + 28, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(gen_num),  smx + smw // 2 + 30, smy + 28, C["txt_mid"], "sm")

    # Fila 2: Inventario | Tiles
    inv_str   = f"{inventory} items"
    tiles_str = f"{visited}/{total_tiles}"
    _label(pantalla, fuentes, "Inv.",        smx + pad,        smy + 44, C["txt_dim"], "xs")
    _label(pantalla, fuentes, inv_str,       smx + pad + 26,   smy + 44, C["txt_mid"], "xs")
    _label(pantalla, fuentes, "Tiles",       smx + smw // 2,   smy + 44, C["txt_dim"], "xs")
    _label(pantalla, fuentes, tiles_str,     smx + smw // 2 + 34, smy + 44, C["txt_mid"], "xs")
