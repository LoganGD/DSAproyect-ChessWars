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
    Pawn(1,1)
    Rook(1,3)

    # debug components
    creators = []
    for piece in Piece.__subclasses__():
        creators.append(Button(piece.__class__))
    debug_menu = Menu(DEBUG_MENU_SIZE, creators)
    clicked = None
    debug_screen = pygame.Surface(DEBUG_SCREEN_SIZE)
    font = pygame.font.Font(TEXT_FONT, 24)
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
                    debug_menu.click(mouse)
                    clicked = False
                if event.button == 3:
                    clicked = mouse
  
        # Start rendering
        screen.fill(PURPLE)

        # Start world rendering
        world.fill(RED)
        grid.draw(world)
        # while move_timer >= 5:
        #     move_timer -= 5
        #     current_piece = pieces.front()
        #     current_piece.move()
        #     pieces.pop_front()
        #     pieces.push_back(current_piece)
        for piece in pieces:
            piece.draw(world, square_size)

        world_rect = world.get_rect(bottomright=(screen.get_width(), screen.get_height()))
        screen.blit(world, world_rect)

        # debug menu
        if clicked:
            pass

        # Side bar rendering
        side_bar.fill(BEIGE)
        for button in buttons:
            button.draw(side_bar, mouse)
        side_bar_rect = side_bar.get_rect(bottomleft=(0, screen.get_height()))
        screen.blit(side_bar, side_bar_rect)
        
        # debug screen (currently just fps)
        if DEBUG_MODE:
            text = font.render("FPS: " + str(fps), True, WHITE)
            text_rect = text.get_rect(topleft=(5,5))
            debug_screen.fill(GRAY)
            debug_screen.blit(text, text_rect)
            debug_screen_rect = debug_screen.get_rect(bottomleft=(0, screen.get_height()))
            screen.blit(debug_screen, debug_screen_rect)

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