import pygame

from rendering.theme import (
    C, SEASON_COLORS, EVENT_COLORS, GOAL_LABELS,
    CROP_PHASE_LABELS, CROP_PHASE_COLORS,
    GRID_W, HUD_W, WINDOW_H,
)
from rendering.helpers import _card, _label, _bar, _section_title


GENE_RANGES = {
    "energy_max":         (150,  350),
    "energy_consumption": (0.1,  1.5),
    "rest_efficiency":    (0.5,  8.0),
    "exploration_rate":   (0.01, 1.0),
}


def _gene_pct(value, gene_name):
    lo, hi = GENE_RANGES[gene_name]
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


class HUDLayout:
    """Apila secciones verticalmente con padding automático."""

    def __init__(self, x, width, start_y=8, gap=10):
        self.x   = x
        self.w   = width
        self.y   = start_y
        self.gap = gap
        self.pad = 12

    def next_section(self, height):
        """Reserva espacio para una sección. Retorna (x, y, w, h)."""
        rect   = (self.x, self.y, self.w, height)
        self.y += height + self.gap
        return rect


# ── Constantes de layout ───────────────────────────────────────────────────────
# Sumas de altura: 46+76+56+144+134+74+100+72 = 702 + gaps(70) + start(8) = 780
_H_HEADER    = 46
_H_SEASON    = 76
_H_EVENT     = 56
_H_AGENT     = 144   # reducido 20px (espacio muerto eliminado)
_H_GENETICS  = 134   # +4
_H_EVOLUTION = 74    # +2
_H_CROPS     = 100   # +4
_H_SIM       = 72    # +10 (era muy apretado)

# Espaciado interno de tarjetas
_PAD        = 12   # padding izq/der/top de cada tarjeta
_TITLE_H    = 26   # altura reservada para título + divisor (_section_title dibuja en y+pad, línea en y+pad+14)
_ROW_H      = 22   # altura de fila estándar entre textos
_CONTENT_Y0 = _PAD + _TITLE_H - _PAD + 6   # = 32  — primera fila tras el divisor


def dibujar_hud(pantalla, state, agente, fuentes):
    px  = GRID_W + 10
    pw  = HUD_W - 20
    pad = _PAD

    pygame.draw.rect(pantalla, C["bg"], (GRID_W, 0, HUD_W, WINDOW_H))
    pygame.draw.line(pantalla, C["divider"], (GRID_W, 0), (GRID_W, WINDOW_H), 1)

    gen_num = agente.evolution.generation
    layout  = HUDLayout(px, pw)

    # ── Header ────────────────────────────────────────────────────────────
    hx, hy, hw, hh = layout.next_section(_H_HEADER)
    _card(pantalla, hx, hy, hw, hh, radius=8)
    _label(pantalla, fuentes, "AI SMART FARM",       hx + pad, hy + 12, C["accent"],  "md")
    _label(pantalla, fuentes, "Simulación autónoma",  hx + pad, hy + 29, C["txt_dim"], "xs")
    gen_txt = f"Gen. {gen_num}"
    gen_w   = fuentes["xs"].size(gen_txt)[0]
    _label(pantalla, fuentes, gen_txt, hx + hw - pad - gen_w, hy + 16, C["txt_dim"], "xs")

    # ── Estación ──────────────────────────────────────────────────────────
    sx, sy, sw, sh = layout.next_section(_H_SEASON)
    season  = getattr(state, "season", "—")
    s_color = SEASON_COLORS.get(season, C["txt_mid"])
    _card(pantalla, sx, sy, sw, sh, radius=8)
    _section_title(pantalla, fuentes, "ESTACIÓN", sx + pad, sy + pad, sw - pad * 2)
    _label(pantalla, fuentes, season, sx + pad, sy + 30, s_color, "sm")
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
    pygame.draw.circle(pantalla, evt_color, (ex + pad + 5, ey + 36), 5)
    _label(pantalla, fuentes, evt_label, ex + pad + 18, ey + 29, evt_color, "sm")

    # ── Agente ────────────────────────────────────────────────────────────
    ax, ay, aw, ah = layout.next_section(_H_AGENT)

    # Preparar datos
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
    val1_x = col1_x + 62        # valores col izquierda (>= ancho de "Cosechas" ~48px)
    val2_x = col2_x + 44        # valores col derecha  (>= ancho de "Acc." ~26px)
    row_h  = _ROW_H

    r0y = ay + 32   # primera fila (tras title+divider+gap)

    # Fila 0: Pos | Estado
    _label(pantalla, fuentes, "Pos",               col1_x, r0y + row_h * 0, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"({agente.x},{agente.y})", val1_x, r0y + row_h * 0, C["txt_hi"],  "xs")
    _label(pantalla, fuentes, estado_txt,            col2_x, r0y + row_h * 0, estado_col,  "xs")

    # Fila 1: Goal | Acción
    _label(pantalla, fuentes, "Goal",      col1_x, r0y + row_h * 1, C["txt_dim"], "xs")
    _label(pantalla, fuentes, goal_str,    val1_x, r0y + row_h * 1, C["txt_hi"],  "xs")
    _label(pantalla, fuentes, "Acc.",      col2_x, r0y + row_h * 1, C["txt_dim"], "xs")
    _label(pantalla, fuentes, accion_str,  val2_x, r0y + row_h * 1, C["accent"],  "xs")

    # Fila 2: Barra de energía (full width)
    bar_row_y = r0y + row_h * 2
    _label(pantalla, fuentes, "Energía", col1_x, bar_row_y, C["txt_dim"], "xs")
    bar_x = col1_x + 58
    bar_w = aw - pad * 2 - 58 - 30
    _bar(pantalla, bar_x, bar_row_y + 3, bar_w, 10, energy_pct,
         C["energy_hi"], C["energy_lo"], C["energy_mid"])
    pct_txt = f"{int(energy_pct * 100)}%"
    _label(pantalla, fuentes, pct_txt,
           ax + aw - pad - fuentes["xs"].size(pct_txt)[0], bar_row_y, C["txt_mid"], "xs")

    # Fila 3: Valores energía | Path  (desplazada manualmente por la barra)
    r3y = bar_row_y + 20
    _label(pantalla, fuentes, f"{agente.energy:.0f}/{agente.max_energy:.0f}",
           col1_x, r3y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, "Path",   col2_x, r3y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, path_str, val2_x, r3y, C["txt_hi"],  "xs")

    # Fila 4: Cosechas | Inventario
    r4y = r3y + row_h
    _label(pantalla, fuentes, "Cosechas", col1_x, r4y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(cosechas), val1_x, r4y, C["accent2"], "xs")
    _label(pantalla, fuentes, "Inv.",      col2_x, r4y, C["txt_dim"], "xs")
    _label(pantalla, fuentes, inv_str,     val2_x, r4y, C["accent2"], "xs")

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
    ]
    gene_col_w   = (gw - pad * 2) // 2  # ancho de cada columna de gen
    gene_row_h   = 50                    # altura por fila de gen (label + bar con espacio)
    gene_row0_y  = gy + 32              # primera fila tras título

    for i, (lbl, val, pct) in enumerate(gene_stats):
        col = i % 2
        row = i // 2
        bx  = gx + pad + col * gene_col_w
        by  = gene_row0_y + row * gene_row_h
        _label(pantalla, fuentes, lbl, bx,      by, C["txt_dim"], "xs")
        _label(pantalla, fuentes, val, bx + 38, by, C["txt_hi"],  "xs")
        _bar(pantalla, bx, by + 16, gene_col_w - 10, 7, pct, C["accent"], C["accent"], None)

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
    evo_col2_x = vx + vw // 2 + 6
    evo_val1_x = evo_col1_x + 38
    evo_val2_x = evo_col2_x + 46

    _card(pantalla, vx, vy, vw, vh, radius=8)
    _section_title(pantalla, fuentes, "EVOLUCIÓN", vx + pad, vy + pad, vw - pad * 2)

    # Fila 0: Gen | Fitness actual
    _label(pantalla, fuentes, "Gen.",         evo_col1_x, vy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(gen_num),   evo_val1_x, vy + 32, C["txt_hi"],  "xs")
    _label(pantalla, fuentes, "Actual",        evo_col2_x, vy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"{last_fitness:.1f}", evo_val2_x, vy + 32, C["txt_hi"], "xs")

    # Fila 1: Mejor | Tendencia
    _label(pantalla, fuentes, "Mejor",         evo_col1_x, vy + 54, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"{best_fitness:.1f}", evo_val1_x + 4, vy + 54, C["accent2"], "xs")
    _label(pantalla, fuentes, "Tend.",          evo_col2_x, vy + 54, C["txt_dim"], "xs")
    _label(pantalla, fuentes, trend,             evo_val2_x, vy + 54, trend_col,   "sm")

    # ── Cultivos ──────────────────────────────────────────────────────────
    cx, cy_s, cw, ch = layout.next_section(_H_CROPS)
    fase_counts = {0: 0, 1: 0, 2: 0}
    for crop in state.crops:
        fase_counts[crop.fase] = fase_counts.get(crop.fase, 0) + 1
    total = len(state.crops)

    crop_row_h  = 22   # espaciado entre filas de cultivo
    crop_row0_y = cy_s + 30

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
            _bar(pantalla, bx + 14, by + 14, cw - pad * 2 - 14, 5,
                 cnt / total, CROP_PHASE_COLORS[fase], CROP_PHASE_COLORS[fase])

    # ── Simulación ────────────────────────────────────────────────────────
    smx, smy, smw, smh = layout.next_section(_H_SIM)
    visited     = len(agente.memory.get("visited_tiles", set()))
    total_tiles = 80 * 65
    inventory   = len(state.farmer_inventory)

    sim_col1_x = smx + pad
    sim_col2_x = smx + smw // 2 + 6
    sim_val1_x = sim_col1_x + 32
    sim_val2_x = sim_col2_x + 38

    _card(pantalla, smx, smy, smw, smh, radius=8)
    _section_title(pantalla, fuentes, "SIMULACIÓN", smx + pad, smy + pad, smw - pad * 2)

    # Fila 0: Tick | Gen.
    _label(pantalla, fuentes, "Tick",          sim_col1_x, smy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(state.tick), sim_val1_x, smy + 32, C["txt_hi"],  "sm")
    _label(pantalla, fuentes, "Gen.",           sim_col2_x, smy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(gen_num),     sim_val2_x, smy + 32, C["txt_mid"], "sm")

    # Fila 1: Inventario | Tiles explorados
    inv_str   = f"{inventory} items"
    tiles_str = f"{visited}/{total_tiles}"
    _label(pantalla, fuentes, "Inv.",     sim_col1_x, smy + 48, C["txt_dim"], "xs")
    _label(pantalla, fuentes, inv_str,    sim_val1_x, smy + 48, C["txt_mid"], "xs")
    _label(pantalla, fuentes, "Tiles",    sim_col2_x, smy + 48, C["txt_dim"], "xs")
    _label(pantalla, fuentes, tiles_str,  sim_val2_x, smy + 48, C["txt_mid"], "xs")
