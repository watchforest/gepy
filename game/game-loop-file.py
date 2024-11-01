import pygame
from game.config import WIDTH, HEIGHT, FPS, BLACK
from game.create_network import create_network
from game.player import Player
from game.opponent import Opponent
from game.camera import Camera
from game.begin_figure import BeginFigure
from game.button import Button
from game.game_state import GameStateEnum
from game.pause_menu import PauseMenu
from game.settings_menu import SettingsMenu
from game.resource_manager import ResourceManager

# Initialize ResourceManager for game loop
resource_manager = ResourceManager()

def game_loop(screen, clock, game_state):
    # Initialize game objects
    network = create_network('assets/network/random_graph_100_nodes.gexf', WIDTH * 2, HEIGHT * 2)
    player = None
    opponent = None
    camera = Camera(WIDTH, HEIGHT)
    
    # Load the image once using ResourceManager
    begin_figure_image = resource_manager.load_image('begin_figure', 'start_screen_image.png')
    begin_figure = BeginFigure(begin_figure_image, (WIDTH - 850, HEIGHT // 2 - 200), screen)
    
    # Create UI elements
    back_button = Button("main menu", WIDTH - 310, 20, 290, 50,
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
        handle_game_events(event_handler_params(
            game_state, player, opponent, network, camera,
            pause_menu, settings_menu, begin_figure))

        update_game_state(update_params(
            game_state, player, opponent, network, camera))

        draw_game_state(draw_params(
            screen, game_state, network, player, opponent,
            camera, begin_figure, back_button, pause_menu, settings_menu))

        pygame.display.flip()
        clock.tick(FPS)

    # If we've exited the game loop, return to the start screen
    from game.start_screen import start_screen  # Import here to avoid circular import
    start_screen(screen, clock)

def event_handler_params(game_state, player, opponent, network, camera,
                        pause_menu, settings_menu, begin_figure):
    return {
        'game_state': game_state,
        'player': player,
        'opponent': opponent,
        'network': network,
        'camera': camera,
        'pause_menu': pause_menu,
        'settings_menu': settings_menu,
        'begin_figure': begin_figure
    }

def update_params(game_state, player, opponent, network, camera):
    return {
        'game_state': game_state,
        'player': player,
        'opponent': opponent,
        'network': network,
        'camera': camera
    }

def draw_params(screen, game_state, network, player, opponent,
                camera, begin_figure, back_button, pause_menu, settings_menu):
    return {
        'screen': screen,
        'game_state': game_state,
        'network': network,
        'player': player,
        'opponent': opponent,
        'camera': camera,
        'begin_figure': begin_figure,
        'back_button': back_button,
        'pause_menu': pause_menu,
        'settings_menu': settings_menu
    }

def handle_game_events(params):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        if event.type == pygame.KEYDOWN:
            handle_keydown_event(event, params)
        handle_menu_events(event, params)

def handle_keydown_event(event, params):
    if event.key == pygame.K_ESCAPE:
        handle_escape_key(params)
    elif params['game_state'].is_state(GameStateEnum.INTRO_FIGURE):
        initialize_game(params)
    else:
        params['game_state'].handle_keypress()

def handle_escape_key(params):
    if params['game_state'].is_state(GameStateEnum.PLAYING):
        params['game_state'].toggle_pause()
    elif params['game_state'].is_state(GameStateEnum.PAUSED) or \
         params['game_state'].is_state(GameStateEnum.SETTINGS):
        params['game_state'].change_state(GameStateEnum.PLAYING)

def initialize_game(params):
    params['game_state'].change_state(GameStateEnum.PLAYING)
    params['player'] = Player(params['network'].nodes[0], pygame.Color(255, 0, 0))
    params['opponent'] = Opponent(params['network'].nodes[-1], pygame.Color(0, 0, 255), params['network'])
    params['camera'].update(params['player'])

def handle_menu_events(event, params):
    if params['game_state'].is_state(GameStateEnum.PAUSED):
        params['pause_menu'].handle_event(event)
    elif params['game_state'].is_state(GameStateEnum.SETTINGS):
        params['settings_menu'].handle_event(event)

def update_game_state(params):
    params['game_state'].update()
    if params['game_state'].is_state(GameStateEnum.PLAYING) and params['player'] is not None:
        keys = pygame.key.get_pressed()
        params['player'].update(keys, params['network'])
        params['opponent'].update(params['player'], params['network'])
        params['camera'].update(params['player'])

def draw_game_state(params):
    params['screen'].fill(BLACK)
    if not params['game_state'].is_state(GameStateEnum.SETTINGS):
        draw_game_elements(params)
    else:
        params['settings_menu'].draw(params['screen'])

def draw_game_elements(params):
    params['network'].draw(params['screen'], params['camera'])

    if params['game_state'].is_state(GameStateEnum.INTRO_FIGURE):
        params['begin_figure'].draw()
    elif params['game_state'].is_state(GameStateEnum.PLAYING) and params['player'] is not None:
        draw_playing_state(params)
    if params['game_state'].is_state(GameStateEnum.PAUSED):
        params['pause_menu'].draw(params['screen'])

def draw_playing_state(params):
    params['player'].draw(params['screen'], params['camera'])
    params['opponent'].draw(params['screen'], params['camera'])
    params['back_button'].check_for_input(pygame.mouse.get_pos())
    params['back_button'].draw(params['screen'])

def exit_game():
    pygame.quit()
    sys.exit()
