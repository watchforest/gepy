import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 1400, 800
FPS = 60

# Define colors
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BACKGROUND_COLOR = pygame.Color('#DAD6C1')

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()

# Setup font for text rendering
title_font = pygame.font.Font(None, 120)  # Title font
button_font = pygame.font.Font(None, 74)  # Button font

# Load the image for the start screen (Make sure to place the image in the correct directory)
image_path = os.path.join('assets', 'images', 'start_screen_image.png')
start_screen_image = pygame.image.load(image_path).convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (600, 600))  # Adjust size as needed

# Button class to handle the buttons
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN
        self.action = action
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, WHITE, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        text_surface = button_font.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.hovered = True
            return True
        else:
            self.hovered = False
            return False

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
        self.image.fill(GREEN)
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
            text_surface = button_font.render(self.message, True, WHITE)
            surface.blit(text_surface, (self.rect.x + 30, self.rect.y - 20))

# Game state management
def game_loop():
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

def start_screen():
    def start_new_game():
        game_loop()

    start_button = Button("Start", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75, start_new_game)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)  # Set background color to the specified hex color
        title_surface = title_font.render("NETWORKS", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 8))  # Move title up

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if start_button.check_for_input(mouse_position):
                    start_button.action()  # Trigger the start game action

        mouse_position = pygame.mouse.get_pos()
        start_button.check_for_input(mouse_position)

        start_button.draw(screen)

        # Draw the image on the right side of the screen
        screen.blit(start_screen_image, (WIDTH - start_screen_image.get_width() - 50, HEIGHT // 2 - start_screen_image.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

start_screen()
