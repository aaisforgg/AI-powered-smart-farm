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
    alto = len(grid)
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


COLORES = {
    "pasto":      (118, 186, 27),
    "agua":       (74, 163, 223),
    "acantilado": (142, 112, 72),
    "edificio":   (180, 70, 50),
    "cultivo":    (220, 190, 50),
    "puente":     (150, 100, 50),
    "puerta":     (200, 160, 80),
    "casa":       (200, 200, 255),
}

CROP_COLORS = {
    0: (180, 140, 20),
    1: (80, 200, 80),
    2: (255, 80, 80),
}


def dibujar(pantalla, state, agente, celda_px):
    pantalla.fill((0, 0, 0))
    for fila in state.grid:
        for nodo in fila:
            color = COLORES.get(nodo.type_name, (255, 255, 255))
            pygame.draw.rect(pantalla, color,
                (nodo.x * celda_px, nodo.y * celda_px, celda_px - 1, celda_px - 1))
    for crop in state.crops:
        cx, cy = crop.pos
        color = CROP_COLORS.get(crop.fase, (255, 255, 255))
        pygame.draw.rect(pantalla, color,
            (cx * celda_px + 2, cy * celda_px + 2, celda_px - 4, celda_px - 4))
    centro = (agente.x * celda_px + celda_px // 2, agente.y * celda_px + celda_px // 2)
    pygame.draw.circle(pantalla, (255, 255, 255), centro, celda_px // 2)
    pygame.draw.circle(pantalla, (0, 0, 255), centro, celda_px // 3)
    pygame.display.flip()


def debug_print(state, agente):
    print(f"--- Tick {state.tick} ---")
    print(f"Pos: ({agente.x}, {agente.y}) | Energía: {agente.energy:.1f} | Resting: {agente.resting}")
    print(f"Goal: {agente.goal} | Path: {len(agente.current_path)}")
    if hasattr(agente, 'genes'):
        g = agente.genes
        print(f"Genes → emax:{g.energy_max:.1f} econs:{g.energy_consumption:.2f} rest:{g.rest_efficiency:.2f} expl:{g.exploration_rate:.2f}")
    if state.active_effects:
        print(f"Efectos activos: {state.active_effects}")
    print()


def main():
    pygame.init()
    celda_px = 12
    ancho = 80 * celda_px
    alto = 72 * celda_px
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("AI Smart Farm")

    mundo = cargar_mapa_logico()
    spawn_x, spawn_y = posicion_random_valida(mundo)
    print(f"Spawn del agente: ({spawn_x}, {spawn_y})")

    agente = Agent(spawn_x, spawn_y, crop_factory=spawn_crops)
    crops = spawn_crops()
    season_mgr = SeasonManager(days_per_season=30)
    event_mgr = EventManager()

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

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        pipeline.run(state)
        debug_print(state, agente)
        dibujar(pantalla, state, agente, celda_px)
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()