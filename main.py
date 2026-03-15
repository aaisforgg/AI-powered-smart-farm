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
        Crop(35, 45),
    ]


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("AI Smart Farm")

    assets = AssetManager(cell_size=CELDA_PX, grid_w=GRID_W, grid_h=GRID_H)
    assets.load_all()

    mundo = cargar_mapa_logico()
    spawn_x, spawn_y = posicion_random_valida(mundo)
    print(f"Spawn del agente: ({spawn_x}, {spawn_y})")

    agente     = Agent(spawn_x, spawn_y, crop_factory=spawn_crops)
    crops      = spawn_crops()
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
    clock      = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        pipeline.run(state)
        render_frame(pantalla, state, agente, CELDA_PX, particulas, fuentes, assets)
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
