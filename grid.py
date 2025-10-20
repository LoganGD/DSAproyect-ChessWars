import pygame
from constants import *

class Grid:
    def __init__(self, screen: pygame.Surface):
        # get dimensions
        self.square_size = screen.get_height() / GRID_HEIGHT
        self.grid_width = (screen.get_width() - SIDE_BAR_MIN_WIDTH) // self.square_size
        self.grid_width = int(self.grid_width)
        self.grid_height = GRID_HEIGHT
        self.width = self.grid_width * self.square_size
        # create the grid
        self.cells = [[] for _ in range(self.grid_width)]

        for i in range(self.grid_width):
            for j in range(self.grid_height):
                self.cells[i].append(Square(i,j))

    def draw(self, world: pygame.Surface):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                self.cells[i][j].draw(world, self.square_size)
        
class Square:
    def __init__(self, pos_x: float, pos_y: float):
        self.position = pygame.Vector2(pos_x, pos_y)
        self.color = WHITE if ( pos_x + pos_y ) % 2 == 0 else BLACK
    
    def draw(self, world: pygame.Surface, square_size: float):
        pos_x,pos_y = self.position * square_size
        draw_position = (pos_x, pos_y, square_size, square_size)
        pygame.draw.rect(world, self.color, draw_position)
