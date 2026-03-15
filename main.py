import pygame
import random
from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from agent.agent import Agent
from entities.crop import Crop


def cargar_mapa_logico():
    grid = []
    for y, fila in enumerate(MAP_DATA):
        nodos_fila = []
        for x, tile_id in enumerate(fila):
            nombre = TILE_TYPES.get(tile_id, "pasto")
            nodos_fila.append(Node(x, y, tile_id, nombre))
        grid.append(nodos_fila)
    return grid


# ======================================
# SPAWN RANDOM DEL AGENTE
# ======================================

def posicion_random_valida(grid):

    tiles_prohibidos = {
        "agua",
        "acantilado",
        "cultivo",
        "puerta"
    }

    alto = len(grid)
    ancho = len(grid[0])

    while True:

        x = random.randint(0, ancho - 1)
        y = random.randint(0, alto - 1)

        tile = grid[y][x]

        if tile.type_name not in tiles_prohibidos and tile.walkable:
            return x, y


def _spawn_crops():
    """Crea la lista inicial de cultivos. Se llama al inicio y en cada nueva vida."""
    from entities.crop import Crop
    return [
        Crop(50, 40),
        Crop(55, 42),
        Crop(22, 45),
        Crop(25, 50),
        Crop(62, 58),
    ]


def main():

    pygame.init()

    celda_px = 12
    ancho = 80 * celda_px
    alto = 72 * celda_px

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

    agente = Agent(spawn_x, spawn_y, crop_factory=_spawn_crops)

    # ==========================
    # CULTIVOS
    # ==========================

    crops = _spawn_crops()

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
        "pasto": (118, 186, 27),
        "agua": (74, 163, 223),
        "acantilado": (142, 112, 72),
        "edificio": (180, 70, 50),
        "cultivo": (220, 190, 50),
        "puente": (150, 100, 50),
        "puerta": (200, 160, 80),
        "casa": (200, 200, 255)
    }

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # ==========================
        # UPDATE AGENTE
        # ==========================

        # ==========================
        # DEBUG ENERGÍA
        # ==========================

        energia_antes = agente.energy

        agente.update(state)

        energia_despues = agente.energy
        consumo = energia_despues - energia_antes

        print("----------- AGENTE -----------")
        print(f"Tick: {state.tick}")
        print(f"Posición: ({agente.x}, {agente.y})")

        print(f"Energía: {energia_antes:.2f} -> {energia_despues:.2f}")

        if consumo < 0:
            print(f"Consumo energía: {consumo:.2f}")
        else:
            print(f"Recuperación energía: +{consumo:.2f}")

        print(f"Resting: {agente.resting}")

        # ==========================
        # GENÉTICA
        # ==========================

        if hasattr(agente, "genes"):
            g = agente.genes

            print(
            f"Genes -> "
            f"energy_max:{g.energy_max:.2f} "
            f"energy_consumption:{g.energy_consumption:.2f} "
            f"rest_efficiency:{g.rest_efficiency:.2f} "
            f"exploration_rate:{g.exploration_rate:.2f}"
            )

        print("--------------------------------")

        print(
            f"Agente: ({agente.x}, {agente.y}) | "
            f"goal: {agente.goal} | "
            f"path: {len(agente.current_path)}"
        )

        state.farmer_pos = (agente.x, agente.y)
        state.tick += 1

        # ==========================
        # CRECIMIENTO DE CULTIVOS
        # ==========================

        for crop in state.crops:
            crop.crecer(
               tasa_secado=1.0,
                ticks_por_fase=20
            )

        # ==========================
        # DIBUJAR
        # ==========================

        pantalla.fill((0, 0, 0))

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
        # CULTIVOS
        # ==========================

        for crop in state.crops:

            cx, cy = crop.pos

            if crop.fase == 0:
                color_crop = (180, 140, 20)
            elif crop.fase == 1:
                color_crop = (80, 200, 80)
            else:
                color_crop = (255, 80, 80)

            pygame.draw.rect(
                pantalla,
                color_crop,
                (
                    cx * celda_px + 2,
                    cy * celda_px + 2,
                    celda_px - 4,
                    celda_px - 4
                )
            )

        # ==========================
        # AGENTE
        # ==========================

        centro = (
            agente.x * celda_px + celda_px // 2,
            agente.y * celda_px + celda_px // 2
        )

        pygame.draw.circle(
            pantalla,
            (255, 255, 255),
            centro,
            celda_px // 2
        )

        pygame.draw.circle(
            pantalla,
            (0, 0, 255),
            centro,
            celda_px // 3
        )

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()