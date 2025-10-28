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

        self.position = position
        self.team = team
        self.piece_color = BLACK if team else WHITE
        self.stamina = 5
        self.level = 0

        # preparing base rect
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        piece_name = type(self).__name__
        text = font.render(piece_name, True, self.piece_color, GRAY)
        text_rect = text.get_rect(center = (55 / 2, 20 / 2))
        
        self.back = pygame.Surface((55,20))
        self.back.fill(GRAY)
        self.back.blit(text, text_rect)

        # first draw
        self.draw()


    def draw(self):
        piece_offset = self.offset + pygame.Vector2(self.square_size) / 2
        position = pygame.Vector2(self.position) * self.square_size + piece_offset
        
        back_rect = self.back.get_rect(center = position)
        self.screen.blit(self.back, back_rect)


    def delete(self):
        self.grid.clear(self.position)


    def tick(self):
        pass



class Pawn(Piece):
    def tick(self):
        self.position

        piece = self.grid.get((0,0))
        if piece:
            piece.delete()


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
