import pygame
from constants import *

class Piece:
    def __init__(self, position: tuple[int], is_enemy: bool = False):
        self.pieces_deque.push_back(self)
        self.position = pygame.Vector2(position)
        self.is_enemy = is_enemy
        self.piece_color = BLACK if self.is_enemy else WHITE
        self.drawed = False

    def draw(self):
        piece_offset = self.offset + pygame.Vector2(self.square_size, self.square_size) / 2
        position = self.position * self.square_size + piece_offset
        
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        text = font.render(type(self).__name__, True, self.piece_color, GRAY)
        text_rect = text.get_rect(center = (55 / 2, 20 / 2))
        
        back = pygame.Surface((55,20))
        back.fill(GRAY)
        back.blit(text, text_rect)
        back_rect = back.get_rect(center=position)
        self.screen.blit(back, back_rect)

        self.drawed = True
    
    def clear(self):
        color = BLACK if sum(self.position) % 2 else WHITE
        position = self.position * self.square_size + self.offset
        draw_position = (*position, self.square_size, self.square_size)
        pygame.draw.rect(self.screen, color, draw_position)

        self.drawed = False


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


pieces_dict = dict()
for piece in Piece.__subclasses__():
    pieces_dict[piece.__name__.lower()] = piece
