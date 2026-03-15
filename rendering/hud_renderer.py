import pygame

from rendering.theme import (
    C, SEASON_COLORS, EVENT_COLORS, GOAL_LABELS,
    CROP_PHASE_LABELS, CROP_PHASE_COLORS,
    GRID_W, HUD_W, WINDOW_H,
)
from rendering.helpers import _card, _label, _bar, _section_title


def dibujar_hud(pantalla, state, agente, fuentes):
    px  = GRID_W + 10
    pw  = HUD_W - 20
    pad = 10

    pygame.draw.rect(pantalla, C["bg"], (GRID_W, 0, HUD_W, WINDOW_H))
    pygame.draw.line(pantalla, C["card_border"], (GRID_W, 0), (GRID_W, WINDOW_H), 1)

    gen_num = agente.evolution.generation

    _card(pantalla, px, 10, pw, 44, radius=8)
    _label(pantalla, fuentes, "AI SMART FARM", px + pad, 20, C["accent"], "md")
    _label(pantalla, fuentes, "Simulación autonoma", px + pad, 36, C["txt_dim"], "xs")
    gen_txt = f"Gen. {gen_num}"
    gen_w   = fuentes["xs"].size(gen_txt)[0]
    _label(pantalla, fuentes, gen_txt, px + pw - pad - gen_w, 22, C["txt_dim"], "xs")

    cy = 66

    season  = getattr(state, "season", "—")
    s_color = SEASON_COLORS.get(season, C["txt_mid"])
    _card(pantalla, px, cy, pw, 86, radius=6)
    _section_title(pantalla, fuentes, "ESTACIÓN", px + pad, cy + pad, pw - pad * 2)
    _label(pantalla, fuentes, season, px + pad, cy + 34, s_color, "sm")
    day_in_season = getattr(state, "_season_mgr", None)
    if day_in_season and hasattr(day_in_season, "days_passed"):
        dp  = day_in_season.days_passed
        dps = day_in_season.days_per_season
        _bar(pantalla, px + pad, cy + 56, pw - pad * 2, 10, dp / dps, s_color, s_color)
        _label(pantalla, fuentes, f"Día {dp} de {dps}", px + pad, cy + 72, C["txt_dim"], "xs")
    cy += 96

    event_name = state.active_effects.get("event_name", "")
    evt_label  = event_name.replace("_", " ").capitalize() if event_name else "Despejado"
    evt_color  = EVENT_COLORS.get(event_name, C["accent2"]) if event_name else C["txt_mid"]
    _card(pantalla, px, cy, pw, 86, radius=6)
    _section_title(pantalla, fuentes, "EVENTO", px + pad, cy + pad, pw - pad * 2)
    pygame.draw.circle(pantalla, evt_color, (px + pad + 5, cy + 54), 5)
    _label(pantalla, fuentes, evt_label, px + pad + 18, cy + 44, evt_color, "sm")
    cy += 96

    energy_pct = agente.energy / max(agente.max_energy, 1)
    goal_str   = GOAL_LABELS.get(agente.strategy, str(agente.strategy) if agente.strategy else "—")
    _card(pantalla, px, cy, pw, 138, radius=6)
    _section_title(pantalla, fuentes, "AGENTE", px + pad, cy + pad, pw - pad * 2)
    _label(pantalla, fuentes, "Pos",  px + pad, cy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"({agente.x}, {agente.y})", px + pad + 24, cy + 32, C["txt_hi"], "xs")
    _label(pantalla, fuentes, "Goal", px + pw // 2, cy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, goal_str, px + pw // 2 + 28, cy + 32, C["accent"], "xs")
    estado_txt = "Descansando" if agente.resting else "Activo"
    estado_col = C["energy_mid"] if agente.resting else C["energy_hi"]
    _label(pantalla, fuentes, estado_txt, px + pad, cy + 54, estado_col, "xs")
    _label(pantalla, fuentes, "Energía", px + pad, cy + 76, C["txt_dim"], "xs")
    _bar(pantalla, px + pad + 52, cy + 74, pw - pad * 2 - 52, 12,
         energy_pct, C["energy_hi"], C["energy_lo"], C["energy_mid"])
    pct_txt = f"{int(energy_pct * 100)}%"
    _label(pantalla, fuentes, pct_txt, px + pw - pad - fuentes["xs"].size(pct_txt)[0], cy + 76, C["txt_mid"], "xs")
    _label(pantalla, fuentes, f"{agente.energy:.0f} / {agente.max_energy:.0f}", px + pad, cy + 100, C["txt_dim"], "xs")
    cosechas = agente.life_stats.get("harvests", 0)
    _label(pantalla, fuentes, f"Cosechas:  {cosechas}", px + pw // 2, cy + 100, C["txt_dim"], "xs")
    cy += 148

    g = agente.genes
    _card(pantalla, px, cy, pw, 144, radius=6)
    _section_title(pantalla, fuentes, f"GENÉTICA  —  Gen {gen_num}", px + pad, cy + pad, pw - pad * 2)
    stats = [
        ("E.Max",  f"{g.energy_max:.0f}"),
        ("Cons.",  f"{g.energy_consumption:.2f}"),
        ("Rest.",  f"{g.rest_efficiency:.2f}"),
        ("Expl.",  f"{g.exploration_rate:.2f}"),
    ]
    col_w = (pw - pad * 2) // 2
    for i, (lbl, val) in enumerate(stats):
        col = i % 2
        row = i // 2
        bx  = px + pad + col * col_w
        by  = cy + 32 + row * 52
        _label(pantalla, fuentes, lbl, bx, by, C["txt_dim"], "xs")
        _label(pantalla, fuentes, val, bx + 36, by, C["txt_hi"], "xs")
        _bar(pantalla, bx, by + 16, col_w - 8, 8, 0.5, C["accent"], C["accent"], None)
    cy += 154

    fase_counts = {0: 0, 1: 0, 2: 0}
    for crop in state.crops:
        fase_counts[crop.fase] = fase_counts.get(crop.fase, 0) + 1
    total = len(state.crops)

    _card(pantalla, px, cy, pw, 122, radius=6)
    _section_title(pantalla, fuentes, f"CULTIVOS  ({total} total)", px + pad, cy + pad, pw - pad * 2)
    for i, (fase, label) in enumerate(CROP_PHASE_LABELS.items()):
        bx  = px + pad
        by  = cy + 30 + i * 30
        cnt = fase_counts.get(fase, 0)
        pygame.draw.circle(pantalla, CROP_PHASE_COLORS[fase], (bx + 4, by + 6), 4)
        _label(pantalla, fuentes, label, bx + 14, by, C["txt_mid"], "xs")
        cnt_w = fuentes["xs"].size(str(cnt))[0]
        _label(pantalla, fuentes, str(cnt), px + pw - pad - cnt_w, by, C["txt_hi"], "xs")
        if total > 0:
            _bar(pantalla, bx + 14, by + 16, pw - pad * 2 - 14, 6,
                 cnt / total, CROP_PHASE_COLORS[fase], CROP_PHASE_COLORS[fase])
    cy += 132

    _card(pantalla, px, cy, pw, 78, radius=6)
    _section_title(pantalla, fuentes, "SIMULACIÓN", px + pad, cy + pad, pw - pad * 2)
    _label(pantalla, fuentes, "Tick", px + pad, cy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(state.tick), px + pad + 30, cy + 32, C["txt_hi"], "sm")
    _label(pantalla, fuentes, "Vel.", px + pw // 2, cy + 32, C["txt_dim"], "xs")
    _label(pantalla, fuentes, "10 t/s", px + pw // 2 + 28, cy + 32, C["txt_mid"], "sm")
