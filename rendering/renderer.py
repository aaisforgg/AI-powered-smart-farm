import pygame

class FarmRender:
    def __init__(self, width=800, height=720):
        self.screen = pygame.display.set_mode((width, height))
        self.cell_size = 10 
        
        # Colores base (Primavera por defecto)
        self.base_colors = {
            "pasto": (118, 186, 27),
            "agua": (74, 163, 223),
            "cultivo": (255, 204, 0),
            "edificio": (165, 42, 42),
            "acantilado": (100, 100, 100)
        }
        
        # Configuración de Filtros por Estación (RGBA)
        self.season_filters = {
            "Primavera": None, # Color natural
            "Verano": (255, 255, 0, 30),  # Filtro cálido amarillento
            "Otoño": (200, 100, 0, 50),   # Filtro naranja/rojizo
            "Invierno": (200, 230, 255, 80) # Filtro azulado/blanco frío
        }

    def get_season_color(self, type_name, season):
        """Ajusta el color del pasto según la estación"""
        color = list(self.base_colors[type_name])
        
        if type_name == "pasto":
            if season == "Otoño":
                return (170, 130, 50) # Pasto seco/café
            if season == "Invierno":
                return (240, 248, 255) # Pasto con nieve (Alice Blue)
            if season == "Verano":
                return (50, 150, 20)  # Verde más oscuro/intenso
        return tuple(color)

    def draw_grid(self, grid, season="Primavera"):
        # 1. Dibujar el fondo y las celdas
        for row in grid:
            for node in row:
                rect = (node.x * self.cell_size, node.y * self.cell_size, 
                        self.cell_size, self.cell_size)
                
                # Obtener color según estación
                color = self.get_season_color(node.type_name, season)
                
                pygame.draw.rect(self.screen, color, rect)
                # Opcional: solo dibujar bordes si es necesario para no saturar
                # pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # 2. Aplicar Filtro Atmosférico (Overlay)
        filter_color = self.season_filters.get(season)
        if filter_color:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill(filter_color)
            self.screen.blit(overlay, (0, 0))