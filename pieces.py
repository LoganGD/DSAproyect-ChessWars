import pygame
from constants import *
from deque import Deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grid import Grid    


class Piece:
    screen: pygame.Surface
    grid: 'Grid'
    pieces_deque: Deque['Piece']
    square_size: int
    offset: pygame.Vector2

    def __init__(self, position: tuple[int, int], team: int = 0):
        self.pieces_deque.push_back(self)
        self.grid.set(position, self)

        self.position = pygame.Vector2(position)
        self.team = team
        self.piece_color = BLACK if team else WHITE
        self.stamina = 5
        self.level = 0
        self.draw()


    def draw(self):
        piece_offset = self.offset + pygame.Vector2(self.square_size) / 2
        position = self.position * self.square_size + piece_offset
        
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        piece_name = type(self).__name__
        text = font.render(piece_name, True, self.piece_color, GRAY)
        text_rect = text.get_rect(center = (55 / 2, 20 / 2))
        
        back = pygame.Surface((55,20))
        back.fill(GRAY)
        back.blit(text, text_rect)
        back_rect = back.get_rect(center = position)
        self.screen.blit(back, back_rect)


    def undraw(self):
        color = BLACK if sum(self.position) % 2 else WHITE
        position = self.position * self.square_size + self.offset
        draw_position = (*position, self.square_size, self.square_size)
        pygame.draw.rect(self.screen, color, draw_position)


    def tick(self):
        pass



class Pawn(Piece):
    pass

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass



pieces_dict: dict[str, type[Piece]] = dict()
for piece in Piece.__subclasses__():
    pieces_dict[piece.__name__.lower()] = piece
