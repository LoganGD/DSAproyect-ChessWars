import pygame
from constants import *

# empty grid
squares: list[list['Square']] = [[] for _ in range(GRID_WIDTH)]
turn_speed = 0
turn_timer = 1000
current_team = 0


def init(screen: pygame.Surface, grid_square_size: int, offset: int):
    global square_size
    square_size = grid_square_size

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

    from pieces import Piece,Pawn,Rook,Knight,Bishop,Queen,King
    for piece in Piece.__subclasses__():
        for team in range(2):
            image_path = f"assets/{piece.__name__}_{team}.png"

            image = pygame.image.load(image_path).convert_alpha()

            w, h = image.get_size()
            scale = (square_size * 0.6) / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            image = pygame.transform.smoothscale(image, new_size)

            piece_sprites[team][piece] = image

    # create the grid
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            position = pygame.Vector2(i,j)
            squares[i].append(Square(screen, position, square_size, offset))

    # Starting placement
    Rook((0,2), 0)
    Knight((0,3), 0)
    Bishop((0,4), 0)
    Queen((0,5),0)
    King((0,6), 0)
    Bishop((0,7), 0)
    Knight((0,8), 0)
    Rook((0,9), 0)

    Pawn((1,2), 0)
    Pawn((1,3), 0)
    Pawn((1,4), 0)
    Pawn((1,5), 0)
    Pawn((1,6), 0)
    Pawn((1,7), 0)
    Pawn((1,8), 0)
    Pawn((1,9), 0)


    Rook((15,2), 1)
    Knight((15,3), 1)
    Bishop((15,4), 1)
    Queen((15,5),1)
    King((15,6), 1)
    Bishop((15,7), 1)
    Knight((15,8), 1)
    Rook((15,9), 1)

    Pawn((14,2), 1)
    Pawn((14,3), 1)
    Pawn((14,4), 1)
    Pawn((14,5), 1)
    Pawn((14,6), 1)
    Pawn((14,7), 1)
    Pawn((14,8), 1)
    Pawn((14,9), 1)
    
   

    



def get_piece(position: pygame.Vector2):
    x,y = position
    x = round(x)
    y = round(y)
    if x < 0 and x >= GRID_WIDTH and y < 0 and y >= GRID_HEIGHT:
        raise Exception("out of bounds")
    return squares[x][y].piece
    
def set_piece(piece):
    x,y = piece.position
    x = round(x)
    y = round(y)
    if x < 0 and x >= GRID_WIDTH and y < 0 and y >= GRID_HEIGHT:
        raise Exception("out of bounds")
    squares[x][y].set(piece)


def clear(piece):
    x,y = piece.position
    x = round(x)
    y = round(y)
    if x < 0 and x >= GRID_WIDTH and y < 0 and y >= GRID_HEIGHT:
        raise Exception("out of bounds")
    squares[x][y].set(None)


def update(dt: float, clicked: list | None, action: str | None):
    global turn_timer
    global turn_speed
    global current_team

    if clicked:
        x,y = clicked[0]
        if x >= 0 and x < GRID_WIDTH and y >= 0 and y < GRID_HEIGHT:
            if squares[x][y].piece and squares[x][y].piece.team == 0:
                squares[x][y].piece.selected = clicked[1]
                set_piece(squares[x][y].piece)

    from pieces import Piece

    if action == "Pause":
        turn_speed = 0
    elif action == "Slow":
        turn_speed = 1
    elif action == "Fast":
        turn_speed = 3
    elif action == "UFast":
        turn_speed = 15
    elif action:
        for piece in Piece.deque[0]:
            if piece.selected:
                piece.current_order = action
                piece.selected = False
                set_piece(piece)
    
    turn_timer -= turn_speed * dt
    if turn_timer <= 0:
        turn_timer += 1000

        for piece in Piece.deque[current_team]:
            piece.tick()

        current_team = not current_team


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


    def set(self, piece):
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

            stamina_bar = pygame.Surface((square_size, square_size * 0.2))
            offset = square_size * 0.02
            for i in range(piece.stamina):
                pygame.draw.rect(stamina_bar, GREEN, 
                        (i / piece.max_stamina * (square_size - 3 * offset) + offset,
                         offset, 
                         1 / piece.max_stamina * square_size - offset * 3,
                         square_size * 0.15 - offset * 2))
                
            stamina_bar_rect = stamina_bar.get_rect(
                midbottom = self.drawing_position + (0, square_size * 0.5))
            self.screen.blit(stamina_bar, stamina_bar_rect)

