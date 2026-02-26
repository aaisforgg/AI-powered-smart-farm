# main.py
import pygame
import numpy as np # Requisito del proyecto
from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node # pyright: ignore[reportMissingImports]

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
    mapa_img = pygame.image.load("assets/map_overlay.png")
    print("Proyecto IA Granja iniciado") #
    
    # Configuración de pantalla
    celda_px = 12
    ancho = 80 * celda_px
    alto = 72 * celda_px
    mapa_img = pygame.transform.scale(mapa_img, (ancho, alto)) 
    pantalla = pygame.display.set_mode((ancho, alto))
    
    # Colores temáticos de Stardew Valley
    colores = {
        "pasto": (118, 186, 27),
        "agua": (74, 163, 223),
        "acantilado": (142, 112, 72),
        "edificio": (180, 70, 50),
        "cultivo": (220, 190, 50),
        "puente": (150, 100, 50)
    }

    mundo = cargar_mapa()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Renderizado del grid
        pantalla.fill((0, 0, 0))
        for fila in mundo:
            for nodo in fila:
                color = colores.get(nodo.type_name, (255, 255, 255))
                pygame.draw.rect(pantalla, color, 
                                (nodo.x * celda_px, nodo.y * celda_px, 
                                 celda_px - 1, celda_px - 1))

        pantalla.blit(mapa_img, (0, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()