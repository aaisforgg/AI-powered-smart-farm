# main.py
import pygame
import numpy as np # Requisito del proyecto
from world.farm_grid import MAP_DATA, TILE_TYPES
from world.node import Node # pyright: ignore[reportMissingImports]

# --- Definición del Agente ---
class SmartAgent:
    def __init__(self, start_node):
        self.current_node = start_node
        self.x = start_node.x
        self.y = start_node.y
        self.path = []
        # Color azul para el agente
        self.color = (0, 0, 255)

    def set_path(self, new_path):
        """Asigna la ruta para el agente"""
        self.path = new_path

    def update(self, mundo):
        """Mueve al agente al siguiente nodo de la ruta"""
        if self.path:
            next_node = self.path.pop(0)
            self.current_node = next_node
            self.x = next_node.x
            self.y = next_node.y

    def draw(self, pantalla, celda_px):
        """Dibuja al agente como un círculo sin modificar el fondo"""
        centro = (self.x * celda_px + celda_px // 2, 
                  self.y * celda_px + celda_px // 2)
        pygame.draw.circle(pantalla, self.color, centro, celda_px // 3)

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
    # Intenta cargar la imagen, si no existe crea una superficie vacía para evitar errores
    try:
        mapa_img = pygame.image.load("assets/map_overlay.png")
    except:
        mapa_img = pygame.Surface((80 * 12, 72 * 12))
        
    print("Proyecto IA Granja iniciado")
    
    # Configuración de pantalla
    celda_px = 12
    ancho = 80 * celda_px
    alto = 72 * celda_px
    mapa_img = pygame.transform.scale(mapa_img, (ancho, alto)) 
    pantalla = pygame.display.set_mode((ancho, alto))
    
    colores = {
        "pasto": (118, 186, 27),
        "agua": (74, 163, 223),
        "acantilado": (142, 112, 72),
        "edificio": (180, 70, 50),
        "cultivo": (220, 190, 50),
        "puente": (150, 100, 50)
    }

    mundo = cargar_mapa()
    clock = pygame.time.Clock()
    
    # Inicializar Agente
    agente = SmartAgent(mundo[10][30])
    
    # Definir una ruta de ejemplo inicial
    camino = [mundo[12][i] for i in range(60, 50, -1)] 
    camino += [mundo[y][50] for y in range(12, 20)]
    camino += [mundo[20][i] for i in range(50, 30, -1)]
    camino += [mundo[y][31] for y in range(20, 40)]

    agente = SmartAgent(camino[0])
    agente.set_path(camino)

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # 1. Dibujar fondo negro
        pantalla.fill((0, 0, 0))
        
        # 2. Renderizado del grid (Lógica visual original)
        for fila in mundo:
            for nodo in fila:
                color = colores.get(nodo.type_name, (255, 255, 255))
                pygame.draw.rect(pantalla, color, 
                                (nodo.x * celda_px, nodo.y * celda_px, 
                                 celda_px - 1, celda_px - 1))

        # Convertir mundo a mapa para State
        def construir_state_desde_grid(mundo):
            state = State()

            for fila in mundo:
                for nodo in fila:
                    if nodo.type_name == "agua":
                        state.mapa[(nodo.x, nodo.y)] = "AGUA"
                    elif nodo.type_name in ["acantilado", "edificio"]:
                        state.mapa[(nodo.x, nodo.y)] = "OBSTACULO"
                    else:
                        state.mapa[(nodo.x, nodo.y)] = "PASTO"

            return state
        # 3. Actualizar y dibujar agente
        agente.update(mundo)
        
        # 4. Superponer imagen (Overlay)
        pantalla.blit(mapa_img, (0, 0))
        
        # 5. Dibujar al agente encima de todo
        agente.draw(pantalla, celda_px)
        
        pygame.display.flip()
        clock.tick(5)  # Velocidad controlada (5 FPS)

    pygame.quit()

if __name__ == "__main__":
    main()