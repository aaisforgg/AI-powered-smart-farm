import sys
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
from rendering import render_frame
from rendering.asset_manager import AssetManager
from rendering.theme import WINDOW_W, WINDOW_H, CELDA_PX, GRID_W, GRID_H
from rendering.particles import Particle


DEBUG_MODE = "--debug" in sys.argv


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
    tiles_prohibidos = {"agua", "acantilado", "cultivo", "puerta", "edificio"}
    # Zona central del mapa donde hay pasto y cultivos accesibles
    for _ in range(1000):
        x = random.randint(20, 60)
        y = random.randint(20, 55)
        tile = grid[y][x]
        if tile.type_name not in tiles_prohibidos and tile.walkable:
            return x, y
    return 35, 40 


def spawn_crops(grid, count=None):
    """Genera cultivos en posiciones aleatorias de tiles tipo 'cultivo'.

    Distribución de fases:
      30% fase 0 (semilla)   humedad 80-100
      40% fase 1 (creciendo) humedad 40-80
      30% fase 2 (listo)     humedad 20-60
    """
    if count is None:
        count = random.randint(8, 12)

    cultivo_tiles = [
        (tile.x, tile.y)
        for fila in grid
        for tile in fila
        if tile.type_name == "cultivo"
    ]

    if not cultivo_tiles:
        print("[WARN] spawn_crops: no hay tiles de tipo 'cultivo' en el mapa")
        return []

    count = min(count, len(cultivo_tiles))
    positions = random.sample(cultivo_tiles, count)

    crops = []
    for x, y in positions:
        c = Crop(x, y)
        r = random.random()
        if r < 0.30:
            c.fase    = 0
            c.humedad = random.uniform(80, 100)
        elif r < 0.70:
            c.fase    = 1
            c.humedad = random.uniform(40, 80)
        else:
            c.fase    = 2
            c.humedad = random.uniform(20, 60)
        crops.append(c)

    return crops


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("AI Smart Farm")

    assets = AssetManager(cell_size=CELDA_PX, grid_w=GRID_W, grid_h=GRID_H)
    assets.load_all()

    mundo = cargar_mapa_logico()
    spawn_x, spawn_y = posicion_random_valida(mundo)
    print(f"Spawn del agente: ({spawn_x}, {spawn_y})")
    assert mundo[spawn_y][spawn_x].walkable, (
        f"[ERROR] Spawn en tile no caminable: ({spawn_x}, {spawn_y}) "
        f"tipo='{mundo[spawn_y][spawn_x].type_name}'"
    )

    agente        = Agent(spawn_x, spawn_y, crop_factory=spawn_crops)
    agente.debug  = DEBUG_MODE
    crops         = spawn_crops(mundo)
    event_mgr  = EventManager()

    for fila in mundo:
        for nodo in fila:
            if nodo.type_name == "casa":
                agente.memory["home_tiles"].add((nodo.x, nodo.y))

    season_mgr = SeasonManager(days_per_season=120)

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
    clock      = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        pipeline.run(state)

        if len(state.crops) < 3:
            nuevos = spawn_crops(state.grid, count=5)
            state.crops.extend(nuevos)
            print(f"[Main] Repoblando cultivos: +{len(nuevos)} → total {len(state.crops)}")

        render_frame(pantalla, state, agente, CELDA_PX, particulas, fuentes, assets)
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
