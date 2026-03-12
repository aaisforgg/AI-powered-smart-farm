import pygame
import numpy as np
from world.farm_grid import MAP_DATA, TILE_TYPES, FarmGrid
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


def main():
    pygame.init()
    celda_px = 12
    ancho, alto = 80 * celda_px, 72 * celda_px
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("AI Smart Farm - Seasonal World")

    # --- 1. CARGAR DICCIONARIO DE MAPAS ---
    # Cargamos todas las versiones del mapa para no leer el disco en cada frame
    fondos = {}
    rutas_mapas = {
        "Primavera": "assets/map_overlay.png",
        "Verano": "assets/map_verano.jpeg",
        "Otoño": "assets/map_otoño.jpeg",
        "Invierno": "assets/map_invierno.jpeg"
    }

    for estacion, ruta in rutas_mapas.items():
        try:
            img = pygame.image.load(ruta).convert_alpha()
            fondos[estacion] = pygame.transform.scale(img, (ancho, alto))
            print(f"✅ Mapa de {estacion} cargado.")
        except:
            print(f"⚠️ No se encontró {ruta}, se usará el mapa base.")
            # Fallback al mapa base si uno falta
            if "Primavera" in fondos:
                fondos[estacion] = fondos["Primavera"]

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

    mundo = cargar_mapa_logico()
    crops = [Crop(50, 40), Crop(55, 42), Crop(22, 45), Crop(25, 50), Crop(60, 55)]
    state = GameState(farmer_pos=(30, 10), grid=mundo, crops=crops)
    agente = Agent(30, 10)

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Tick del agente — aqui vive A*
        agente.update(state)
        print(f"Agente: ({agente.x}, {agente.y}) | goal: {agente.goal} | path: {len(agente.current_path)}")
        state.farmer_pos = (agente.x, agente.y)
        state.tick += 1

        # Crecer cultivos cada tick
        for crop in state.crops:
            crop.crecer(tasa_secado=1.0, umbral_crecimiento=20.0)

        # Dibujar fondo
        pantalla.fill((0, 0, 0))

        # 1. DIBUJAR FONDO DINÁMICO
        # Selecciona el fondo según la estación actual
        fondo_actual = fondos.get(clima, fondos.get("Primavera"))
        if fondo_actual:
            pantalla.blit(fondo_actual, (0, 0))

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

        # 3. FILTRO ATMOSFÉRICO (Sutil para no tapar los mapas nuevos)
        weather_overlay.fill((0, 0, 0, 0))
        if clima == "Invierno":
            weather_overlay.fill((150, 200, 255, 40)) # Muy suave, el mapa ya es blanco
        elif clima == "Verano":
            weather_overlay.fill((255, 200, 0, 20))
        elif clima == "Otoño":
            weather_overlay.fill((180, 100, 0, 30))
        
        if evento_activo == "Tormenta":
            weather_overlay.fill((10, 10, 40, 120))
        elif evento_activo == "Sequía":
            weather_overlay.fill((255, 50, 0, 30))
        
        pantalla.blit(weather_overlay, (0, 0))

        # 4. PARTÍCULAS
        if clima == "Invierno" or evento_activo == "Tormenta":
            p_color = (255, 255, 255) if clima == "Invierno" else (100, 100, 255)
            for p in particulas:
                p.caer()
                pygame.draw.line(pantalla, p_color, (p.x, p.y), (p.x, p.y + 2), 1)

        # 5. AGENTE
        centro = (agente.x * celda_px + celda_px // 2, agente.y * celda_px + celda_px // 2)
        pygame.draw.circle(pantalla, (255, 255, 255), centro, celda_px // 2) 
        pygame.draw.circle(pantalla, (0, 0, 255), centro, celda_px // 3)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()