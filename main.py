import pygame
from constants import *
from pieces import *
from deque import Deque
from grid import Grid
from console import Console


def main():
    pygame.init()
    pygame.display.set_caption("Chess 2") # window title

    # global objects
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(PURPLE)
    grid = Grid(screen)
    
    # debugging console
    position = 10, screen.get_height() - 110
    size = grid.offset.x - 20, 100
    console_rect = pygame.Rect(*position, *size)
    console = Console(screen, console_rect)

    # initialize pieces structures
    pieces_deque = Deque[Piece]()
    Piece.screen = screen
    Piece.screen = screen
    Piece.grid = grid
    Piece.pieces_deque = pieces_deque
    Piece.square_size = grid.square_size
    Piece.offset = grid.offset

    # temporary piece placement
    order: list[type[Piece]] = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece in enumerate(order):
        piece((0,i+2), team = 0)
        Pawn((1,i+2), team = 0)
        Pawn((14,i+2), team = 1)
        piece((15,i+2), team = 1)

    # variables
    current_team = 0
    turn_timer = 0
    fps_timer = 0
    timer = 0
    dt,fps = 0,0

    inputs = ""
    debug = False
    
    while True:
        for event in pygame.event.get():
            # close the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # keyboard keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                
                # check for debugging
                if debug:
                    console.process_key(event.key, event.unicode)
                    console.draw()
                else:
                    inputs += event.unicode
                    if inputs[-3:] == DEBUG_CODE:
                        debug = True
                        console.draw()

        # piece turns
        if timer - turn_timer > TIMER_SECONDS:
            turn_timer = timer

            for piece in pieces_deque:
                if piece.team == current_team:
                    piece.tick()
            current_team = 1 - current_team

        # debug fps
        if debug and timer - fps_timer > 1:
            fps_timer = timer
            console.show_fps(fps)

        # show on screen
        pygame.display.flip()

        # clock
        dt = clock.tick(0) # limit FPS (0 for unlimited)
        timer += dt / 1000
        fps += (clock.get_fps() - fps) * dt / 1000



if __name__ == "__main__":
    main()