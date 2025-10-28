import pygame
from constants import *
from pieces import Piece


class Grid:
    def __init__(self, surface: pygame.Surface):
        # get dimensions
        self.surface = surface
        self.square_size = surface.get_height() // GRID_HEIGHT
        self.width = self.square_size * GRID_WIDTH
        self.offset = pygame.Vector2(surface.get_width() - self.width, 0)

        # create the grid
        self.cells: list[list[Square]] = [[] for _ in range(GRID_WIDTH)]
        
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                position = pygame.Vector2(i,j)
                square = Square(surface, 
                        position, self.square_size, self.offset)
                self.cells[i].append(square)


    def clear(self, position: tuple[int, int]):
        self.cells[position[0]][position[1]].draw(self.surface)
        self.cells[position[0]][position[1]].piece = None
    
    def set(self, position: tuple[int, int], piece: Piece):
        if self.cells[position[0]][position[1]].piece:
            raise Exception(f'There is already a piece at f{position}')

        self.cells[position[0]][position[1]].piece = piece
    

    def get(self, position: tuple[int, int]):
        return self.cells[position[0]][position[1]].piece



class Square:
    def __init__(
        self, 
        surface: pygame.Surface, 
        position: pygame.Vector2, 
        square_size: int, 
        offset: pygame.Vector2
    ):
        self.color = BLACK if sum(position) % 2 else WHITE
        self.piece: Piece | None = None

        adjusted_position = position * square_size + offset
        size = pygame.Vector2(square_size)

        self.rect = pygame.Rect(*adjusted_position, *size)
        self.base = pygame.Surface(size)
        self.base.fill(self.color)

        self.draw(surface)


    def draw(self, surface: pygame.Surface):
        surface.blit(self.base, self.rect)
