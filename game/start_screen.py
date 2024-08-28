import pygame
import sys
import os
import game.colors as colors
from game.create_network import create_network  
from game.player import Player  
from game.camera import Camera
from game.begin_figure import BeginFigure

# Initialize Pygame
pygame.init()

# Define constants
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME, pygame.OPENGL, vsync=1)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Syndesi")
clock = pygame.time.Clock()
FPS = 60

# Determine the base directory of the project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
font_path = os.path.join(base_dir, 'assets', 'font', 'Pastor of Muppets.TTF')

# Load the title font
title_font = pygame.font.Font(font_path, 200)

# Setup font for button rendering
button_font = pygame.font.Font(None, 74)

# Load the image for the start screen
image_path = os.path.join(base_dir, 'assets', 'images', 'start_screen_image.png')
start_screen_image = pygame.image.load(image_path).convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (600, 600))

# Button class to handle the buttons
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = colors.WHITE  # Button color is initially WHITE
        self.text_color = colors.BLACK  # Text color is initially BLACK
        self.hovered = False
        self.action = action
        self.font = pygame.font.Font(font_path, 74)

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
