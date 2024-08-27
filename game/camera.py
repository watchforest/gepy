import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Offset the entity position by the camera's top-left corner
        return entity.move(self.camera.topleft)

    def update(self, target):
        # Center the camera on the target (player)
        self.camera.x = -target.rect.centerx + int(self.width / 2)
        self.camera.y = -target.rect.centery + int(self.height / 2)
