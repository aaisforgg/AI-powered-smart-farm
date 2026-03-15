import pygame

from rendering.theme import C


def _card(surf, x, y, w, h, radius=6):
    pygame.draw.rect(surf, C["card"],        (x, y, w, h), border_radius=radius)
    pygame.draw.rect(surf, C["card_border"], (x, y, w, h), 1, border_radius=radius)


def _label(surf, fuentes, text, x, y, color, size="sm"):
    f = fuentes[size]
    s = f.render(text, True, color)
    surf.blit(s, (x, y))
    return s.get_width()


def _bar(surf, x, y, w, h, pct, color_hi, color_lo, color_mid=None):
    pct = max(0.0, min(1.0, pct))
    pygame.draw.rect(surf, C["divider"], (x, y, w, h), border_radius=3)
    if pct > 0:
        fill_w = max(2, int(w * pct))
        color = color_hi if pct > 0.5 else (color_mid or color_lo) if pct > 0.25 else color_lo
        pygame.draw.rect(surf, color, (x, y, fill_w, h), border_radius=3)
    pygame.draw.rect(surf, C["card_border"], (x, y, w, h), 1, border_radius=3)


def _section_title(surf, fuentes, text, x, y, w):
    _label(surf, fuentes, text, x, y, C["txt_dim"], "xs")
    pygame.draw.line(surf, C["divider"], (x, y + 14), (x + w, y + 14), 1)
