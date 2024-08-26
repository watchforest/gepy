import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 1400, 1200
FPS = 60

# Define colors using pygame.Color
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()

# Setup font for text rendering
font = pygame.font.Font(None, 36)

# Define the Node class
class Node:
    def __init__(self, x, y, message=""):
        self.x = x
        self.y = y
        self.message = message  # Message associated with the node
        self.neighbors = {}  # Dictionary to hold neighboring nodes

    def add_neighbor(self, direction, node):
        self.neighbors[direction] = node

# Define the Network class
class Network:
    def __init__(self):
        self.nodes = []

    def add_node(self, x, y, message=""):
        node = Node(x, y, message)
        self.nodes.append(node)
        return node

    def draw(self, surface):
        for node in self.nodes:
            for neighbor in node.neighbors.values():
                pygame.draw.line(surface, WHITE, (node.x, node.y), (neighbor.x, neighbor.y), 2)
            pygame.draw.circle(surface, WHITE, (node.x, node.y), 10)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, node):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
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

    def draw_message(self, surface):
        if self.message:
            text_surface = font.render(self.message, True, WHITE)
            surface.blit(text_surface, (self.rect.x + 30, self.rect.y - 20))

# Initialize network and player with messages
network = Network()

# Create nodes in different positions
node1 = network.add_node(100, 100, "Hello my friend.")
node2 = network.add_node(300, 100, "Don't go further down, it is scary.")
node3 = network.add_node(500, 100, "You should have listened to me, now there is no way home.")
node4 = network.add_node(300, 300, "Help")
node5 = network.add_node(100, 300, "Help")
node6 = network.add_node(500, 300, "Help")
node7 = network.add_node(300, 500, "Help")
node8 = network.add_node(100, 500, "Help")
node9 = network.add_node(500, 500, "Help")
node10 = network.add_node(700, 300, "Help")

# Connect nodes with neighbors (edges)
node1.add_neighbor('right', node2)
node2.add_neighbor('left', node1)
node2.add_neighbor('right', node3)
node3.add_neighbor('left', node2)
node2.add_neighbor('down', node4)
node4.add_neighbor('up', node2)
node4.add_neighbor('left', node5)
node4.add_neighbor('right', node6)
node4.add_neighbor('down', node7)
node5.add_neighbor('right', node4)
node6.add_neighbor('left', node4)
node7.add_neighbor('up', node4)
node7.add_neighbor('left', node8)
node7.add_neighbor('right', node9)
node8.add_neighbor('right', node7)
node9.add_neighbor('left', node7)
node6.add_neighbor('right', node10)
node10.add_neighbor('left', node6)

# Initialize the player at the starting node
player = Player(node1)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill(BLACK)
    network.draw(screen)
    screen.blit(player.image, player.rect)
    player.draw_message(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
