from enum import Enum, auto


class GameStateEnum(Enum):
    START_SCREEN = auto()
    INTRO_FIGURE = auto()
    PLAYING = auto()
    PAUSED = auto()
    SETTINGS = auto()
    GAME_OVER = auto()


class GameState:
    def __init__(self):
        self.current_state = GameStateEnum.START_SCREEN
        self.figure_displayed = False
        self.waiting_for_keypress = False
        self.previous_state = None

    def change_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state = new_state

    def is_state(self, state):
        return self.current_state == state

    def update(self):
        if self.is_state(GameStateEnum.INTRO_FIGURE):
            if self.waiting_for_keypress:
                self.figure_displayed = True
                self.waiting_for_keypress = False
                self.change_state(GameStateEnum.PLAYING)

    def start_waiting_for_keypress(self):
        if self.is_state(GameStateEnum.INTRO_FIGURE):
            self.waiting_for_keypress = True

    def handle_keypress(self):
        if self.is_state(GameStateEnum.INTRO_FIGURE) and self.waiting_for_keypress:
            self.change_state(GameStateEnum.PLAYING)
            return True
        return False

    def toggle_pause(self):
        if self.is_state(GameStateEnum.PLAYING):
            self.change_state(GameStateEnum.PAUSED)
        elif self.is_state(GameStateEnum.PAUSED):
            self.change_state(GameStateEnum.PLAYING)

    def enter_settings(self):
        if not self.is_state(GameStateEnum.SETTINGS):
            self.change_state(GameStateEnum.SETTINGS)

    def exit_settings(self):
        if self.is_state(GameStateEnum.SETTINGS):
            self.change_state(self.previous_state)