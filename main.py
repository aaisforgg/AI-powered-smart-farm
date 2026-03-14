import pygame
import random

from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from agent.agent import Agent
from entities.crop import Crop
from pathfinding.astar import AStarPathfinder


def cargar_mapa():
    grid = []
    for y, fila in enumerate(MAP_DATA):
        nodos_fila = []
        for x, tile_id in enumerate(fila):
            nombre = TILE_TYPES.get(tile_id, "pasto")
            nodos_fila.append(Node(x, y, tile_id, nombre))
        grid.append(nodos_fila)
    return grid


def posicion_random_valida(grid):
    alto = len(grid)
    ancho = len(grid[0])

    while True:
        x = random.randint(0, ancho - 1)
        y = random.randint(0, alto - 1)

        nodo = grid[y][x]

        if nodo.type_name not in ["agua", "acantilado", "edificio"]:
            return x, y


def posicion_random_cultivo(grid):
    alto = len(grid)
    ancho = len(grid[0])

    while True:
        x = random.randint(0, ancho - 1)
        y = random.randint(0, alto - 1)

        nodo = grid[y][x]

        if nodo.type_name == "cultivo":
            return x, y


def main():

    pygame.init()

    celda_px = 12
    ancho = 80 * celda_px
    alto = 65 * celda_px

    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("AI Smart Farm")

    mundo = cargar_mapa()

    pathfinder = AStarPathfinder()

    # ==========================
    # SPAWN DEL AGENTE
    # ==========================

    spawn_x, spawn_y = posicion_random_valida(mundo)
    agente = Agent(spawn_x, spawn_y)

    # ==========================
    # CREAR CROPS
    # ==========================

    crops = []

    for _ in range(10):
        x, y = posicion_random_cultivo(mundo)
        crops.append(Crop(x, y))

    # ==========================
    # OBJETIVO PARA A*
    # ==========================

    objetivo = crops[0]

    # ==========================
    # CALCULAR PATH
    # ==========================

    path = pathfinder.find_path(
        agente.x,
        agente.y,
        objetivo.x,
        objetivo.y,
        mundo
    )

    # ==========================
    # GAME STATE
    # ==========================

    state = GameState(
        farmer_pos=(agente.x, agente.y),
        grid=mundo,
        crops=crops
    )

    colores = {
        "pasto":      (118, 186, 27),
        "agua":       (74, 163, 223),
        "acantilado": (142, 112, 72),
        "edificio":   (180, 70, 50),
        "cultivo":    (220, 190, 50),
        "puente":     (150, 100, 50),
        "puerta":     (200, 160, 80),
        "casa":       (200, 100, 100),
    }

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        pantalla.fill((0, 0, 0))

        # ==========================
        # MOVER AGENTE CON A*
        # ==========================

        if path and len(path) > 1:

            siguiente = path[1]

            agente.x = siguiente[0]
            agente.y = siguiente[1]

            path.pop(0)

        # ==========================
        # DIBUJAR MAPA
        # ==========================

        for fila in mundo:
            for nodo in fila:

                color = colores.get(nodo.type_name, (255, 255, 255))

                pygame.draw.rect(
                    pantalla,
                    color,
                    (
                        nodo.x * celda_px,
                        nodo.y * celda_px,
                        celda_px - 1,
                        celda_px - 1
                    )
                )

        # ==========================
        # DIBUJAR CROPS
        # ==========================

        for crop in crops:

            pygame.draw.rect(
                pantalla,
                (0, 200, 0),
                (
                    crop.x * celda_px,
                    crop.y * celda_px,
                    celda_px - 1,
                    celda_px - 1
                )
            )

        # ==========================
        # DIBUJAR PATH
        # ==========================

        if path:

            for px, py in path:

                pygame.draw.rect(
                    pantalla,
                    (255, 0, 255),
                    (
                        px * celda_px,
                        py * celda_px,
                        celda_px - 1,
                        celda_px - 1
                    )
                )

        # ==========================
        # DIBUJAR AGENTE
        # ==========================

        pygame.draw.rect(
            pantalla,
            (255, 255, 255),
            (
                agente.x * celda_px,
                agente.y * celda_px,
                celda_px - 1,
                celda_px - 1
            )
        )

        pygame.display.flip()

        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()