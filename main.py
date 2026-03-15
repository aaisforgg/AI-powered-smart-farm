import pygame
import random

from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from core.pipeline import Pipeline
from core.steps import tick_agent, tick_crops, tick_season, tick_events, tick_counter
from agent.agent import Agent
from entities.crop import Crop
from simulation.season_manager import SeasonManager
from simulation.event_manager import EventManager


# ── Layout ────────────────────────────────────────────────────────────────────
CELDA_PX  = 12
GRID_COLS = 80
GRID_ROWS = 65
GRID_W    = GRID_COLS * CELDA_PX   # 960
GRID_H    = GRID_ROWS * CELDA_PX   # 780
HUD_W     = 290
WINDOW_W  = GRID_W + HUD_W         # 1250
WINDOW_H  = GRID_H                 # 780

# ── Paleta de tiles ───────────────────────────────────────────────────────────
COLORES = {
    "pasto":      (118, 186,  27),
    "agua":       ( 74, 163, 223),
    "acantilado": (142, 112,  72),
    "edificio":   (180,  70,  50),
    "cultivo":    (220, 190,  50),
    "puente":     (150, 100,  50),
    "puerta":     (200, 160,  80),
    "casa":       (200, 200, 255),
}

CROP_COLORS = {
    0: (180, 140,  20),
    1: ( 80, 200,  80),
    2: (255,  80,  80),
}

SEASON_TINTS = {
    "Invierno":  (150, 200, 255,  60),
    "Verano":    (255, 200,   0,  25),
    "Otoño":     (180, 100,   0,  40),
    "Primavera": (  0, 200,  80,  15),
}

EVENT_TINTS = {
    "sequia":             (180,  80,   0,  60),
    "tormenta":           ( 50,  50, 150,  80),
    "nevada":             (200, 200, 255,  70),
    "inundacion":         (  0,  50, 180,  70),
    "plaga":              (  0, 150,   0,  60),
    "gran_deslave":       (100,  60,   0,  80),
    "nevada_paralizante": (200, 200, 255, 110),
    "plaga_de_insectos":  (  0, 180,   0,  80),
}

# ── Paleta HUD ────────────────────────────────────────────────────────────────
C = {
    "bg":           ( 10,  12,  28),
    "panel":        ( 18,  22,  48),
    "card":         ( 26,  32,  64),
    "card_border":  ( 48,  58, 110),
    "accent":       ( 80, 160, 255),
    "accent2":      (120, 220, 160),
    "divider":      ( 38,  46,  90),
    "txt_hi":       (230, 235, 255),
    "txt_mid":      (155, 165, 210),
    "txt_dim":      ( 80,  92, 148),
    "energy_hi":    ( 80, 220, 120),
    "energy_mid":   (240, 200,  60),
    "energy_lo":    (220,  70,  60),
}

SEASON_COLORS = {
    "Primavera": ( 80, 220, 100),
    "Verano":    (255, 200,  50),
    "Otoño":     (220, 120,  40),
    "Invierno":  (150, 200, 255),
}

SEASON_ICONS = {
    "Primavera": "☀",
    "Verano":    "🌞",
    "Otoño":     "🍂",
    "Invierno":  "❄",
}

EVENT_COLORS = {
    "sequia":             (220, 100,  40),
    "tormenta":           (100, 120, 255),
    "nevada":             (180, 210, 255),
    "inundacion":         ( 50, 130, 220),
    "plaga":              ( 80, 200,  80),
    "gran_deslave":       (150, 100,  50),
    "nevada_paralizante": (200, 220, 255),
    "plaga_de_insectos":  (120, 200,  60),
}

GOAL_LABELS = {
    "HARVEST":  "Cosechar",
    "WATER":    "Regar",
    "PLANT":    "Plantar",
    "EXPLORE":  "Explorar",
    "REST":     "Descansar",
    "GO_HOME":  "Ir a casa",
    None:       "—",
}

CROP_PHASE_LABELS = {0: "Semilla", 1: "Creciendo", 2: "Lista"}
CROP_PHASE_COLORS = {0: (180, 140, 20), 1: (80, 200, 80), 2: (255, 80, 80)}


# ── Utilidades de carga ───────────────────────────────────────────────────────
def cargar_mapa_logico():
    grid = []
    for y, fila in enumerate(MAP_DATA):
        nodos_fila = []
        for x, tile_id in enumerate(fila):
            nombre = TILE_TYPES.get(tile_id, "pasto")
            nodos_fila.append(Node(x, y, tile_id, nombre))
        grid.append(nodos_fila)
    return grid


def posicion_random_valida(grid):
    tiles_prohibidos = {"agua", "acantilado", "cultivo", "puerta"}
    alto  = len(grid)
    ancho = len(grid[0])
    while True:
        x = random.randint(0, ancho - 1)
        y = random.randint(0, alto - 1)
        tile = grid[y][x]
        if tile.type_name not in tiles_prohibidos and tile.walkable:
            return x, y


def spawn_crops():
    return [
        Crop(50, 40),
        Crop(55, 42),
        Crop(22, 45),
        Crop(25, 50),
        Crop(62, 58),
    ]


# ── Partículas ────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto  = alto
        self.reset()

    def reset(self):
        self.x         = random.randint(0, self.ancho)
        self.y         = random.randint(-self.alto, 0)
        self.velocidad = random.randint(2, 6)

    def caer(self):
        self.y += self.velocidad
        if self.y > self.alto:
            self.reset()


# ── Helpers de dibujo HUD ─────────────────────────────────────────────────────
def _card(surf, x, y, w, h, radius=6):
    """Dibuja un card con fondo y borde redondeado."""
    pygame.draw.rect(surf, C["card"],        (x, y, w, h), border_radius=radius)
    pygame.draw.rect(surf, C["card_border"], (x, y, w, h), 1, border_radius=radius)


def _label(surf, fuentes, text, x, y, color, size="sm"):
    f = fuentes[size]
    s = f.render(text, True, color)
    surf.blit(s, (x, y))
    return s.get_width()


def _bar(surf, x, y, w, h, pct, color_hi, color_lo, color_mid=None):
    """Barra de progreso. pct en [0, 1]."""
    pct = max(0.0, min(1.0, pct))
    # track
    pygame.draw.rect(surf, C["divider"], (x, y, w, h), border_radius=3)
    if pct > 0:
        fill_w = max(2, int(w * pct))
        color = color_hi if pct > 0.5 else (color_mid or color_lo) if pct > 0.25 else color_lo
        pygame.draw.rect(surf, color, (x, y, fill_w, h), border_radius=3)
    # borde sutil
    pygame.draw.rect(surf, C["card_border"], (x, y, w, h), 1, border_radius=3)


def _section_title(surf, fuentes, text, x, y, w):
    """Línea de título de sección con separador."""
    _label(surf, fuentes, text, x, y, C["txt_dim"], "xs")
    pygame.draw.line(surf, C["divider"], (x, y + 14), (x + w, y + 14), 1)


# ── Dibujo del GRID ───────────────────────────────────────────────────────────
def dibujar_grid(pantalla, state, agente, celda_px, particulas):
    # Clip para que el tint no se pase al panel HUD
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

    # Agente: glow + círculo principal
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

    # Partículas
    if season == "Invierno" or event_name in ("tormenta", "nevada", "nevada_paralizante"):
        p_color = (240, 240, 255) if season == "Invierno" else (80, 80, 200)
        for p in particulas:
            p.caer()
            pygame.draw.line(pantalla, p_color, (p.x, p.y), (p.x, p.y + 3), 1)

    pantalla.set_clip(None)


# ── Dibujo del HUD ────────────────────────────────────────────────────────────
def dibujar_hud(pantalla, state, agente, fuentes):
    px   = GRID_W + 10     # x inicio panel
    pw   = HUD_W - 20      # ancho útil
    pad  = 10              # padding interno cards

    # Fondo panel
    pygame.draw.rect(pantalla, C["bg"], (GRID_W, 0, HUD_W, WINDOW_H))
    pygame.draw.line(pantalla, C["card_border"], (GRID_W, 0), (GRID_W, WINDOW_H), 1)

    # ── Header ──────────────────────────────────────────────────────────────
    _card(pantalla, px, 10, pw, 44, radius=8)
    _label(pantalla, fuentes, "AI SMART FARM", px + pad, 20, C["accent"], "md")
    _label(pantalla, fuentes, "Simulación autonoma", px + pad, 36, C["txt_dim"], "xs")

    cy = 66  # cursor y

    # ── Estación ─────────────────────────────────────────────────────────────
    season     = getattr(state, "season", "—")
    s_color    = SEASON_COLORS.get(season, C["txt_mid"])
    _card(pantalla, px, cy, pw, 52, radius=6)
    _section_title(pantalla, fuentes, "ESTACIÓN", px + pad, cy + pad, pw - pad * 2)
    _label(pantalla, fuentes, season, px + pad, cy + 26, s_color, "sm")
    # Indicador de día en la estación
    day_in_season = getattr(state, "_season_mgr", None)
    if day_in_season and hasattr(day_in_season, "days_passed"):
        dp  = day_in_season.days_passed
        dps = day_in_season.days_per_season
        pct = dp / dps
        _bar(pantalla, px + pad + 75, cy + 29, pw - pad * 2 - 75, 8,
             pct, s_color, s_color)
        _label(pantalla, fuentes, f"Día {dp}/{dps}", px + pw - pad - 52, cy + 28,
               C["txt_dim"], "xs")
    cy += 62

    # ── Evento ───────────────────────────────────────────────────────────────
    event_name = state.active_effects.get("event_name", "")
    evt_label  = event_name.replace("_", " ").capitalize() if event_name else "Despejado"
    evt_color  = EVENT_COLORS.get(event_name, C["accent2"]) if event_name else C["txt_mid"]
    _card(pantalla, px, cy, pw, 52, radius=6)
    _section_title(pantalla, fuentes, "EVENTO", px + pad, cy + pad, pw - pad * 2)
    dot_x = px + pad
    dot_y = cy + 32
    pygame.draw.circle(pantalla, evt_color, (dot_x + 4, dot_y), 4)
    _label(pantalla, fuentes, evt_label, dot_x + 14, dot_y - 8, evt_color, "sm")
    cy += 62

    # ── Agente ───────────────────────────────────────────────────────────────
    energy_pct = agente.energy / max(agente.max_energy, 1)
    goal_str   = GOAL_LABELS.get(agente.goal, str(agente.goal) if agente.goal else "—")
    _card(pantalla, px, cy, pw, 104, radius=6)
    _section_title(pantalla, fuentes, "AGENTE", px + pad, cy + pad, pw - pad * 2)
    # Pos + Goal
    _label(pantalla, fuentes, f"Pos", px + pad, cy + 26, C["txt_dim"], "xs")
    _label(pantalla, fuentes, f"({agente.x}, {agente.y})", px + pad + 22, cy + 26, C["txt_hi"], "xs")
    _label(pantalla, fuentes, f"Goal", px + pw // 2, cy + 26, C["txt_dim"], "xs")
    _label(pantalla, fuentes, goal_str, px + pw // 2 + 28, cy + 26, C["accent"], "xs")
    # Estado
    estado_txt = "Descansando" if agente.resting else "Activo"
    estado_col = C["energy_mid"] if agente.resting else C["energy_hi"]
    _label(pantalla, fuentes, estado_txt, px + pad, cy + 42, estado_col, "xs")
    # Barra energía
    _label(pantalla, fuentes, "Energía", px + pad, cy + 60, C["txt_dim"], "xs")
    _bar(pantalla, px + pad + 50, cy + 60, pw - pad * 2 - 50, 10,
         energy_pct, C["energy_hi"], C["energy_lo"], C["energy_mid"])
    pct_txt = f"{int(energy_pct * 100)}%"
    _label(pantalla, fuentes, pct_txt, px + pw - pad - 28, cy + 60, C["txt_mid"], "xs")
    # Valor numérico energía
    _label(pantalla, fuentes, f"{agente.energy:.0f} / {agente.max_energy:.0f}",
           px + pad, cy + 78, C["txt_dim"], "xs")
    cy += 114

    # ── Genética ──────────────────────────────────────────────────────────────
    g = agente.genes
    gen_num = agente.evolution.generation
    _card(pantalla, px, cy, pw, 110, radius=6)
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
        by  = cy + 26 + row * 30
        _label(pantalla, fuentes, lbl, bx, by, C["txt_dim"], "xs")
        _label(pantalla, fuentes, val, bx + 32, by, C["txt_hi"], "xs")
        # mini barra relativa (visual de comparación)
        _bar(pantalla, bx + 70, by + 2, col_w - 78, 7, 0.5, C["accent"], C["accent"], None)
    cy += 120

    # ── Cultivos ──────────────────────────────────────────────────────────────
    fase_counts = {0: 0, 1: 0, 2: 0}
    for crop in state.crops:
        fase_counts[crop.fase] = fase_counts.get(crop.fase, 0) + 1
    total = len(state.crops)

    _card(pantalla, px, cy, pw, 90, radius=6)
    _section_title(pantalla, fuentes, f"CULTIVOS  ({total} total)", px + pad, cy + pad, pw - pad * 2)
    for i, (fase, label) in enumerate(CROP_PHASE_LABELS.items()):
        bx  = px + pad
        by  = cy + 26 + i * 20
        cnt = fase_counts.get(fase, 0)
        pygame.draw.circle(pantalla, CROP_PHASE_COLORS[fase], (bx + 4, by + 5), 4)
        _label(pantalla, fuentes, label, bx + 14, by, C["txt_mid"], "xs")
        _label(pantalla, fuentes, str(cnt), bx + 80, by, C["txt_hi"], "xs")
        if total > 0:
            _bar(pantalla, bx + 96, by + 2, pw - pad * 2 - 96, 7,
                 cnt / total, CROP_PHASE_COLORS[fase], CROP_PHASE_COLORS[fase])
    cy += 100

    # ── Simulación ────────────────────────────────────────────────────────────
    _card(pantalla, px, cy, pw, 52, radius=6)
    _section_title(pantalla, fuentes, "SIMULACIÓN", px + pad, cy + pad, pw - pad * 2)
    _label(pantalla, fuentes, "Tick", px + pad, cy + 26, C["txt_dim"], "xs")
    _label(pantalla, fuentes, str(state.tick), px + pad + 28, cy + 26, C["txt_hi"], "xs")
    _label(pantalla, fuentes, "Vel.", px + pw // 2, cy + 26, C["txt_dim"], "xs")
    _label(pantalla, fuentes, "10 t/s", px + pw // 2 + 24, cy + 26, C["txt_mid"], "xs")


# ── Función de dibujo principal ───────────────────────────────────────────────
def dibujar(pantalla, state, agente, celda_px, particulas, fuentes):
    pantalla.fill(C["bg"])
    dibujar_grid(pantalla, state, agente, celda_px, particulas)
    dibujar_hud(pantalla, state, agente, fuentes)
    pygame.display.flip()


def debug_print(state, agente):
    print(f"--- Tick {state.tick} ---")
    print(f"Pos: ({agente.x}, {agente.y}) | Energía: {agente.energy:.1f} | Resting: {agente.resting}")
    print(f"Goal: {agente.goal} | Path: {len(agente.current_path)}")
    if hasattr(agente, 'genes'):
        g = agente.genes
        print(f"Genes → emax:{g.energy_max:.1f} econs:{g.energy_consumption:.2f} "
              f"rest:{g.rest_efficiency:.2f} expl:{g.exploration_rate:.2f}")
    if state.active_effects:
        print(f"Efectos activos: {state.active_effects}")
    print()


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("AI Smart Farm")

    mundo = cargar_mapa_logico()
    spawn_x, spawn_y = posicion_random_valida(mundo)
    print(f"Spawn del agente: ({spawn_x}, {spawn_y})")

    agente    = Agent(spawn_x, spawn_y, crop_factory=spawn_crops)
    crops     = spawn_crops()
    season_mgr = SeasonManager(days_per_season=30)
    event_mgr  = EventManager()

    state = GameState(
        farmer_pos=(agente.x, agente.y),
        grid=mundo,
        crops=crops,
        _agent_ref=agente,
        _season_mgr=season_mgr,
        _event_mgr=event_mgr,
    )

    pipeline = Pipeline(
        tick_agent,
        tick_crops,
        tick_season,
        tick_events,
        tick_counter,
    )

    fuentes = {
        "lg": pygame.font.SysFont("Segoe UI", 18, bold=True),
        "md": pygame.font.SysFont("Segoe UI", 15, bold=True),
        "sm": pygame.font.SysFont("Segoe UI", 13, bold=False),
        "xs": pygame.font.SysFont("Segoe UI", 11, bold=False),
    }

    particulas = [Particle(GRID_W, GRID_H) for _ in range(120)]

    clock     = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        pipeline.run(state)
        debug_print(state, agente)
        dibujar(pantalla, state, agente, CELDA_PX, particulas, fuentes)
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
