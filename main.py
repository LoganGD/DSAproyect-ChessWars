import pygame
from grid import Grid
from constants import *
from math import floor
from pieces import *
from deque import Deque
from button import Button
from menu import Menu

def main():
    pygame.init()
    pygame.display.set_caption("Ajedrez 2")
    
    # global objects
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    grid = Grid(screen)
    world = pygame.Surface((grid.width, screen.get_height()))
    side_bar_width = screen.get_width() - grid.width
    side_bar = pygame.Surface((side_bar_width, screen.get_height()))

    # Pieces
    pieces = Deque()
    Piece.pieces = pieces
    Piece.square_size = grid.square_size
    Pawn((1,1))
    Rook((1,3))

    # debug components
    buttons_settings = []
    for piece in Piece.__subclasses__():
        function = lambda position: (position[0] // grid.square_size, position[1] // grid.square_size)
        buttons_settings.append([function, piece.__name__])
    debug_menu = Menu(DEBUG_MENU_SIZE, buttons_settings)
    clicked = None
    debug_screen = pygame.Surface(DEBUG_SCREEN_SIZE)
    font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
    dt,fps = 0,0
    time_since_fps,new_fps = 0,0
    move_timer = 0

    while True:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and clicked:
                    debug_menu.click(mouse, clicked)
                    clicked = False
                if event.button == 3 and DEBUG_MODE:
                    clicked = mouse
  
        # Start rendering
        screen.fill(RAND_RED())

        # World rendering
        world.fill(RAND_GREEN())
        grid.draw(world)
        for piece in pieces:
            piece.draw(world)
        world_rect = world.get_rect( bottomright = screen.get_size() )
        screen.blit(world, world_rect)

        # Side bar rendering
        side_bar.fill(RAND_BLUE())
        side_bar_rect = side_bar.get_rect( bottomleft = (0, screen.get_height()) )
        screen.blit(side_bar, side_bar_rect)
        
        # debug screen
        if DEBUG_MODE:
            text = font.render("FPS: " + str(fps), True, WHITE)
            text_rect = text.get_rect( topleft = (5,5) )
            debug_screen.fill(GRAY)
            debug_screen.blit(text, text_rect)
            debug_screen_rect = debug_screen.get_rect( bottomleft = (0, screen.get_height()) )
            screen.blit(debug_screen, debug_screen_rect)
        if clicked:
            debug_menu.draw(screen, clicked, mouse)

        # Show on screen
        pygame.display.flip()

        # Update clock
        dt = clock.tick(0) / 1000 # limit FPS (0 for unlimited)
        move_timer += dt
        new_fps += 1
        time_since_fps += dt
        if time_since_fps >= 1:
            fps = new_fps
            time_since_fps,new_fps = 0,0
        
if __name__ == "__main__":
    main()