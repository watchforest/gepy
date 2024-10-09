import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        elif hasattr(entity, 'rect'):
            return entity.rect.move(self.camera.topleft)
        else:
            raise TypeError("Entity must be a Rect or have a 'rect' attribute")

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to game boundaries
        # x = min(0, x)  # left
        # y = min(0, y)  # top
        # x = max(-(self.width), x)  # right
        # y = max(-(self.height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)