import pygame
from game.start_screen import start_screen

from pygame import Color, font
from pygame.font import Font
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
font_path = os.path.join(base_dir, 'assets', 'font', 'Pastor of Muppets.TTF')

def gamefont(size):
    font = Font(font_path, size)
    return font

WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
MAGENTA = Color(255, 0, 255)
CYAN = Color(0, 255, 255)
PINK = Color(255, 0, 255)
ORANGE = Color(255, 165, 0)
PURPLE = Color(230, 0, 220)

NODE_COLOR = {
    0: WHITE,
    1: CYAN,
    2: GREEN,
    3: BLUE,
    4: YELLOW,
    5: MAGENTA,
    6: PINK,
    7: ORANGE,
    8: PURPLE,
}

import pygame
import game.styles as colors

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def draw(self, screen, color):
        pygame.draw.line(screen, color, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 10)


# Initialize Pygame
pygame.init()

# Define constants
# Setup the display in fullscreen mode without window borders
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()
FPS = 60

# Setup font for text rendering
font = pygame.font.Font(None, 36)

# Start screen function
start_screen()

from .node import Node
from .edge import Edge
import pygame
from pygame import gfxdraw
from game.styles import NODE_COLOR

class Network:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, x, y, name, message, size, cluster):
        node = Node(x, y, name, message, size, cluster)
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self.edges.append(edge)

    def draw(self, screen, color, camera):
        for edge in self.edges:
            start_pos = camera.apply(pygame.Rect(edge.node1.x, edge.node1.y, 0, 0)).topleft
            end_pos = camera.apply(pygame.Rect(edge.node2.x, edge.node2.y, 0, 0)).topleft
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

        for node in self.nodes:
            node_center = camera.apply(pygame.Rect(node.x, node.y, 0, 0)).center
            pygame.draw.circle(screen, NODE_COLOR[node.cluster], node_center, node.size)

import pygame
import game.styles as colors
from game.styles import gamefont
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = colors.WHITE  # Button color is initially WHITE
        self.text_color = colors.BLACK  # Text color is initially BLACK
        self.hovered = False
        self.action = action
        self.font = gamefont(74)

    def draw(self, surface):
        # Change button color on hover
        pygame.draw.rect(surface, colors.BLACK if self.hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color if not self.hovered else colors.WHITE)
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height - text_surface.get_height()) // 2+20))

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.action:
                self.action()
        else:
            self.hovered = False

import pygame

class BeginFigure:
    def __init__(self, image_path, position, screen):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (600, 600))  # Adjust size as needed
        self.position = position
        self.screen = screen
        self.alpha = 0  # Start with fully transparent
        self.text = "Welcome to GE.PY!!! Press a key to begin"
        self.displayed_text = ""
        self.text_index = 0
        self.typing_speed = 1  # Control the speed of the text appearing
        self.typing_counter = 0
        self.font = pygame.font.Font(None, 36)
        self.bubble_width = 300
        self.bubble_height = 150
        self.button_font = pygame.font.Font(None, 48)
        self.button_color = (255, 0, 0)
        self.button_hover_color = (200, 0, 0)
        self.button_text_color = (255, 255, 255)
        self.button_rect = pygame.Rect(position[0] + 50, position[1] + 250, 200, 50)
        self.show_button = False

    def fade_in(self, speed=14):
        """Gradually increase the alpha value to fade in the image."""
        if self.alpha < 255:
            self.alpha += speed
            self.image.set_alpha(self.alpha)

    def update_text(self):
        """Update the text display to simulate typing."""
        if self.text_index < len(self.text):
            self.typing_counter += 1
            if self.typing_counter % self.typing_speed == 0:
                self.displayed_text += self.text[self.text_index]
                self.text_index += 1
        else:
            self.show_button = True  # Show the button when typing is complete

    def draw_speech_bubble(self):
        """Draw a speech bubble connected to the image."""
        bubble_x = self.position[0] + self.image.get_width() // 2 - self.bubble_width // 2
        bubble_y = self.position[1] - self.bubble_height - 10
        pygame.draw.rect(self.screen, (255, 255, 255), (bubble_x, bubble_y, self.bubble_width, self.bubble_height), 0)
        pygame.draw.rect(self.screen, (0, 0, 0), (bubble_x, bubble_y, self.bubble_width, self.bubble_height), 2)

        # Draw the text inside the bubble with word wrapping
        lines = []
        words = self.displayed_text.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            text_width, text_height = self.font.size(test_line)
            if text_width < self.bubble_width - 20:  # Adjust for padding inside the bubble
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  # Add the last line

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (bubble_x + 10, bubble_y + 10 + i * text_height))

    def draw(self):
        """Draw the image and speech bubble on the screen."""
        self.fade_in()  # Apply the fade-in effect
        self.screen.blit(self.image, self.position)

        if self.alpha >= 255:
            self.update_text()  # Start typing text after image is fully displayed
            self.draw_speech_bubble()  # Draw the speech bubble and the text

import pygame
import sys
import os
import game.styles as colors
from game.create_network import create_network
from game.player import Player
from game.styles import gamefont, base_dir
from game.button import Button
from game.camera import Camera
from game.begin_figure import BeginFigure

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption("Syndesi")
clock = pygame.time.Clock()
FPS = 60

title_font = gamefont(200)
button_font = gamefont(74)

# Load the image for the start screen
image_path = os.path.join(base_dir, 'assets', 'images', 'start_screen_image.png')
start_screen_image = pygame.image.load(image_path).convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (600, 600))

def exit_game():
    pygame.quit()
    sys.exit()

# Game loop definition
def game_loop():
    # Load the network and initialize the player
    network = create_network('assets/network/random_graph_100_nodes.gexf')
    player = Player(network.nodes[0], pygame.Color(255, 0, 0))

    # Initialize the camera to match the screen size
    camera = Camera(WIDTH, HEIGHT)

    # Initialize the BeginFigure instance
    begin_figure = BeginFigure('assets/images/start_screen_image.png', (WIDTH - 850, HEIGHT // 2 - 200), screen)

    # Create the "Back to Main Menu" button
    back_button = Button("main menu", WIDTH - 310, 20, 290, 50, start_screen)

    running = True
    figure_displayed = False  # Track whether the figure has been displayed
    waiting_for_keypress = False  # Wait for a keypress after text is fully shown

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # If text has been fully displayed, then respond to any keypress
                if waiting_for_keypress:
                    figure_displayed = True
                    waiting_for_keypress = False  # Reset for potential future use

        # Update the player based on user input only after the figure is done
        if figure_displayed:
            keys = pygame.key.get_pressed()
            player.update(keys)
            camera.update(player)

        # Clear the screen and redraw everything with the camera offset
        screen.fill(colors.BLACK)
        network.draw(screen, colors.WHITE, camera)  # Ensure network.draw handles the camera

        if not figure_displayed:
            # Display the figure until it's fully shown
            begin_figure.draw()
            if begin_figure.show_button:
                waiting_for_keypress = True  # Now waiting for the user to press a key

        # Draw the player with camera offset
        screen.blit(player.image, camera.apply(player.rect))

        # Draw the "Back to Main Menu" button
        mouse_position = pygame.mouse.get_pos()
        back_button.check_for_input(mouse_position)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# Campaign menu
def campaign_menu():
    stage_buttons = [Button(f"Stage {i+1}", WIDTH // 4, HEIGHT // 5 + i * 40, 300, 50, lambda i=i: start_stage(i)) for i in range(3)]

    running = True
    while running:
        screen.fill(colors.BLACK)
        title_surface = title_font.render("Campaign", True, colors.WHITE)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in stage_buttons:
                    button.check_for_input(mouse_position)

        mouse_position = pygame.mouse.get_pos()
        for button in stage_buttons:
            button.check_for_input(mouse_position)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def start_stage(stage_number):
    print(f"Starting stage {stage_number + 1}...")

def upload_files():
    print("Uploading files...")

def run_files():
    print("Running files...")

# Start screen
def start_screen():
    start_button = Button("start", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75, game_loop)
    #levels_button = Button("Levels", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75, campaign_menu)
   # upload_button = Button("Upload Files", WIDTH // 4 - 150, HEIGHT // 2 + 300, 300, 75, upload_files)
    #run_button = Button("Run Files", WIDTH // 4 - 150, HEIGHT // 2 + 400, 300, 75, run_files)
    exit_button = Button("exit Game", WIDTH - 250, 50, 200, 75, lambda: (pygame.quit(), sys.exit()))

    buttons =  [start_button, exit_button] #start_button, upload_button, run_button.

    running = True
    while running:
        screen.fill(colors.BLACK)
        title_surface = title_font.render("SYNDESI", True, colors.WHITE)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_for_input(mouse_position)

        mouse_position = pygame.mouse.get_pos()
        for button in buttons:
            button.check_for_input(mouse_position)
            button.draw(screen)

        screen.blit(start_screen_image, (WIDTH - start_screen_image.get_width() - 50, HEIGHT // 2 - start_screen_image.get_height() // 4))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_screen()

import pygame
from game.styles import NODE_COLOR

class Node:
    def __init__(self, x, y, name, message, size, cluster):
        self.x = x
        self.y = y
        self.name = name
        self.message = message
        self.size = int(size)
        self.cluster = cluster
        self.neighbors = {}


    def draw(self, surface, color):
        pygame.draw.circle(surface, NODE_COLOR[self.cluster], (self.x, self.y), self.size+10)  # Draw the node
        font = pygame.font.Font(None, 24)
        name_surface = font.render(self.name, True, pygame.Color('white'))
        surface.blit(name_surface, (self.x + 12, self.y - 12))  # Draw the node's name

    def add_neighbor(self, direction, node):
        self.neighbors[direction] = node

import pandas as pd
import networkx as nx
from game.network import Network

def load_gexf_to_network(gexf_file_path, network, scale=10000):
    # Load the GEXF file
    graph = nx.read_gexf(gexf_file_path)
    pos = nx.spring_layout(graph)
    weighted_degrees = dict(graph.degree(weight='weight'))
    communities_generator = nx.community.greedy_modularity_communities(graph)
    # Create an inverted dictionary directly
    cluster_dict = {
        node: i
        for i, community in enumerate(communities_generator)
        for node in community
    }
    # Create a dictionary to map node IDs to Node objects
    node_dict = {}

    # Add nodes to the network
    for g_node, (x, y) in pos.items():
        x = x * scale  # Scale up the x position
        y = y * scale  # Scale up the y position
        name = g_node  # Use label if available, otherwise the node ID
        message = ' '
        # Extract the node weight, defaulting to 1 if not present
        node_weight = weighted_degrees[g_node]*5
        node_cluster = cluster_dict[g_node]
        #print(f"Adding node with x={x}, y={y}, name={name}, weight={node_weight}")
        # Add the node to the network
        node = network.add_node(x, y, name, message, node_weight, node_cluster)
        node_dict[g_node] = node

    # Add edges to the network and set neighbors
    for source, target in graph.edges():
        node1 = node_dict[source]
        node2 = node_dict[target]
        network.add_edge(node1, node2)

        # Only add the closest node in each direction
        def add_neighbor_if_closer(node1, node2, direction1, direction2):
            if direction1 not in node1.neighbors or (
                (node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2
            ) < (
                (node1.neighbors[direction1].x - node1.x) ** 2 + (node1.neighbors[direction1].y - node1.y) ** 2
            ):
                node1.add_neighbor(direction1, node2)
                node2.add_neighbor(direction2, node1)

        for source, target in graph.edges():
            node1 = node_dict[source]
            node2 = node_dict[target]
            network.add_edge(node1, node2)

            if node1 != node2:
                dx = node2.x - node1.x
                dy = node2.y - node1.y

                # Primary Directions
                if dx > 0 and abs(dy) <= abs(dx):  # Mostly right
                    add_neighbor_if_closer(node1, node2, 'right', 'left')
                elif dx < 0 and abs(dy) <= abs(dx):  # Mostly left
                    add_neighbor_if_closer(node1, node2, 'left', 'right')
                if dy > 0 and abs(dx) <= abs(dy):  # Mostly down
                    add_neighbor_if_closer(node1, node2, 'down', 'up')
                elif dy < 0 and abs(dx) <= abs(dy):  # Mostly up
                    add_neighbor_if_closer(node1, node2, 'up', 'down')

                # Diagonal Directions
                if dx > 0 and dy < 0:  # Up-right
                    add_neighbor_if_closer(node1, node2, 'up-right', 'down-left')
                elif dx > 0 and dy > 0:  # Down-right
                    add_neighbor_if_closer(node1, node2, 'down-right', 'up-left')
                elif dx < 0 and dy < 0:  # Up-left
                    add_neighbor_if_closer(node1, node2, 'up-left', 'down-right')
                elif dx < 0 and dy > 0:  # Down-left
                    add_neighbor_if_closer(node1, node2, 'down-left', 'up-right')

def create_network(gexf_file_path):
    # Initialize the network
    network = Network()

    # Load data into the network from the GEXF file
    G = gexf_file_path
    load_gexf_to_network(G, network)

    return network

