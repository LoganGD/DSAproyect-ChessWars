import pygame
from constants import *

class Piece:
    def __init__(self, position: tuple[int]):
        self.pieces.push_back(self)
        self.position = pygame.Vector2(position)

    def draw(self, world: pygame.Surface):
        pos_x = ( self.position.x + 1/2 ) * self.square_size
        pos_y = ( self.position.y + 1/2 ) * self.square_size

        font_size = 20
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(type(self).__name__, True, BLACK, GRAY)
        text_rect = text.get_rect(center = (pos_x, pos_y))
        world.blit(text, text_rect)


class Pawn(Piece):
    def __init__(self, position: tuple[int]):
        super().__init__(position)
        self.name = "Pawn"


class Rook(Piece):
    def __init__(self, position: tuple[int]):
        super().__init__(position)
        self.name = "Rook"
