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

