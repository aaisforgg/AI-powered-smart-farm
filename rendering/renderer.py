import pygame
import numpy as np

class FarmRender:
    def __init__(self, width=800, height=720):
        self.screen = pygame.display.set_mode((width, height))
        self.cell_size = 10 # Cada celda del grid 80x72 será de 10px
        
        # Colores basados en tu imagen de Stardew
        self.colors = {
            "pasto": (118, 186, 27),
            "agua": (74, 163, 223),
            "cultivo": (255, 204, 0),
            "edificio": (165, 42, 42),
            "acantilado": (100, 100, 100)
        }

    def draw_grid(self, grid):
        for row in grid:
            for node in row:
                rect = (node.x * self.cell_size, node.y * self.cell_size, 
                        self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.colors[node.type_name], rect)
                # Dibujar bordes del grid para visualización
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)