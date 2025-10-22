import pygame
from constants import *

class Grid:
    def __init__(self, screen: pygame.Surface):
        # get dimensions
        self.square_size = screen.get_height() // GRID_HEIGHT
        self.width = self.square_size * GRID_WIDTH
        self.offset = pygame.Vector2(screen.get_width() - self.width, 0)
        
        # create the grid
        self.cells = [[] for _ in range(GRID_WIDTH)]
        
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                position = pygame.Vector2(i,j)
                self.cells[i].append(Square(screen, position, self.square_size, self.offset))

class Square:
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2, square_size: int, offset: pygame.Vector2):
        self.position = position
        self.square_size = square_size
        self.color = BLACK if sum(position) % 2 else WHITE
        position = position * square_size + offset
        draw_position = (*position, square_size, square_size)
        pygame.draw.rect(screen, self.color, draw_position)
