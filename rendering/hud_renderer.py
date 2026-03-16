import pygame

from rendering.theme import (
    C, SEASON_COLORS, EVENT_COLORS, GOAL_LABELS,
    CROP_PHASE_LABELS, CROP_PHASE_COLORS,
    GRID_W, HUD_W, WINDOW_H,
)
from rendering.helpers import _card, _label, _bar, _section_title


GENE_RANGES = {
    "energy_max":         (80,   250),
    "energy_consumption": (0.1,  1.5),
    "rest_efficiency":    (0.5,  8.0),
    "exploration_rate":   (0.01, 1.0),
    "water_efficiency":   (15,   100),
    "risk_tolerance":     (0.05, 0.60),
}


def _gene_pct(value, gene_name):
    lo, hi = GENE_RANGES[gene_name]
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


class HUDLayout:
    """Apila secciones verticalmente con padding automático."""

    def __init__(self, x, width, start_y=8, gap=8):
        self.x   = x
        self.w   = width
        self.y   = start_y
        self.gap = gap
        self.pad = 14

    def next_section(self, height):
        """Reserva espacio para una sección. Retorna (x, y, w, h)."""
        rect   = (self.x, self.y, self.w, height)
        self.y += height + self.gap
        return rect


# ── Constantes de layout ───────────────────────────────────────────────────────
# 50+76+54+130+120+88+84+72 = 674 + gaps(96) + start(8) = 778
_H_HEADER    = 50
_H_SEASON    = 76
_H_EVENT     = 54
_H_AGENT     = 130
_H_GENETICS  = 120
_H_EVOLUTION = 88
_H_CROPS     = 84
_H_SIM       = 72

_PAD        = 14
_ROW_H      = 20


def dibujar_hud(pantalla, state, agente, fuentes):
    px  = GRID_W + 10
    pw  = HUD_W - 20
    pad = _PAD

    # Fondo estilo Stardew (madera clara)
    pygame.draw.rect(pantalla, (222, 195, 150), (GRID_W, 0, HUD_W, WINDOW_H))
    
    # Borde oscuro tipo marco
    pygame.draw.rect(pantalla, (120, 85, 50), (GRID_W, 0, HUD_W, WINDOW_H), 4)

    # Línea separadora suave
    pygame.draw.line(pantalla, (160, 120, 80), (GRID_W, 0), (GRID_W, WINDOW_H), 2)

    gen_num = agente.evolution.generation
    layout  = HUDLayout(px, pw)

    # ── Header ────────────────────────────────────────────────────────────
    hx, hy, hw, hh = layout.next_section(_H_HEADER)
    _card(pantalla, hx, hy, hw, hh, radius=8)
    _label(pantalla, fuentes, "AI SMART FARM",       hx + pad, hy + 12, C["accent"],  "md")
    _label(pantalla, fuentes, "Simulación autónoma",  hx + pad, hy + 30, C["txt_dim"], "xs")
    gen_txt   = f"Gen. {gen_num}"
    gen_w     = fuentes["xs"].size(gen_txt)[0]
    _label(pantalla, fuentes, gen_txt, hx + hw - pad - gen_w, hy + 16, C["txt_dim"], "xs")
    score_txt = f"Score: {state.score}"
    score_w   = fuentes["xs"].size(score_txt)[0]
    _label(pantalla, fuentes, score_txt, hx + hw - pad - score_w, hy + 30, C["accent2"], "xs")

    # ── Estación ──────────────────────────────────────────────────────────
    sx, sy, sw, sh = layout.next_section(_H_SEASON)
    season  = getattr(state, "season", "—")
    s_color = SEASON_COLORS.get(season, C["txt_mid"])
    _card(pantalla, sx, sy, sw, sh, radius=8)
    _section_title(pantalla, fuentes, "ESTACIÓN", sx + pad, sy + pad, sw - pad * 2)
    _label(pantalla, fuentes, season, sx + pad, sy + 32, s_color, "sm")
    day_in_season = getattr(state, "_season_mgr", None)
    if day_in_season and hasattr(day_in_season, "days_passed"):
        dp  = day_in_season.days_passed
        dps = day_in_season.days_per_season
        _bar(pantalla, sx + pad, sy + 50, sw - pad * 2, 8, dp / dps, s_color, s_color)
        _label(pantalla, fuentes, f"Día {dp} de {dps}", sx + pad, sy + 62, C["txt_dim"], "xs")

    # ── Evento ────────────────────────────────────────────────────────────
    ex, ey, ew, eh = layout.next_section(_H_EVENT)
    event_name = state.active_effects.get("event_name", "")
    evt_label  = event_name.replace("_", " ").capitalize() if event_name else "Despejado"
    evt_color  = EVENT_COLORS.get(event_name, C["accent2"]) if event_name else C["txt_mid"]
    _card(pantalla, ex, ey, ew, eh, radius=8)
    _section_title(pantalla, fuentes, "EVENTO", ex + pad, ey + pad, ew - pad * 2)
    pygame.draw.circle(pantalla, evt_color, (ex + pad + 5, ey + 38), 5)
    _label(pantalla, fuentes, evt_label, ex + pad + 18, ey + 31, evt_color, "sm")

    # ── Agente ────────────────────────────────────────────────────────────
    ax, ay, aw, ah = layout.next_section(_H_AGENT)

    energy_pct = agente.energy / max(agente.max_energy, 1)
    if agente.resting:
        estado_txt, estado_col = "Descansando", C["energy_mid"]
    elif agente.current_path:
        estado_txt, estado_col = "En ruta",     C["accent"]
    elif agente.goal:
        estado_txt, estado_col = "Trabajando",  C["energy_hi"]
    else:
        estado_txt, estado_col = "Explorando",  C["accent2"]

    goal = agente.goal
    goal_str   = f"({goal.x},{goal.y})" if (goal and hasattr(goal, "x")) else "—"
    accion_str = GOAL_LABELS.get(agente.strategy, str(agente.strategy) if agente.strategy else "—")
    path_len   = len(agente.current_path) if agente.current_path else 0
    path_str   = f"{path_len} pasos" if path_len > 0 else "—"
    cosechas   = agente.life_stats.get("harvests", 0)
    inv_items  = len(state.farmer_inventory)
    inv_str    = f"{inv_items} items" if inv_items > 0 else "vacío"

    _card(pantalla, ax, ay, aw, ah, radius=8)
    _section_title(pantalla, fuentes, "AGENTE", ax + pad, ay + pad, aw - pad * 2)

    # Sistema de 2 columnas con offsets fijos para alineación perfecta
    col1_x = ax + pad           # columna izquierda — etiquetas
    col2_x = ax + aw // 2 + 6  # columna derecha — etiquetas
    val1_x = col1_x + 60       # valores col izquierda (>= ancho de "Cosechas" ~48px)
    val2_x = col2_x + 60        # valores col derecha  (>= ancho de "Acc." ~26px)
    row_h  = _ROW_H
    r0y    = ay + 32

    # Fila 0: Pos | Estado
    _label(pantalla, fuentes, "Pos",                    col1_x, r0y,           C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"({agente.x},{agente.y})", val1_x, r0y,         C["txt_hi"],  "xs")
    _label(pantalla, fuentes, estado_txt,                col2_x, r0y,          estado_col,   "xs")

    # Fila 1: Goal | Acción
    _label(pantalla, fuentes, "Goal",      col1_x, r0y + row_h,     C["txt_dim"], "xs")
    _label(pantalla, fuentes, goal_str,    val1_x, r0y + row_h,     C["txt_hi"],  "xs")
    _label(pantalla, fuentes, "Acc.",      col2_x, r0y + row_h,     C["txt_dim"], "xs")
    _label(pantalla, fuentes, accion_str,  val2_x, r0y + row_h,     C["accent"],  "xs")

    # Fila 2: Barra de energía
    bar_row_y = r0y + row_h * 2
    _label(pantalla, fuentes, "Energía", col1_x, bar_row_y, C["txt_dim"], "xs")
    bar_x = col1_x + 60
    bar_w = aw - pad * 2 - 90
    _bar(pantalla, bar_x, bar_row_y + 3, bar_w, 10, energy_pct,
         C["energy_hi"], C["energy_lo"], C["energy_mid"])
    pct_txt = f"{int(energy_pct * 100)}%"
    _label(pantalla, fuentes, pct_txt,
           ax + aw - pad - fuentes["xs"].size(pct_txt)[0], bar_row_y, C["txt_mid"], "xs")

    # Fila 3: Valores energía | Path
    r3y = bar_row_y + 20
    _label(pantalla, fuentes, f"{agente.energy:.0f}/{agente.max_energy:.0f}",
           col1_x, r3y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, "Path",   col2_x, r3y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, path_str, val2_x, r3y, C["txt_hi"],  "xs")

    # Fila 4: Cosechas | Inventario
    r4y = r3y + row_h
    _label(pantalla, fuentes, "Cosechas",    col1_x, r4y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(cosechas), val1_x, r4y, C["accent2"], "xs")
    _label(pantalla, fuentes, "Inv.",        col2_x, r4y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, inv_str,       val2_x, r4y, C["accent2"], "xs")

    # ── Genética ──────────────────────────────────────────────────────────
    gx, gy, gw, gh = layout.next_section(_H_GENETICS)
    g = agente.genes
    _card(pantalla, gx, gy, gw, gh, radius=8)
    _section_title(pantalla, fuentes, f"GENÉTICA  —  Gen {gen_num}", gx + pad, gy + pad, gw - pad * 2)

    gene_stats = [
        ("E.Max",  f"{g.energy_max:.0f}",          _gene_pct(g.energy_max,         "energy_max")),
        ("Cons.",  f"{g.energy_consumption:.2f}",   _gene_pct(g.energy_consumption, "energy_consumption")),
        ("Rest.",  f"{g.rest_efficiency:.2f}",      _gene_pct(g.rest_efficiency,    "rest_efficiency")),
        ("Expl.",  f"{g.exploration_rate:.2f}",     _gene_pct(g.exploration_rate,   "exploration_rate")),
        ("Agua",   f"{g.water_efficiency:.1f}",     _gene_pct(g.water_efficiency,   "water_efficiency")),
        ("Riesgo", f"{g.risk_tolerance:.2f}",       _gene_pct(g.risk_tolerance,     "risk_tolerance")),
    ]
    gene_col_w  = (gw - pad * 2) // 2
    gene_row_h  = 30
    gene_row0_y = gy + 30

    for i, (lbl, val, pct) in enumerate(gene_stats):
        col = i % 2
        row = i // 2
        bx  = gx + pad + col * gene_col_w
        by  = gene_row0_y + row * gene_row_h
        _label(pantalla, fuentes, lbl, bx,      by, C["txt_dim"], "xs")
        _label(pantalla, fuentes, val, bx + 40, by, C["txt_hi"],  "xs")
        _bar(pantalla, bx, by + 12, gene_col_w - 10, 5, pct, C["accent"], C["accent"], None)

    # ── Evolución ─────────────────────────────────────────────────────────
    vx, vy, vw, vh = layout.next_section(_H_EVOLUTION)
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

    evo_col1_x = vx + pad
    evo_col2_x = vx + vw // 2
    evo_val1_x = evo_col1_x + 50
    evo_val2_x = evo_col2_x + 50

    elite_count = len(evo.elite_genes)
    evo_title   = f"EVOLUCIÓN  —  {elite_count} elite{'s' if elite_count != 1 else ''}"

    _card(pantalla, vx, vy, vw, vh, radius=8)
    _section_title(pantalla, fuentes, evo_title, vx + pad, vy + pad, vw - pad * 2)

    _label(pantalla, fuentes, "Gen.",              evo_col1_x, vy + 34, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(gen_num),        evo_val1_x, vy + 34, C["txt_hi"],  "xs")
    _label(pantalla, fuentes, "Actual",             evo_col2_x, vy + 34, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"{last_fitness:.1f}", evo_val2_x, vy + 34, C["txt_hi"], "xs")

    _label(pantalla, fuentes, "Mejor",              evo_col1_x, vy + 52, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"{best_fitness:.1f}", evo_val1_x + 4, vy + 52, C["accent2"], "xs")
    _label(pantalla, fuentes, "Tend.",               evo_col2_x, vy + 52, C["txt_dim"], "xs")
    _label(pantalla, fuentes, trend,                  evo_val2_x, vy + 52, trend_col,   "sm")

    # Sparkline de fitness
    history = list(evo.fitness_history[-15:])
    if len(history) >= 2:
        spark_x = vx + pad
        spark_y = vy + vh - 18
        spark_w = vw - pad * 2
        spark_h = 12

        max_f  = max(history) if max(history) > 0 else 1
        points = []
        for j, f in enumerate(history):
            px_s = spark_x + int(j / (len(history) - 1) * spark_w)
            py_s = spark_y + spark_h - int(f / max_f * spark_h)
            points.append((px_s, py_s))

        if len(points) >= 2:
            pygame.draw.lines(pantalla, C["accent"], False, points, 1)
            pygame.draw.circle(pantalla, C["accent2"], points[-1], 2)

    # ── Cultivos ──────────────────────────────────────────────────────────
    cx, cy_s, cw, ch = layout.next_section(_H_CROPS)
    fase_counts = {0: 0, 1: 0, 2: 0}
    for crop in state.crops:
        fase_counts[crop.fase] = fase_counts.get(crop.fase, 0) + 1
    total = len(state.crops)

    crop_row_h  = 18
    crop_row0_y = cy_s + 28

    _card(pantalla, cx, cy_s, cw, ch, radius=8)
    _section_title(pantalla, fuentes, f"CULTIVOS  ({total} total)", cx + pad, cy_s + pad, cw - pad * 2)
    for i, (fase, label) in enumerate(CROP_PHASE_LABELS.items()):
        bx  = cx + pad
        by  = crop_row0_y + i * crop_row_h
        cnt = fase_counts.get(fase, 0)
        pygame.draw.circle(pantalla, CROP_PHASE_COLORS[fase], (bx + 4, by + 6), 4)
        _label(pantalla, fuentes, label, bx + 14, by, C["txt_mid"], "xs")
        cnt_w = fuentes["xs"].size(str(cnt))[0]
        _label(pantalla, fuentes, str(cnt), cx + cw - pad - cnt_w, by, C["txt_hi"], "xs")
        if total > 0:
            _bar(pantalla, bx + 14, by + 12, cw - pad * 2 - 14, 5,
                 cnt / total, CROP_PHASE_COLORS[fase], CROP_PHASE_COLORS[fase])

    # ── Simulación ────────────────────────────────────────────────────────
    smx, smy, smw, smh = layout.next_section(_H_SIM)
    visited     = len(agente.memory.get("visited_tiles", set()))
    total_tiles = 80 * 65
    inventory   = len(state.farmer_inventory)

    sim_col1_x = smx + pad
    sim_col2_x = smx + smw // 2 + 6
    sim_val1_x = sim_col1_x + 50
    sim_val2_x = sim_col2_x + 50

    _card(pantalla, smx, smy, smw, smh, radius=8)
    _section_title(pantalla, fuentes, "SIMULACIÓN", smx + pad, smy + pad, smw - pad * 2)

    _label(pantalla, fuentes, "Tick",          sim_col1_x, smy + 34, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(state.tick), sim_val1_x, smy + 34, C["txt_hi"],  "sm")
    _label(pantalla, fuentes, "Gen.",           sim_col2_x, smy + 34, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(gen_num),     sim_val2_x, smy + 34, C["txt_mid"], "sm")

    inv_str2  = f"{inventory} items"
    tiles_str = f"{visited}/{total_tiles}"
    _label(pantalla, fuentes, "Inv.",    sim_col1_x, smy + 52, C["txt_dim"], "xs")
    _label(pantalla, fuentes, inv_str2,  sim_val1_x, smy + 52, C["txt_mid"], "xs")
    _label(pantalla, fuentes, "Tiles",   sim_col2_x, smy + 52, C["txt_dim"], "xs")
    _label(pantalla, fuentes, tiles_str, sim_val2_x, smy + 52, C["txt_mid"], "xs")
