import pygame
from constants import *
from deque import Deque
from pqueue import Pqueue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grid import Grid


class Piece:
    screen: pygame.Surface
    grid: 'Grid'
    pieces_deque: Deque['Piece']
    square_size: int
    offset: pygame.Vector2

    moves: list[tuple[int, int]]

    def __init__(self, position: tuple[int, int], team: int = 0):
        self.pieces_deque.push_back(self)
        self.grid.set(position, self)

        self.position = position
        self.team = team
        self.piece_color = BLACK if team else WHITE
        
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


    def undraw(self):
        self.grid.clear(self.position)


    def delete(self):
        self.grid.clear(self.position)



    def tick(self):
        pass

def valid(move_x, move_y):
    if move_x < 0 or move_x >= GRID_WIDTH:
        return False
    if move_y < 0 or move_y >= GRID_HEIGHT:
        return False
    return True

def reward(piece, team, pos_x):
    if piece.__class__ == Pawn:
        value = 10-abs(2*pos_x - 15)
        if team == 0:
            value += 4*pos_x
        else:
            value += 4*(16-pos_x)

    if piece.__class__ == Knight:
        value = 10-abs(2*pos_x - 15)
    
    if piece.__class__ == Bishop:
        value = 10-abs(2*pos_x - 15)
    
    if piece.__class__ == Rook:
        value = 10-abs(2*pos_x - 15)
    
    if piece.__class__ == Queen:
        value = 10-abs(2*pos_x - 15)

    if piece.__class__ == King:
        if team == 0:
            value = pos_x * 5
        else:
            value = (15 - pos_x)*5
        
    return value


pieces_dict: dict[str, type[Piece]] = dict()
for piece in Piece.__subclasses__():
    pieces_dict[piece.__name__.lower()] = piece
