import pygame


class AgentVisual:

    def __init__(self, image_path, cell_size):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, screen, x, y, cell_size):
        screen.blit(self.image, (x * cell_size, y * cell_size))