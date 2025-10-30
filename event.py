import random
import grid
from constants import *

def random_event():
    random.choice(
        create_resources
    )()

def create_resources():
    for _ in range(3):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        while grid.get_piece((x,y)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
        
        grid.set_resouce((x,y), GRASS_BALL)