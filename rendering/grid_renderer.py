import pygame

from rendering.theme import (
    COLORES, CROP_COLORS, SEASON_TINTS, EVENT_TINTS,
    GRID_W, GRID_H, CELDA_PX,
)


def dibujar_grid(pantalla, state, agente, celda_px, particulas, assets=None, debug_visual=False):
    pantalla.set_clip((0, 0, GRID_W, GRID_H))

    season = getattr(state, "season", "")
    event_name = state.active_effects.get("event_name", "")

    # — Fondo: imagen estacional o fallback de tiles por color —
    map_img = assets.get_map(season) if assets else None
    if map_img:
        pantalla.blit(map_img, (0, 0))
    else:
        for fila in state.grid:
            for nodo in fila:
                tile_img = assets.get_tile(nodo.type_name) if assets else None
                if tile_img:
                    pantalla.blit(tile_img, (nodo.x * celda_px, nodo.y * celda_px))
                else:
                    color = COLORES.get(nodo.type_name, (255, 255, 255))
                    pygame.draw.rect(pantalla, color,
                        (nodo.x * celda_px, nodo.y * celda_px, celda_px - 1, celda_px - 1))

    # — Overlay del mapa (estructura, caminos, etc.) —
    if assets:
        overlay_img = assets.get_map_overlay()
        if overlay_img:
            pantalla.blit(overlay_img, (0, 0))

    # — Tints de estación y evento —
    tint = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)
    if season in SEASON_TINTS:
        tint.fill(SEASON_TINTS[season])
        pantalla.blit(tint, (0, 0))
    if event_name in EVENT_TINTS:
        tint.fill(EVENT_TINTS[event_name])
        pantalla.blit(tint, (0, 0))

    # — Tiles visitados (debug) —
    if debug_visual and agente.memory.get("visited_tiles"):
        dbg_surf = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)
        for vx, vy in agente.memory["visited_tiles"]:
            pygame.draw.rect(dbg_surf, (255, 230, 40, 90),
                             (vx * celda_px, vy * celda_px, celda_px, celda_px))
        pantalla.blit(dbg_surf, (0, 0))

    # — Crops —
    for crop in state.crops:
        cx, cy = crop.pos
        crop_img = assets.get_crop(crop.fase) if assets else None
        if crop_img:
            pantalla.blit(crop_img, (cx * celda_px + 2, cy * celda_px + 2))
        else:
            color = CROP_COLORS.get(crop.fase, (255, 255, 255))
            pygame.draw.rect(pantalla, color,
                (cx * celda_px + 2, cy * celda_px + 2, celda_px - 4, celda_px - 4))

    # — Path del agente — gradiente cian (cerca) → amarillo (lejos) —
    if agente.current_path:
        path_list = list(agente.current_path)
        n         = max(len(path_list) - 1, 1)
        path_surf = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)
        prev = (agente.x, agente.y)
        for j, (px, py) in enumerate(path_list):
            t     = j / n                          # 0 = junto al agente, 1 = goal
            r_c   = int(60  + t * 195)             # 60  → 255
            g_c   = int(210 - t * 10)              # 210 → 200
            b_c   = int(255 - t * 215)             # 255 → 40
            a_c   = int(200 - t * 90)              # 200 → 110
            cx_px = px * celda_px + celda_px // 2
            cy_px = py * celda_px + celda_px // 2
            manhattan = abs(px - prev[0]) + abs(py - prev[1])
            if manhattan == 1:
                pygame.draw.circle(path_surf, (r_c, g_c, b_c, a_c), (cx_px, cy_px), 3)
            elif manhattan > 1:
                pygame.draw.circle(path_surf, (255, 40, 40, 220), (cx_px, cy_px), 4)
            prev = (px, py)
        pantalla.blit(path_surf, (0, 0))

    # — Marcador del goal —
    if agente.goal and hasattr(agente.goal, 'pos'):
        gx_px, gy_px = agente.goal.pos
        goal_surf = pygame.Surface((celda_px + 4, celda_px + 4), pygame.SRCALPHA)
        pygame.draw.rect(goal_surf, (255, 255, 0, 120), (0, 0, celda_px + 4, celda_px + 4), 2)
        pantalla.blit(goal_surf, (gx_px * celda_px - 2, gy_px * celda_px - 2))

    # — Agente —
    ax = agente.x * celda_px + celda_px // 2
    ay = agente.y * celda_px + celda_px // 2
    r  = celda_px // 2
    agent_img = assets.get_agent() if assets else None
    if agent_img:
        pantalla.blit(agent_img, (agente.x * celda_px, agente.y * celda_px))
    else:
        glow_surf = pygame.Surface((r * 6, r * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (80, 160, 255, 45), (r * 3, r * 3), r * 3)
        pygame.draw.circle(glow_surf, (80, 160, 255, 70), (r * 3, r * 3), r * 2)
        pantalla.blit(glow_surf, (ax - r * 3, ay - r * 3))
        pygame.draw.circle(pantalla, (200, 220, 255), (ax, ay), r)
        pygame.draw.circle(pantalla, ( 60, 130, 255), (ax, ay), r - 2)
        pygame.draw.circle(pantalla, (180, 210, 255), (ax, ay), r // 2)

    # — Partículas (nieve/lluvia) —
    if season == "Invierno" or event_name in ("tormenta", "nevada", "nevada_paralizante"):
        p_color = (240, 240, 255) if season == "Invierno" else (80, 80, 200)
        for p in particulas:
            p.caer()
            pygame.draw.line(pantalla, p_color, (p.x, p.y), (p.x, p.y + 3), 1)

    # — Controles (esquina inferior izquierda) —
    keys = [
        ("P", "Pausa"),
        ("D", "Debug"),
        ("+/-", "Vel"),
        ("R", "Reset"),
    ]
    item_w  = 72
    item_h  = 16
    margin  = 8
    total_w = len(keys) * item_w + (len(keys) - 1) * 4
    bx      = margin
    by      = GRID_H - item_h - margin

    # Fondo negro semitransparente detrás de todos los ítems
    bg = pygame.Surface((total_w + 8, item_h + 6), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    pantalla.blit(bg, (bx - 4, by - 3))

    font = pygame.font.SysFont("Segoe UI", 10, bold=False)
    font_key = pygame.font.SysFont("Segoe UI", 10, bold=True)
    x = bx
    for key, label in keys:
        # Fondo de tecla negro sólido con borde blanco
        key_w = font_key.size(key)[0] + 6
        key_surf = pygame.Surface((key_w, item_h), pygame.SRCALPHA)
        key_surf.fill((20, 20, 20, 230))
        pygame.draw.rect(key_surf, (200, 200, 200, 200), (0, 0, key_w, item_h), 1)
        pantalla.blit(key_surf, (x, by))
        key_txt = font_key.render(key, True, (240, 240, 240))
        pantalla.blit(key_txt, (x + 3, by + 3))

        lbl_txt = font.render(label, True, (200, 200, 200))
        pantalla.blit(lbl_txt, (x + key_w + 3, by + 3))
        x += item_w

    pantalla.set_clip(None)
