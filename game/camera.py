import pygame

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def update(self, target):
        # Use the player's direct position instead of expecting a rect
        self.x = -target.x + self.width // 2
        self.y = -target.y + self.height // 2

    def apply(self, pos):
        # Convert tuple to Vector2 if needed
        if isinstance(pos, tuple):
            pos = pygame.math.Vector2(pos)
        return pygame.math.Vector2(pos.x + self.x, pos.y + self.y)
