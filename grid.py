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
    global white_blue_square
    global black_blue_square
    global piece_sprites

    # preparing default sprites
    white_square = pygame.Surface((square_size,square_size))
    white_square.fill(WHITE)
    black_square = pygame.Surface((square_size,square_size))
    black_square.fill(BLACK)
    white_blue_square = pygame.Surface((square_size,square_size))
    white_blue_square.fill(WHITE_BLUE)
    black_blue_square = pygame.Surface((square_size,square_size))
    black_blue_square.fill(BLACK_BLUE)
    
    # preparing pieces sprites
    piece_sprites = dict(),dict()
    size = (square_size // 1.5, square_size // 4)
    center = size[0] // 2, size[1] // 2
    font = pygame.font.Font(FONT_STYLE, square_size // 4)

    for piece in Piece.__subclasses__():
        for team, color in enumerate([WHITE, BLACK]):
            text = font.render(piece.__name__, True, color)
            text_rect = text.get_rect(center = center)
            
            square = pygame.Surface(size)
            square.fill(GRAY)
            square.blit(text, text_rect)

            piece_sprites[team][piece] = square

    # create the grid
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            position = pygame.Vector2(i,j)
            squares[i].append(Square(screen, position, square_size, offset))

    # Starting placement
    Knight((0,4), 0)
    King((0,5), 0)
    Bishop((0,6), 0)
    Pawn((1,4), 0)
    Pawn((1,5), 0)
    Pawn((1,6), 0)
    
    Knight((15,4), 1)
    King((15,5), 1)
    Bishop((15,6), 1)
    Pawn((14,4), 1)
    Pawn((14,5), 1)
    Pawn((14,6), 1)


def get(position: pygame.Vector2):
    if x < 0 and x >= GRID_WIDTH and y < 0 and y >= GRID_HEIGHT:
        raise Exception("out of bounds")
    x,y = position
    return squares[x][y].piece
    
def set(piece: Piece):
    if x < 0 and x >= GRID_WIDTH and y < 0 and y >= GRID_HEIGHT:
        raise Exception("out of bounds")
    x,y = piece.position
    squares[x][y].set(piece)


def clear(piece: Piece):
    if x < 0 and x >= GRID_WIDTH and y < 0 and y >= GRID_HEIGHT:
        raise Exception("out of bounds")
    x,y = piece.position
    squares[x][y].set(None)


def update(current_time: float, clicked: list | None, action: str | None):
    global turn_timer
    global turn_speed
    global current_team

    if clicked:
        x,y = clicked[0]
        if x >= 0 and x < GRID_WIDTH and y >= 0 and y < GRID_HEIGHT:
            if squares[x][y].piece and squares[x][y].piece.team == 0:
                squares[x][y].piece.selected = clicked[1]
                set(squares[x][y].piece)

    if action == "Pause":
        turn_speed = 0
    elif action == "Slow":
        turn_speed = 1
    elif action == "Fast":
        turn_speed = 3
    elif action:
        for piece in Piece.deque[0]:
            if piece.selected:
                piece.current_order = action
                piece.selected = False
                set(piece)
    
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
            self.selected_sprite = black_blue_square
        else:
            self.default_sprite = white_square
            self.selected_sprite = white_blue_square

        # first draw
        self.set(None)


    def set(self, piece: Piece):
        self.piece = piece

        # clear the square
        if piece and piece.selected:
            square_rect = self.selected_sprite.get_rect(center = self.drawing_position)
            self.screen.blit(self.selected_sprite, square_rect)
        else:
            square_rect = self.default_sprite.get_rect(center = self.drawing_position)
            self.screen.blit(self.default_sprite, square_rect)

        # if piece on square draw it's sprite
        if piece:
            square = piece_sprites[piece.team][type(piece)]
            square_rect = square.get_rect(center = self.drawing_position)
            self.screen.blit(square, square_rect)
