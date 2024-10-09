import pygame
import sys
from game.config import WIDTH, HEIGHT, FPS, BLACK, WHITE
from game.create_network import create_network
from game.player import Player
from game.button import Button
from game.camera import Camera
from game.begin_figure import BeginFigure
from game.game_state import GameState, GameStateEnum
from game.pause_menu import PauseMenu
from game.settings_menu import SettingsMenu
from game.resource_manager import ResourceManager

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
    exit_button = Button("Exit Game", WIDTH - 250, 50, 200, 75, exit_game)
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
    title_surface = title_font.render("SYNDESI", True, WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

    for button in buttons:
        button.draw(screen)

    screen.blit(start_screen_image,
                (WIDTH - start_screen_image.get_width() - 50, HEIGHT // 2 - start_screen_image.get_height() // 4))


def game_loop(screen, clock, game_state):
    # Initialize game objects
    network = create_network('assets/network/random_graph_100_nodes.gexf')
    player = Player(network.nodes[0], pygame.Color(255, 0, 0))
    camera = Camera(WIDTH, HEIGHT)

    # Load the image once using ResourceManager
    begin_figure_image = resource_manager.load_image('begin_figure', 'start_screen_image.png')
    begin_figure = BeginFigure(begin_figure_image, (WIDTH - 850, HEIGHT // 2 - 200), screen)

    back_button = Button("Main Menu", WIDTH - 310, 20, 290, 50,
                         lambda: game_state.change_state(GameStateEnum.START_SCREEN))

    pause_menu = PauseMenu(
        resume_action=game_state.toggle_pause,
        settings_action=game_state.enter_settings,
        exit_action=exit_game
    )

    settings_menu = SettingsMenu(back_action=game_state.exit_settings)

    game_state.change_state(GameStateEnum.INTRO_FIGURE)

    # Main game loop
    while not game_state.is_state(GameStateEnum.START_SCREEN):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state.is_state(GameStateEnum.PLAYING):
                        game_state.toggle_pause()
                    elif game_state.is_state(GameStateEnum.PAUSED) or game_state.is_state(GameStateEnum.SETTINGS):
                        game_state.change_state(GameStateEnum.PLAYING)
                else:
                    game_state.handle_keypress()

            if game_state.is_state(GameStateEnum.PAUSED):
                pause_menu.handle_event(event)
            elif game_state.is_state(GameStateEnum.SETTINGS):
                settings_menu.handle_event(event)

        # Update game state
        game_state.update()

        if game_state.is_state(GameStateEnum.PLAYING):
            keys = pygame.key.get_pressed()
            player.update(keys)
            camera.update(player)
        elif game_state.is_state(GameStateEnum.INTRO_FIGURE) and begin_figure.show_button:
            game_state.start_waiting_for_keypress()

        # Draw game
        screen.fill(BLACK)

        if not game_state.is_state(GameStateEnum.SETTINGS):
            network.draw(screen, WHITE, camera)

            if game_state.is_state(GameStateEnum.INTRO_FIGURE):
                begin_figure.draw()
            elif game_state.is_state(GameStateEnum.PLAYING) or game_state.is_state(GameStateEnum.PAUSED):
                player.draw(screen, camera.camera)

            back_button.check_for_input(pygame.mouse.get_pos())
            back_button.draw(screen)

        if game_state.is_state(GameStateEnum.PAUSED):
            pause_menu.draw(screen)
        elif game_state.is_state(GameStateEnum.SETTINGS):
            settings_menu.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    # If we've exited the game loop, return to the start screen
    start_screen(screen, clock)


def exit_game():
    pygame.quit()
    sys.exit()