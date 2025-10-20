import pygame
from constants import *

class Piece:
    def __init__(self, pos_x: float, pos_y: float):
        self.position = pygame.Vector2(pos_x, pos_y)
        self.pieces.push_back(self)

    def draw(self, world: pygame.Surface, square_size: int):
        pos_x = ( self.position.x + 1/2 ) * square_size
        pos_y = ( self.position.y + 1/2 ) * square_size

        font_size = 20
        font = pygame.font.Font(TEXT_FONT, font_size)
        text = font.render(self.name, True, BLACK, GRAY)
        text_rect = text.get_rect(center = (pos_x, pos_y))
        world.blit(text, text_rect)


class Pawn(Piece):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.name = "Pawn"


class Rook(Piece):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.name = "Rook"
