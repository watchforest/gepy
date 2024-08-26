import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, node, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(node.x, node.y))
        self.node = node
        self.target_node = node
        self.speed = 5
        self.message = node.message
        self.moving = False
        self.direction = pygame.math.Vector2(0, 0)

    def move_to_node(self, target_node):
        self.target_node = target_node
        self.direction = pygame.math.Vector2(target_node.x - self.node.x, target_node.y - self.node.y)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize() * self.speed
        self.moving = True

    def update(self, keys):
        if not self.moving:
            if keys[pygame.K_RIGHT] and 'right' in self.node.neighbors:
                self.move_to_node(self.node.neighbors['right'])
            elif keys[pygame.K_LEFT] and 'left' in self.node.neighbors:
                self.move_to_node(self.node.neighbors['left'])
            elif keys[pygame.K_UP] and 'up' in self.node.neighbors:
                self.move_to_node(self.node.neighbors['up'])
            elif keys[pygame.K_DOWN] and 'down' in self.node.neighbors:
                self.move_to_node(self.node.neighbors['down'])
        else:
            self.rect.x += self.direction.x
            self.rect.y += self.direction.y
            # Check if the player has reached the target node
            if self.direction.length() > 0 and self.direction.dot(pygame.math.Vector2(self.target_node.x - self.rect.x, self.target_node.y - self.rect.y)) <= 0:
                self.rect.center = (self.target_node.x, self.target_node.y)
                self.node = self.target_node
                self.message = self.node.message
                self.moving = False

    def draw_message(self, surface, camera_offset):
        if self.message:
            WHITE = pygame.Color(255, 255, 255)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.message, True, WHITE)
            surface.blit(text_surface, (self.rect.x + 30 + camera_offset.x, self.rect.y - 20 + camera_offset.y))
