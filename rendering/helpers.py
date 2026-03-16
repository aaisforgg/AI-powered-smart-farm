import pygame

from rendering.theme import C


def _card(surface, x, y, w, h, radius=5):

    # fondo pergamino
    pygame.draw.rect(surface, (245, 226, 182), (x, y, w, h), border_radius=radius)

    # borde exterior oscuro
    pygame.draw.rect(surface, (120, 85, 50), (x, y, w, h), 2, border_radius=radius)

    # sombra ligera abajo
    pygame.draw.line(surface, (200, 170, 120), (x+2, y+h-2), (x+w-2, y+h-2), 1)
    

def _label(surf, fuentes, text, x, y, color, size="sm"):
    f = fuentes[size]
    s = f.render(text, True, color)
    surf.blit(s, (x, y))
    return s.get_width()


def _bar(surf, x, y, w, h, pct, color_hi, color_lo, color_mid=None):
    """Bar sin borde — look moderno con border_radius suave."""
    pct = max(0.0, min(1.0, pct))
    pygame.draw.rect(surf, C["divider"], (x, y, w, h), border_radius=4)
    if pct > 0:
        fill_w = max(2, int(w * pct))
        color = color_hi if pct > 0.5 else (color_mid or color_lo) if pct > 0.25 else color_lo
        pygame.draw.rect(surf, color, (x, y, fill_w, h), border_radius=4)


def _section_title(surface, fonts, text, x, y, width):

    font = fonts["sm"]

    surf = font.render(text, True, (90, 60, 30))
    rect = surf.get_rect()

    rect.centerx = x + width // 2
    rect.y = y

    surface.blit(surf, rect)

    # línea decorativa
    pygame.draw.line(surface, (170,130,80), (x, y+20), (x+width, y+20), 1)
    
def _label_center_x(pantalla, fuentes, texto, x, y, width, color, size="xs"):

    font = fuentes[size]

    surf = font.render(texto, True, color)
    rect = surf.get_rect()

    rect.centerx = x + width // 2
    rect.y = y

    pantalla.blit(surf, rect)