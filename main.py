import pygame
from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node


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

    celda_px = 12
    ancho = 80 * celda_px
    alto = 65 * celda_px

    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("AI Smart Farm")

    # ==========================
    # CARGAR MAPA
    # ==========================

    mundo = cargar_mapa_logico()

    # ==========================
    # SPAWN RANDOM DEL AGENTE
    # ==========================

    spawn_x, spawn_y = posicion_random_valida(mundo)

    print(f"Spawn del agente: ({spawn_x}, {spawn_y})")

    agente = Agent(spawn_x, spawn_y)

    # ==========================
    # CULTIVOS
    # ==========================

    crops = [
        Crop(50, 40),
        Crop(55, 42),
        Crop(22, 45),
        Crop(25, 50),
        Crop(62, 58),
    ]

    # ==========================
    # GAME STATE
    # ==========================

    state = GameState(
        farmer_pos=(agente.x, agente.y),
        grid=mundo,
        crops=crops
    )

    # ==========================
    # COLORES
    # ==========================

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

    mundo = cargar_mapa()

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        pantalla.fill((0, 0, 0))

        # Dibujar mapa
        for fila in mundo:
            for nodo in fila:
                color = colores.get(nodo.type_name, (255, 255, 255))
                pygame.draw.rect(
                    pantalla,
                    color,
                    (nodo.x * celda_px, nodo.y * celda_px,
                     celda_px - 1, celda_px - 1)
                )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()