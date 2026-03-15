import os
import pygame


class AssetManager:
    """Carga y cachea assets gráficos. Se inicializa una vez en main.py."""

    def __init__(self, cell_size=12, grid_w=960, grid_h=780):
        self.cell_size = cell_size
        self.grid_w = grid_w
        self.grid_h = grid_h
        self._tiles = {}       # {nombre: Surface}
        self._crops = {}       # {fase: Surface}
        self._agent = None     # Surface
        self._maps = {}        # {estacion: Surface} — mapa de fondo por estación
        self._map_overlay = None  # Surface — overlay encima del mapa
        self._loaded = False

    def load_all(self):
        """Llamar después de pygame.init() y antes del game loop."""
        self._load_tiles()
        self._load_crops()
        self._load_agent()
        self._load_maps()
        self._loaded = True

    def get_tile(self, type_name):
        """Retorna Surface del tile, o None si no hay imagen (usa fallback de color)."""
        return self._tiles.get(type_name)

    def get_crop(self, fase):
        """Retorna Surface del crop, o None si no hay imagen."""
        return self._crops.get(fase)

    def get_agent(self):
        """Retorna Surface del agente, o None si no hay imagen."""
        return self._agent

    def get_map(self, season):
        """Retorna Surface del mapa estacional, o None (Primavera usa fallback de colores)."""
        return self._maps.get(season)

    def get_map_overlay(self):
        """Retorna Surface del overlay del mapa, o None."""
        return self._map_overlay

    def _load_tiles(self):
        tile_dir = "assets/tiles"
        tile_files = {
            "pasto":      "grass.png",
            "agua":       "water.png",
            "acantilado": "cliff.png",
            "edificio":   "building.png",
            "cultivo":    "farmland.png",
            "puente":     "bridge.png",
            "puerta":     "door.png",
            "casa":       "house.png",
        }
        for name, filename in tile_files.items():
            path = os.path.join(tile_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self._tiles[name] = pygame.transform.scale(
                    img, (self.cell_size, self.cell_size)
                )
            except (FileNotFoundError, pygame.error):
                pass  # Sin imagen = fallback a color sólido

    def _load_crops(self):
        crop_dir = "assets/crops"
        crop_files = {0: "seed.png", 1: "growing.png", 2: "ready.png"}
        for fase, filename in crop_files.items():
            path = os.path.join(crop_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self._crops[fase] = pygame.transform.scale(
                    img, (self.cell_size - 4, self.cell_size - 4)
                )
            except (FileNotFoundError, pygame.error):
                pass

    def _load_agent(self):
        path = os.path.join("assets", "agent", "farmer.png")
        try:
            img = pygame.image.load(path).convert_alpha()
            self._agent = pygame.transform.scale(
                img, (self.cell_size, self.cell_size)
            )
        except (FileNotFoundError, pygame.error):
            pass

    def _load_maps(self):
        map_files = {
            "Verano":   "assets/map_verano.jpeg",
            "Otoño":    "assets/map_otoño.jpeg",
            "Invierno": "assets/map_invierno.jpeg",
            # Primavera no tiene imagen — fallback a colores sólidos
        }
        target = (self.grid_w, self.grid_h)
        for season, path in map_files.items():
            try:
                img = pygame.image.load(path)
                try:
                    img = img.convert()
                except pygame.error:
                    pass  # sin display activo, usa Surface sin convertir
                self._maps[season] = pygame.transform.scale(img, target)
            except (FileNotFoundError, pygame.error):
                pass

        try:
            img = pygame.image.load("assets/map_overlay.png")
            try:
                img = img.convert_alpha()
            except pygame.error:
                pass
            self._map_overlay = pygame.transform.scale(img, target)
        except (FileNotFoundError, pygame.error):
            pass
