import pygame

from rendering.theme import (
    COLORES, CROP_COLORS, SEASON_TINTS, EVENT_TINTS,
    GRID_W, GRID_H,
)


def dibujar_grid(pantalla, state, agente, celda_px, particulas):
    pantalla.set_clip((0, 0, GRID_W, GRID_H))

    for fila in state.grid:
        for nodo in fila:
            color = COLORES.get(nodo.type_name, (255, 255, 255))
            pygame.draw.rect(pantalla, color,
                (nodo.x * celda_px, nodo.y * celda_px, celda_px - 1, celda_px - 1))

    overlay = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)

    season = getattr(state, "season", "")
    if season in SEASON_TINTS:
        overlay.fill(SEASON_TINTS[season])
        pantalla.blit(overlay, (0, 0))

    event_name = state.active_effects.get("event_name", "")
    if event_name in EVENT_TINTS:
        overlay.fill(EVENT_TINTS[event_name])
        pantalla.blit(overlay, (0, 0))

    for crop in state.crops:
        cx, cy = crop.pos
        color = CROP_COLORS.get(crop.fase, (255, 255, 255))
        pygame.draw.rect(pantalla, color,
            (cx * celda_px + 2, cy * celda_px + 2, celda_px - 4, celda_px - 4))

    ax = agente.x * celda_px + celda_px // 2
    ay = agente.y * celda_px + celda_px // 2
    r  = celda_px // 2
    glow_surf = pygame.Surface((r * 6, r * 6), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (80, 160, 255, 45), (r * 3, r * 3), r * 3)
    pygame.draw.circle(glow_surf, (80, 160, 255, 70), (r * 3, r * 3), r * 2)
    pantalla.blit(glow_surf, (ax - r * 3, ay - r * 3))
    pygame.draw.circle(pantalla, (200, 220, 255), (ax, ay), r)
    pygame.draw.circle(pantalla, ( 60, 130, 255), (ax, ay), r - 2)
    pygame.draw.circle(pantalla, (180, 210, 255), (ax, ay), r // 2)

    if season == "Invierno" or event_name in ("tormenta", "nevada", "nevada_paralizante"):
        p_color = (240, 240, 255) if season == "Invierno" else (80, 80, 200)
        for p in particulas:
            p.caer()
            pygame.draw.line(pantalla, p_color, (p.x, p.y), (p.x, p.y + 3), 1)

    pantalla.set_clip(None)
