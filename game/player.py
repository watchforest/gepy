import pygame
import game.styles as colors

class Player(pygame.sprite.Sprite):
    def __init__(self, node, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(node.x, node.y))
        self.node = node
        self.target_node = node
        self.speed = 7
        self.message = node.message
        self.moving = False
        self.direction = pygame.math.Vector2(0, 0)

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

    def move_to_node(self, target_node):
        if target_node not in self.node.neighbors.values():
            print(f"Invalid move: Target node not in neighbors")  # Debug print
            return
        self.target_node = target_node
        self.direction = pygame.math.Vector2(target_node.x - self.node.x, target_node.y - self.node.y)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize() * self.speed
        self.moving = True
        print(f"Moving to node: {target_node.name}")  # Debug print

    def update(self, keys, network):
        if not self.moving:
            target_node = None
            direction = pygame.math.Vector2(0, 0)

            # Print current node's neighbors for debugging
            print(f"Current node: {self.node.name}")
            print(f"Available neighbors: {self.node.neighbors.keys()}")

            # Check for horizontal movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                target_node = self.node.neighbors.get('right')
                if target_node:
                    print("Moving right")  # Debug print
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                target_node = self.node.neighbors.get('left')
                if target_node:
                    print("Moving left")  # Debug print
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                target_node = self.node.neighbors.get('up')
                if target_node:
                    print("Moving up")  # Debug print
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                target_node = self.node.neighbors.get('down')
                if target_node:
                    print("Moving down")  # Debug print

            if target_node:
                self.move_to_node(target_node)
        else:
            # Update position while moving
            new_pos = self.rect.center + self.direction
            self.rect.center = new_pos
            to_target = pygame.math.Vector2(self.target_node.x - self.rect.centerx, 
                                          self.target_node.y - self.rect.centery)
            if self.direction.dot(to_target) <= 0:
                self.rect.center = (self.target_node.x, self.target_node.y)
                self.node = self.target_node
                self.message = self.node.message
                self.moving = False
                print(f"Reached node: {self.node.name}")  # Debug print

    def draw(self, surface, camera):
        draw_pos = camera.apply(pygame.math.Vector2(self.rect.topleft))
        surface.blit(self.image, draw_pos)
        if self.message:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.message, True, colors.WHITE)
            text_pos = camera.apply(pygame.math.Vector2(self.rect.x + 30, self.rect.y - 20))
            surface.blit(text_surface, text_pos)
