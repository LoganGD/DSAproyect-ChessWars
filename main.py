import pygame
from math import ceil
from constants import *
from grid import Grid
from animal import Cow

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((1080,720))
    pygame.display.set_caption("Title")

    screen_width, screen_height = screen.get_size()

    # global objects
    clock = pygame.time.Clock()
    grid = Grid()
    world = pygame.Surface((screen_width, screen_height - 25))
    debug_screen = pygame.Surface((80, 25))
    camera = pygame.Vector3(
        ( GRID_WIDTH  - screen_width  / ZOOM ) / 2,
        ( GRID_HEIGHT - screen_height / ZOOM ) / 2,
        ZOOM
    )

    # cow
    cows = pygame.sprite.Group()
    Cow.containers = (cows)
    for _ in range(100):
        cow = Cow(GRID_WIDTH / 2, GRID_HEIGHT / 2)

    # debug components
    font_size = 24
    font = pygame.font.Font(None, font_size) # None for default
    dt,fps = 0,0
    time_since_fps,new_fps = 0,0

    while True:
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                return
            if event.type == pygame.MOUSEWHEEL:
                # Limit the camera from being bigger than the world size
                camera.z = ceil(max([
                    camera.z + event.y,
                    world.get_width() / GRID_WIDTH,
                    world.get_height() / GRID_HEIGHT
                ]))
            
        # Handle WASD movement
        if keys[pygame.K_w]:
            camera.y -= dt * CAMERA_SPEED
        if keys[pygame.K_a]:
            camera.x -= dt * CAMERA_SPEED
        if keys[pygame.K_s]:
            camera.y += dt * CAMERA_SPEED
        if keys[pygame.K_d]:
            camera.x += dt * CAMERA_SPEED

        # Keep the camera withing borders
        camera.x = max(camera.x, 0)
        camera.y = max(camera.y, 0)
        camera.x = min(camera.x, GRID_WIDTH - world.get_width() / camera.z)
        camera.y = min(camera.y, GRID_HEIGHT - world.get_height() / camera.z)
        
        # Start rendering
        screen.fill(PURPLE)
        screen_width, screen_height = screen.get_size()

        # debug screen (currently just fps)
        text = font.render("FPS: " + str(fps), True, WHITE)
        text_rect = text.get_rect(topleft=(5,5))
        debug_screen.fill(GRAY)
        debug_screen.blit(text, text_rect)
        debug_screen_rect = debug_screen.get_rect(topright=(screen_width, 0))
        screen.blit(debug_screen, debug_screen_rect)

        # Start world rendering
        world.fill(RED)
        grid.draw(world, camera)
        for cow in cows:
            cow.update(dt)
            cow.draw(world, grid, camera)
        world_rect = world.get_rect(bottomleft=(0, screen_height))
        screen.blit(world, world_rect)
        
        # Show on screen
        pygame.display.flip()

        # Update clock
        dt = clock.tick(0) / 1000# limit FPS (0 for unlimited)
        new_fps += 1
        time_since_fps += dt
        if time_since_fps >= 1:
            fps = new_fps
            time_since_fps,new_fps = 0,0
        
if __name__ == "__main__":
    main()