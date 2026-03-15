import pygame

from rendering.theme import C
from rendering.grid_renderer import dibujar_grid
from rendering.hud_renderer import dibujar_hud


def render_frame(pantalla, state, agente, celda_px, particulas, fuentes):
    pantalla.fill(C["bg"])
    dibujar_grid(pantalla, state, agente, celda_px, particulas)
    dibujar_hud(pantalla, state, agente, fuentes)
    pygame.display.flip()
