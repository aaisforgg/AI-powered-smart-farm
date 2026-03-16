import sys
import pygame
import random

from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from core.pipeline import Pipeline
from core.steps import tick_agent, tick_crops, tick_animals, tick_season, tick_events, tick_counter
from agent.agent import Agent
from entities.crop import Crop
from entities.animal import Animal
from simulation.season_manager import SeasonManager
from simulation.event_manager import EventManager
from rendering import render_frame
from rendering.asset_manager import AssetManager
from rendering.theme import WINDOW_W, WINDOW_H, CELDA_PX, GRID_W, GRID_H
from rendering.particles import Particle
from ui.start_screen import pantalla_inicio


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
    if count is None:
        count = random.randint(12, 18)

    cultivo_tiles = [
        (tile.x, tile.y)
        for fila in grid
        for tile in fila
        if tile.type_name == "cultivo"
    ]

    if not cultivo_tiles:
        return []

    count = min(count, len(cultivo_tiles))
    positions = random.sample(cultivo_tiles, count)

    crops = []
    for x, y in positions:
        c = Crop(x, y)
        c.fase = 0
        c.humedad = 100.0
        crops.append(c)

    return crops


def spawn_animals(grid, count=3):
    pasto_tiles = [
        (tile.x, tile.y)
        for fila in grid
        for tile in fila
        if tile.type_name == "pasto" and tile.walkable
    ]
    if not pasto_tiles:
        return []
    count = min(count, len(pasto_tiles))
    positions = random.sample(pasto_tiles, count)
    return [Animal(x, y) for x, y in positions]


def main():
    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.stop()

    pygame.mixer.music.load("assets/music/menu_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

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
    animals       = spawn_animals(mundo)
    event_mgr     = EventManager()

    for fila in mundo:
        for nodo in fila:
            if nodo.type_name == "casa":
                agente.memory["home_tiles"].add((nodo.x, nodo.y))

    season_mgr = SeasonManager()

    state = GameState(
        farmer_pos=(agente.x, agente.y),
        grid=mundo,
        crops=crops,
        animals=animals,
        season=season_mgr.current_season,
        _agent_ref=agente,
        _season_mgr=season_mgr,
        _event_mgr=event_mgr,
    )

    pipeline = Pipeline(
        tick_agent,
        tick_crops,
        tick_animals,
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

    pantalla_inicio(pantalla, fuentes, WINDOW_W, WINDOW_H)
    
    pygame.mixer.music.stop()

    pygame.mixer.music.load("assets/music/game_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    particulas    = [Particle(GRID_W, GRID_H) for _ in range(120)]
    clock         = pygame.time.Clock()
    ejecutando    = True
    paused        = False
    game_speed    = 10
    debug_visual  = False

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    paused = not paused
                    print(f"[Main] {'Pausado' if paused else 'Reanudado'}")
                elif evento.key == pygame.K_d:
                    debug_visual = not debug_visual
                    print(f"[Main] Debug visual: {'ON' if debug_visual else 'OFF'}")
                elif evento.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    game_speed = min(60, game_speed + 5)
                    print(f"[Main] Velocidad: {game_speed} t/s")
                elif evento.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    game_speed = max(1, game_speed - 5)
                    print(f"[Main] Velocidad: {game_speed} t/s")
                elif evento.key == pygame.K_r:
                    agente = Agent(spawn_x, spawn_y, crop_factory=spawn_crops)
                    agente.debug = DEBUG_MODE
                    crops = spawn_crops(mundo)
                    for fila in mundo:
                        for nodo in fila:
                            if nodo.type_name == "casa":
                                agente.memory["home_tiles"].add((nodo.x, nodo.y))
                    state.crops = crops
                    state.animals = spawn_animals(mundo)
                    state._agent_ref = agente
                    state.tick = 0
                    state.generation = 0
                    state.score = 0
                    state.active_effects.clear()
                    print("[Main] Reset completo")

        if not paused:
            pipeline.run(state)

        render_frame(pantalla, state, agente, CELDA_PX, particulas, fuentes, assets, debug_visual)
        clock.tick(game_speed)

    pygame.quit()


if __name__ == "__main__":
    main()
