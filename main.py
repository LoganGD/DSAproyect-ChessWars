import pygame
from grid import Grid
from constants import *
from math import floor
from pieces import *

def main():
    pygame.init()
    pygame.display.set_caption("Ajedrez 2")
    
    # global objects
    screen = pygame.display.set_mode()
    clock = pygame.time.Clock()
    square_size = screen.get_height() / GRID_HEIGHT
    grid_width = floor((screen.get_width() - SIDE_BAR_MIN_WIDTH) / square_size)
    world_width = grid_width * square_size
    world = pygame.Surface((world_width, screen.get_height()))
    grid = Grid(grid_width, GRID_HEIGHT)
    side_bar = pygame.Surface((screen.get_width() - world_width, screen.get_height()))

    pieces = pygame.sprite.Group()
    Piece.containers = (pieces)

    pawn = Pawn(1,1)
    rook = Rook(1,3)

    # debug components
    debug_screen = pygame.Surface((80, 25))
    font = pygame.font.Font(None, 24) # None for default
    dt,fps = 0,0
    time_since_fps,new_fps = 0,0
    move_timer = 0

    while True:
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                return
            
        # Start rendering
        screen.fill(PURPLE)

        # Start world rendering
        world.fill(RED)
        grid.draw(world)
        for piece in pieces:
            piece.draw(world, square_size)
        if move_timer >= 5:
            move_timer -= 5
            
        world_rect = world.get_rect(bottomright=(screen.get_width(), screen.get_height()))
        screen.blit(world, world_rect)

        # Side bar rendering
        side_bar.fill(BEIGE)
        side_bar_rect = side_bar.get_rect(bottomleft=(0, screen.get_height()))
        screen.blit(side_bar, side_bar_rect)
        
        # debug screen (currently just fps)
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