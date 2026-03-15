import pygame
import random

from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from agent.agent import Agent
from entities.crop import Crop


def cargar_mapa():

    grid = []

    for y, fila in enumerate(MAP_DATA):

        nodos_fila = []

        for x, tile_id in enumerate(fila):

            nombre = TILE_TYPES.get(tile_id, "pasto")

            nodos_fila.append(Node(x, y, tile_id, nombre))

        grid.append(nodos_fila)

    return grid


def spawn_crops(grid, cantidad=10):

    crops = []

    tipos = ["maiz", "zanahoria", "trigo"]

    for _ in range(cantidad):

        while True:

            x = random.randint(0, len(grid[0]) - 1)
            y = random.randint(0, len(grid) - 1)

            nodo = grid[y][x]

            if nodo.type_name == "cultivo":

                tipo = random.choice(tipos)

                crop = Crop(x, y, tipo)

                # fase aleatoria
                crop.fase = random.randint(0, 3)

                # humedad aleatoria
                crop.humedad = random.uniform(10, 100)

                crops.append(crop)

                break

    return crops


def encontrar_spawn(grid):

    for fila in grid:
        for nodo in fila:

            if nodo.type_name == "casa":
                return nodo.x, nodo.y


def main():

    pygame.init()

    celda_px = 12

    ancho = 80 * celda_px
    alto = 65 * celda_px

    pantalla = pygame.display.set_mode((ancho, alto))

    pygame.display.set_caption("AI Smart Farm")

    mundo = cargar_mapa()

    spawn_x, spawn_y = encontrar_spawn(mundo)

    # agente con generador de cultivos
    agente = Agent(
        spawn_x,
        spawn_y,
        crop_factory=lambda: spawn_crops(mundo, 3)
    )

    crops = spawn_crops(mundo, 3)

    state = GameState(
        farmer_pos=(agente.x, agente.y),
        grid=mundo,
        crops=crops
    )

    colores = {
        "pasto":      (118,186,27),
        "agua":       (74,163,223),
        "acantilado": (142,112,72),
        "edificio":   (180,70,50),
        "cultivo":    (220,190,50),
        "puente":     (150,100,50),
        "puerta":     (200,160,80),
        "casa":       (200,100,100),
    }

    clock = pygame.time.Clock()

    ejecutando = True

    while ejecutando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                ejecutando = False

        # ======================
        # ACTUALIZAR CULTIVOS
        # ======================

        for crop in state.crops:

            crop.crecer(
                tasa_secado=0.1,
                umbral_crecimiento=40
            )

        # ======================
        # UPDATE AGENTE
        # ======================

        state.farmer_pos = (agente.x, agente.y)

        agente.update(state)

        # ======================
        # DIBUJAR
        # ======================

        pantalla.fill((0,0,0))

        # mapa
        for fila in mundo:
            for nodo in fila:

                color = colores.get(nodo.type_name, (255,255,255))

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

        # cultivos
        for crop in state.crops:

            if crop.fase == 0:
                color = (160,120,40)   # tierra

            elif crop.fase == 1:
                color = (120,200,80)   # brote

            elif crop.fase == 2:
                color = (0,200,0)      # creciendo

            elif crop.fase >= 3:
                color = (255,220,0)    # listo para cosechar

            pygame.draw.rect(
                pantalla,
                color,
                (
                    crop.x * celda_px,
                    crop.y * celda_px,
                    celda_px - 1,
                    celda_px - 1
                )
            )

        # path del agente
        if agente.current_path:

            for px, py in agente.current_path:

                pygame.draw.rect(
                    pantalla,
                    (255,0,255),
                    (
                        px * celda_px,
                        py * celda_px,
                        celda_px - 1,
                        celda_px - 1
                    )
                )

        # agente
        pygame.draw.rect(
            pantalla,
            (255,255,255),
            (
                agente.x * celda_px,
                agente.y * celda_px,
                celda_px - 1,
                celda_px - 1
            )
        )

        pygame.display.flip()

        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
