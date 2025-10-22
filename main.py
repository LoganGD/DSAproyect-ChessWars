import pygame
from constants import *
from grid import Grid
from pieces import *
from deque import Deque
from console import Console

def main():
    pygame.init()
    pygame.display.set_caption("Chess 2")
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    grid = Grid(screen)
    console = Console(screen, (grid.offset.x - 10, 100))
        
    pieces_deque = Deque()
    Piece.pieces_deque = pieces_deque
    Piece.square_size = grid.square_size
    Piece.screen = screen
    Piece.offset = grid.offset

    order = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
    for i in range(8):
        order[i]((0,i+2))
        Pawn((1,i+2))
        Pawn((14,i+2),True)
        order[i]((15,i+2),True)

    inputs = ""
    debug = False
    dt,fps = 0,0
    
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if debug:
                    console.process_key(event.key, event.unicode)
                    console.draw()
                else:
                    inputs += event.unicode.lower()
                    if inputs[-3:] == "135":
                        debug = True
                        console.draw()
        
        for piece in pieces_deque:
            if not piece.drawed:
                piece.draw()

        if debug:
            console.show_fps(fps)
        
        pygame.display.flip()
        dt = clock.tick(0) # limit FPS (0 for unlimited)
        fps += (clock.get_fps() - fps) * dt / 1000


if __name__ == "__main__":
    main()