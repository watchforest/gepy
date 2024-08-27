import pygame
import game.colors as colors

class Player(pygame.sprite.Sprite):
    def __init__(self, node, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(node.x, node.y))
        self.node = node
        self.target_node = node
        self.speed = 30
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
            target_node = None
            
            # Check for diagonal movement
            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                if 'up-right' in self.node.neighbors:
                    target_node = self.node.neighbors['up-right']
                elif 'up' in self.node.neighbors and 'right' in self.node.neighbors:
                    target_node = self.node.neighbors['up']
            elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                if 'up-left' in self.node.neighbors:
                    target_node = self.node.neighbors['up-left']
                elif 'up' in self.node.neighbors and 'left' in self.node.neighbors:
                    target_node = self.node.neighbors['up']
            elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                if 'down-right' in self.node.neighbors:
                    target_node = self.node.neighbors['down-right']
                elif 'down' in self.node.neighbors and 'right' in self.node.neighbors:
                    target_node = self.node.neighbors['down']
            elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                if 'down-left' in self.node.neighbors:
                    target_node = self.node.neighbors['down-left']
                elif 'down' in self.node.neighbors and 'left' in self.node.neighbors:
                    target_node = self.node.neighbors['down']
            # Check for single direction movement
            elif keys[pygame.K_RIGHT] and 'right' in self.node.neighbors:
                target_node = self.node.neighbors['right']
            elif keys[pygame.K_LEFT] and 'left' in self.node.neighbors:
                target_node = self.node.neighbors['left']
            elif keys[pygame.K_UP] and 'up' in self.node.neighbors:
                target_node = self.node.neighbors['up']
            elif keys[pygame.K_DOWN] and 'down' in self.node.neighbors:
                target_node = self.node.neighbors['down']

            # Move to the determined target node, if any
            if target_node:
                self.move_to_node(target_node)
        else:
            # Update the player's position
            self.rect.x += self.direction.x
            self.rect.y += self.direction.y
            if self.direction.length() > 0 and self.direction.dot(pygame.math.Vector2(self.target_node.x - self.rect.x, self.target_node.y - self.rect.y)) <= 0:
                self.rect.center = (self.target_node.x, self.target_node.y)
                self.node = self.target_node
                self.message = self.node.message
                self.moving = False


    def draw_message(self, surface, camera_offset):
        if self.message:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.message, True, colors.WHITE)
            surface.blit(text_surface, (self.rect.x + 30 + camera_offset.x, self.rect.y - 20 + camera_offset.y))
