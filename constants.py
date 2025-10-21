from random import randint

def RAND_RED():
    return (randint(0,255),0,0)
def RAND_GREEN():
    return (0,randint(0,255),0)
def RAND_BLUE():
    return (0,0,randint(0,255))

DEBUG_MODE = True

# screenn size (0,0) sets fullscreen
SCREEN_SIZE = (0,0)
DEBUG_MENU_SIZE = (100,100)
DEBUG_SCREEN_SIZE = (80,25)

GRID_HEIGHT = 12
SIDE_BAR_MIN_WIDTH = 360

FONT_STYLE = None # None for default
FONT_SIZE = 24

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (150,150,150)
BEIGE = (245,245,220)

COLOR_LIGHT = (170,170,170)
COLOR_DARK = (100,100,100)
