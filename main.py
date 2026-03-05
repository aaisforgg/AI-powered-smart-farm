import pygame
import numpy as np
from world.farm_grid import MAP_DATA, TILE_TYPES, FarmGrid
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


def main():
    pygame.init()

    try:
        mapa_img = pygame.image.load("assets/map_overlay.png")
    except:
        mapa_img = pygame.Surface((80 * 12, 72 * 12))

    celda_px = 12
    ancho = 80 * celda_px
    alto = 72 * celda_px
    mapa_img = pygame.transform.scale(mapa_img, (ancho, alto))
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("AI Smart Farm")

    colores = {
        "pasto":      (118, 186,  27),
        "agua":       ( 74, 163, 223),
        "acantilado": (142, 112,  72),
        "edificio":   (180,  70,  50),
        "cultivo":    (220, 190,  50),
        "puente":     (150, 100,  50),
        "puerta":     (200, 160,  80),
    }

    mundo = cargar_mapa()

    crops = [
        Crop(50, 40),
        Crop(55, 42),
        Crop(22, 45),
        Crop(25, 50),
        Crop(60, 55),
    ]

    state = GameState(
        farmer_pos=(30, 10),
        grid=mundo,
        crops=crops,
    )

    agente = Agent(30, 10)

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Tick del agente — aqui vive A*
        agente.update(state)
        state.farmer_pos = (agente.x, agente.y)
        state.tick += 1

        # Crecer cultivos cada tick
        for crop in state.crops:
            crop.crecer(tasa_secado=1.0, umbral_crecimiento=20.0)

        # Dibujar fondo
        pantalla.fill((0, 0, 0))

        # Dibujar grid
        for fila in mundo:
            for nodo in fila:
                color = colores.get(nodo.type_name, (255, 255, 255))
                pygame.draw.rect(pantalla, color,
                                 (nodo.x * celda_px, nodo.y * celda_px,
                                  celda_px - 1, celda_px - 1))

        # Dibujar cultivos encima del grid
        for crop in state.crops:
            cx, cy = crop.pos
            if crop.fase == 0:
                color_crop = (180, 140, 20)   # semilla
            elif crop.fase == 1:
                color_crop = (80, 200, 80)    # creciendo
            else:
                color_crop = (255, 80, 80)    # listo para cosechar
            pygame.draw.rect(pantalla, color_crop,
                             (cx * celda_px + 2, cy * celda_px + 2,
                              celda_px - 4, celda_px - 4))

        # Superponer imagen del mapa
        pantalla.blit(mapa_img, (0, 0))

        # Dibujar agente encima de todo
        centro = (agente.x * celda_px + celda_px // 2,
                  agente.y * celda_px + celda_px // 2)
        pygame.draw.circle(pantalla, (0, 0, 255), centro, celda_px // 3)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()