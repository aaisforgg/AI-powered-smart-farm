import os
import pygame


DIR_MAP = {
    (0, -1): "back",
    (0,  1): "front",
    (-1, 0): "left",
    (1,  0): "right",
    (0,  0): "front",
}

FULL_ACTIONS  = ["stationary", "walking", "running", "collecting", "watering"]
FRONT_ONLY    = ["planting"]


class SpriteManager:
    """Carga y gestiona sprites del agente por acción y dirección."""

    def __init__(self, cell_size=12, scale_factor=2):
        self.cell_size   = cell_size
        self.sprite_size = cell_size * scale_factor
        self._sprites    = {}   # {(action, direction): Surface}
        self._loaded     = False

    def load_all(self):
        base = "assets/agent"

        for action in FULL_ACTIONS:
            for direction in ("back", "front", "left", "right"):
                self._load_sprite(base, action, direction, f"{action}-{direction}.png")

        for action in FRONT_ONLY:
            self._load_sprite(base, action, "front", f"{action}-front.png")
            if (action, "front") in self._sprites:
                for d in ("back", "left", "right"):
                    self._sprites[(action, d)] = self._sprites[(action, "front")]

        self._loaded = True
        print(f"[Sprites] Cargados {len(self._sprites)} sprites del agente")

    def _load_sprite(self, base, action, direction, filename):
        for name in [filename, filename.replace(".", " .")]:
            path = os.path.join(base, name)
            try:
                img = pygame.image.load(path).convert_alpha()
                self._sprites[(action, direction)] = pygame.transform.scale(
                    img, (self.sprite_size, self.sprite_size)
                )
                return
            except (FileNotFoundError, pygame.error):
                continue

    def get_sprite(self, action, direction_tuple):
        direction = DIR_MAP.get(direction_tuple, "front")
        return self._sprites.get((action, direction))

    def get_agent_sprite(self, agent):
        """Retorna (Surface, offset_x, offset_y) o (None, 0, 0) para fallback."""
        action = self._determine_action(agent)
        sprite = self.get_sprite(action, agent.dir)
        if sprite is None:
            return None, 0, 0
        offset = (self.sprite_size - self.cell_size) // 2
        return sprite, offset, offset

    def _determine_action(self, agent):
        """Lee el estado visual del agente (escrito por agent.py cada tick)."""
        return getattr(agent, "visual_action", "stationary")
