import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to the map size
        x = max(-(self.map_width - self.width), min(0, x))
        y = max(-(self.map_height - self.height), min(0, y))

        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply_offset(self):
        return pygame.math.Vector2(self.camera.topleft)
