import pygame
from constants import *
from pieces.pieces import *
from deque import Deque
from grid import Grid
from console import Console
from button import Button
from events import create_default


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
    orders = Deque[str]()
    Piece.screen = screen
    Piece.grid = grid
    Piece.pieces_deque = pieces_deque
    # Piece.orders = orders
    Piece.square_size = grid.square_size
    Piece.offset = grid.offset


    global time_speed
    time_speed = 0

    # create buttons
    buttons: list[Button] = []
    Button.buttons_list = buttons

    size = 100, 50

    position = 50, 50    
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Attack", lambda:orders.push_back("Attack"))
    
    position = 160, 50
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Defend", lambda:orders.push_back("Defend"))

    position = 50, 110
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Opt 3", lambda:orders.push_back("Opt 3"))
    
    position = 160, 110
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Opt 4", lambda:orders.push_back("Opt 4"))

    def setSpeed(speed: int):
        global time_speed
        time_speed = speed

    position = 50, 170
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Pause", lambda:setSpeed(0))
    
    position = 160, 170
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Continue", lambda:setSpeed(1))

    # temporary piece placement
    # create_default(0)
    # create_default(1)

    # variables
    current_team = 0
    turn_timer = 0
    fps_timer = 0
    timer = 0
    dt,fps = 0,0

    inputs = ""
    debug = False
    
    while True:
        mouse = pygame.Vector2(pygame.mouse.get_pos())

        for event in pygame.event.get():
            # close the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.click(mouse)

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

        # buttons
        for button in buttons:
            button.draw(mouse)

        # piece turns
        if time_speed and timer - turn_timer > TIMER_SECONDS:
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