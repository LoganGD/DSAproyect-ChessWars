import pygame
from constants import *

class Grid:
    def __init__(self, surface: pygame.Surface):
        # get dimensions
        self.square_size = surface.get_height() // GRID_HEIGHT
        self.width = self.square_size * GRID_WIDTH
        self.offset = pygame.Vector2(surface.get_width() - self.width, 0)

        # create the grid
        self.cells = [[] for _ in range(GRID_WIDTH)]
        
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                position = pygame.Vector2(i,j)
                square = Square(surface, 
                        position, self.square_size, self.offset)
                self.cells[i].append(square)

class Square:
    def __init__(
        self, 
        surface: pygame.Surface, 
        position: pygame.Vector2, 
        square_size: int, 
        offset: pygame.Vector2
    ):
        self.color = BLACK if sum(position) % 2 else WHITE
        adjusted_position = position * square_size + offset
        size = pygame.Vector2(square_size)
        self.rect = pygame.Rect(*adjusted_position, *size)
        self.clear(surface)


    def clear(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
