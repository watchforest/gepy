import pygame
import sys
from game.config import WIDTH, HEIGHT, FPS, BLACK, WHITE
from game.button import Button
from game.resource_manager import ResourceManager
from game.game_state import GameState, GameStateEnum
from game.game_loop import game_loop

# Initialize ResourceManager
resource_manager = ResourceManager()

def start_screen(screen, clock):
    game_state = GameState()

    # Load assets using ResourceManager
    start_screen_image = resource_manager.load_image('start_screen', 'start_screen_image.png')
    start_screen_image = resource_manager.scale_image('start_screen', 0.5)  # Scale to 50% of original size

    # Load and play background music
    resource_manager.load_music('background', 'background_music.mp3')
    resource_manager.play_music('background')

    # Create buttons
    start_button = Button("Start", WIDTH // 4 - 150, HEIGHT // 2 + 100, 300, 75,
                          lambda: game_loop(screen, clock, game_state))
    exit_button = Button("exit game", WIDTH - 250, 50, 200, 75, exit_game)
    buttons = [start_button, exit_button]

    # Main loop
    while game_state.is_state(GameStateEnum.START_SCREEN):
        handle_events(buttons)
        draw_start_screen(screen, buttons, start_screen_image)
        pygame.display.flip()
        clock.tick(FPS)

def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            for button in buttons:
                button.check_for_input(mouse_position)

def draw_start_screen(screen, buttons, start_screen_image):
    screen.fill(BLACK)
    title_font = resource_manager.get_font(200)
    title_surface = title_font.render("ge.py", True, WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

    for button in buttons:
        button.draw(screen)

    screen.blit(start_screen_image,
                (WIDTH - start_screen_image.get_width() - 50, HEIGHT // 2 - start_screen_image.get_height() // 4))

def exit_game():
    pygame.quit()
    sys.exit()
