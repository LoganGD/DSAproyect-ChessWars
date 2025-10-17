import pygame
from math import floor, ceil
from constants import *

class Grid:
    def __init__(self, grid_width, grid_height):
        self.width = grid_width
        self.height = grid_height
        # create the grid
        self.cells = [[] for _ in range(self.width)]

        for i in range(self.width):
            for j in range(self.height):
                self.cells[i].append(Square(i,j))

    def draw(self, world: pygame.Surface):
        for i in range(self.width):
            for j in range(self.height):
                self.cells[i][j].draw(world)
        
class Square:
    def __init__(self, pos_x, pos_y):
        self.position = pygame.Vector2(pos_x, pos_y)
        self.color = WHITE if ( pos_x + pos_y ) % 2 == 0 else BLACK
    
    def draw(self, world: pygame.Surface):
        cell_size = world.get_height() / GRID_HEIGHT
        draw_position = self.position * cell_size
        pygame.draw.rect(world, self.color, (draw_position.x, draw_position.y, cell_size, cell_size))
