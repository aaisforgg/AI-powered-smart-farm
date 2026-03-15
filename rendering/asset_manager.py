import os
import pygame


class AssetManager:
    """Carga y cachea assets gráficos. Se inicializa una vez en main.py."""

    def __init__(self, cell_size=12):
        self.cell_size = cell_size
        self._tiles = {}    # {nombre: Surface}
        self._crops = {}    # {fase: Surface}
        self._agent = None  # Surface
        self._loaded = False

    def load_all(self):
        """Llamar después de pygame.init() y antes del game loop."""
        self._load_tiles()
        self._load_crops()
        self._load_agent()
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
