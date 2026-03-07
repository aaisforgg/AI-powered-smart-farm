import pygame
import numpy as np
import random
import os
from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node
from core.state import GameState
from agent.agent import Agent
from entities.crop import Crop
from simulation.season_manager import SeasonManager
from simulation.event_manager import EventManager

# --- CLASE DE PARTÍCULAS ---
class Particle:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.ancho)
        self.y = random.randint(-self.alto, 0)
        self.velocidad = random.randint(2, 6)

    def caer(self):
        self.y += self.velocidad
        if self.y > self.alto:
            self.reset()

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
    ancho, alto = 80 * celda_px, 72 * celda_px
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("AI Smart Farm - Visual Pro")

    # 1. CARGAR IMAGEN DE FONDO
    try:
        fondo_img = pygame.image.load("assets/map_overlay.png").convert_alpha()
        fondo_img = pygame.transform.scale(fondo_img, (ancho, alto))
        print("✅ Imagen de fondo cargada correctamente.")
    except:
        print("⚠️ No se encontró assets/map_overlay.png. Se usará fondo de colores.")
        fondo_img = None

    # Inicializaciones
    fuente = pygame.font.SysFont("Arial", 20, bold=True)
    season_manager = SeasonManager()
    event_manager = EventManager()
    weather_overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    particulas = [Particle(ancho, alto) for _ in range(120)]

    mundo = cargar_mapa()
    crops = [Crop(50, 40), Crop(55, 42), Crop(22, 45), Crop(25, 50), Crop(60, 55)]
    state = GameState(farmer_pos=(30, 10), grid=mundo, crops=crops)
    agente = Agent(30, 10)

    colores_fallback = {
        "pasto": (118, 186, 27), "agua": (74, 163, 223),
        "acantilado": (142, 112, 72), "edificio": (180, 70, 50),
        "cultivo": (220, 190, 50), "puente": (150, 100, 50),
    }

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: ejecutando = False

        # --- LÓGICA ---
        season_manager.update()
        clima = season_manager.get_season()
        event_manager.update(state, clima)
        evento_activo = event_manager.current_event

        agente.update(state)
        state.farmer_pos = (agente.x, agente.y)
        
        # --- DIBUJAR ---
        pantalla.fill((0, 0, 0))

        # 1. DIBUJAR FONDO
        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            # Si no hay imagen, dibujamos los rectángulos como antes
            for fila in mundo:
                for nodo in fila:
                    color = colores_fallback.get(nodo.type_name, (50, 50, 50))
                    pygame.draw.rect(pantalla, color, (nodo.x*celda_px, nodo.y*celda_px, celda_px, celda_px))

        # 2. DIBUJAR CULTIVOS
        for crop in state.crops:
            cx, cy = crop.pos
            c = (180, 140, 20) if crop.fase == 0 else (80, 200, 80) if crop.fase == 1 else (255, 80, 80)
            pygame.draw.rect(pantalla, c, (cx*celda_px+2, cy*celda_px+2, celda_px-4, celda_px-4))

        # 3. FILTRO ATMOSFÉRICO (Transparencia ajustada para ver el fondo)
        weather_overlay.fill((0, 0, 0, 0))
        if clima == "Invierno":
            weather_overlay.fill((150, 200, 255, 60))
        elif clima == "Verano":
            weather_overlay.fill((255, 200, 0, 25))
        elif clima == "Otoño":
            weather_overlay.fill((180, 100, 0, 40))
        
        if evento_activo == "Tormenta":
            weather_overlay.fill((10, 10, 40, 140))
        elif evento_activo == "Sequía":
            weather_overlay.fill((255, 50, 0, 35))
        
        pantalla.blit(weather_overlay, (0, 0))

        # 4. PARTÍCULAS
        if clima == "Invierno" or evento_activo == "Tormenta":
            p_color = (240, 240, 255) if clima == "Invierno" else (80, 80, 255)
            for p in particulas:
                p.caer()
                pygame.draw.line(pantalla, p_color, (p.x, p.y), (p.x, p.y + 3), 1)

        # 5. AGENTE (Con borde para que resalte sobre la imagen)
        centro = (agente.x * celda_px + celda_px // 2, agente.y * celda_px + celda_px // 2)
        pygame.draw.circle(pantalla, (255, 255, 255), centro, celda_px // 2) 
        pygame.draw.circle(pantalla, (0, 0, 255), centro, celda_px // 3)

        # 6. INTERFAZ (HUD)
        pygame.draw.rect(pantalla, (20, 20, 20), (10, 10, 240, 65))
        pygame.draw.rect(pantalla, (255, 255, 255), (10, 10, 240, 65), 1)
        
        txt_est = fuente.render(f"CLIMA: {clima}", True, (255, 255, 255))
        evt_nombre = evento_activo if evento_activo else "Despejado"
        txt_evt = fuente.render(f"ESTADO: {evt_nombre}", True, (0, 255, 255) if evento_activo else (180, 180, 180))
        
        pantalla.blit(txt_est, (20, 15))
        pantalla.blit(txt_evt, (20, 38))

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()

if __name__ == "__main__":
    main()