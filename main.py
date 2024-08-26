import pygame
import sys
from game.network import Network
from game.player import Player
from create_network import load_gexf_to_network
import networkx as nx

# Initialize Pygame
pygame.init()


# Define colors using pygame.Color
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BACKGROUND_COLOR = pygame.Color('#DAD6C1')

# Define constants
# Setup the display in fullscreen mode without window borders
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
WIDTH, HEIGHT = screen.get_size()  # Get the actual screen size in fullscreen mode
pygame.display.set_caption("Network Node Game")
clock = pygame.time.Clock()
FPS = 60

# Setup font for text rendering
font = pygame.font.Font(None, 36)

# # Initialize network and player with messages
# network = Network()
#
# # Create nodes in different positions
# node1 = network.add_node(100, 100, "Hello my friend.")
# node2 = network.add_node(300, 100, "Don't go further down, it is scary.")
# node3 = network.add_node(500, 100, "You should have listened to me, now there is no way home.")
# node4 = network.add_node(300, 300, "Help")
# node5 = network.add_node(100, 300, "Help")
# node6 = network.add_node(500, 300, "Help")
# node7 = network.add_node(300, 500, "Help")
# node8 = network.add_node(100, 500, "Help")
# node9 = network.add_node(500, 500, "Help")
# node10 = network.add_node(700, 300, "Help")
#
# # Connect nodes with neighbors (edges)
# node1.add_neighbor('right', node2)
# node2.add_neighbor('left', node1)
# node2.add_neighbor('right', node3)
# node3.add_neighbor('left', node2)
# node2.add_neighbor('down', node4)
# node4.add_neighbor('up', node2)
# node4.add_neighbor('left', node5)
# node4.add_neighbor('right', node6)
# node4.add_neighbor('down', node7)
# node5.add_neighbor('right', node4)
# node6.add_neighbor('left', node4)
# node7.add_neighbor('up', node4)
# node7.add_neighbor('left', node8)
# node7.add_neighbor('right', node9)
# node8.add_neighbor('right', node7)
# node9.add_neighbor('left', node7)
# node6.add_neighbor('right', node10)
# node10.add_neighbor('left', node6)

G = 'assets/network/fully_connected_15_nodes.gexf'
network = Network()
load_gexf_to_network(G, network)

# Initialize the player at the starting node
player = Player(network.nodes[0], RED)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill(BLACK)
    network.draw(screen, WHITE)
    screen.blit(player.image, player.rect)
    player.draw_message(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
