import pygame
from constants import *
from pieces import *

# empty grid
squares: list[list['Square']] = [[] for _ in range(GRID_WIDTH)]
turn_speed = 0
turn_timer = 0
current_team = 0


def init(screen: pygame.Surface, square_size: int, offset: int):
    global white_square
    global black_square
    global piece_square

    # preparing default sprites
    white_square = pygame.Surface((square_size,square_size))
    white_square.fill(WHITE)
    black_square = pygame.Surface((square_size,square_size))
    black_square.fill(BLACK)
    
    # preparing pieces sprites
    piece_square = dict(),dict()
    size = (square_size // 1.5, square_size // 4)
    center = size[0] // 2, size[1] // 2
    font = pygame.font.Font(FONT_STYLE, square_size // 4)

    for piece in Piece.__subclasses__():
        for team, color in enumerate([WHITE,BLACK]):
            text = font.render(piece.__name__, True, color)
            text_rect = text.get_rect(center = center)
            
            square = pygame.Surface(size)
            square.fill(GRAY)
            square.blit(text, text_rect)

            piece_square[team][piece] = square

    # create the grid
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            position = pygame.Vector2(i,j)
            squares[i].append(Square(screen, position, square_size, offset))

    # Starting placement
    set(Knight((0,4), 0))
    set(King((0,5), 0))
    set(Bishop((0,6), 0))
    set(Pawn((1,4), 0))
    set(Pawn((1,5), 0))
    set(Pawn((1,6), 0))
    
    set(Knight((15,4), 1))
    set(King((15,5), 1))
    set(Bishop((15,6), 1))
    set(Pawn((14,4), 1))
    set(Pawn((14,5), 1))
    set(Pawn((14,6), 1))


def set(piece: Piece):
    x,y = piece.position
    squares[x][y].set(piece)


def clear(piece: Piece):
    x,y = piece.position
    squares[x][y].set(None)


def update(current_time: float, selection: list | None, option: str | None):
    global turn_timer
    global turn_speed
    global current_team

    if option == "Pause":
        turn_speed = 0
    if option == "Continue":
        turn_speed = 1
    if option == "Death":
        Death()

    if (current_time - turn_timer) * turn_speed > 1:
        turn_timer = current_time

        for piece in Piece.deque[current_team]:
            piece.tick()
        print()

        current_team = 1 - current_team


class Square:
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2, square_size: int, offset: int):
        self.screen = screen

        # drawing variables
        drawing_offset = offset + square_size // 2, square_size // 2
        self.drawing_position = position * square_size + drawing_offset

        if sum(position) % 2:
            self.default_sprite = black_square
        else:
            self.default_sprite = white_square

        # first draw
        self.set(None)


    def set(self, piece: Piece):
        self.piece = piece

        # clear the square
        square_rect = self.default_sprite.get_rect(center = self.drawing_position)
        self.screen.blit(self.default_sprite, square_rect)

        # if piece on square draw it's sprite
        if piece:
            square = piece_square[piece.team][type(piece)]
            square_rect = square.get_rect(center = self.drawing_position)
            self.screen.blit(square, square_rect)
