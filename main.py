import pygame
import numpy as np
from collections import deque
from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from pathfinding.astar import AStarPathfinder
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
    alto = 65 * celda_px
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

    # Construir grid de Nodes
    mundo = cargar_mapa()

    # Construir GameState
    crops = [
        Crop(50, 40),
        Crop(55, 42),
        Crop(22, 45),
    ]

    state = GameState(
        farmer_pos=(30, 10),
        grid=mundo,
        crops=crops,
    )

    # Pathfinder
    pathfinder = AStarPathfinder()

    # Posición inicial del agente
    agent_x, agent_y = state.farmer_pos
    current_path = deque()


    # Calcular ruta al primer cultivo
    if crops:
        gx, gy = crops[0].pos
        path = pathfinder.find_path(agent_x, agent_y, gx, gy, mundo)
        if path:
            current_path = deque(path[1:])
            print(f"Ruta encontrada: {len(current_path)} pasos hacia {crops[0].pos}")
        else:
            print("Sin ruta al cultivo")

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Mover agente un paso por tick
        if current_path:
            agent_x, agent_y = current_path.popleft()
            state.farmer_pos = (agent_x, agent_y)

        # Dibujar mapa de fondo
        pantalla.blit(mapa_img, (0, 0))

        # Dibujar grid
        for fila in mundo:
            for nodo in fila:
                color = colores.get(nodo.type_name, (255, 255, 255))
                pygame.draw.rect(pantalla, color,
                                 (nodo.x * celda_px, nodo.y * celda_px,
                                  celda_px - 1, celda_px - 1))

        # Dibujar cultivos
        for crop in state.crops:
            cx, cy = crop.pos
            pygame.draw.rect(pantalla, (0, 200, 0),
                             (cx * celda_px, cy * celda_px, celda_px - 1, celda_px - 1))

        # Superponer imagen
        #pantalla.blit(mapa_img, (0, 0))

        # Dibujar agente encima de todo
        centro = (agent_x * celda_px + celda_px // 2,
                  agent_y * celda_px + celda_px // 2)
        pygame.draw.circle(pantalla, (0, 0, 255), centro, celda_px // 3)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()