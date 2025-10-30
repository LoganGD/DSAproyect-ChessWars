import pygame
import gui
import grid
from constants import *
import random
import event

def main():
    pygame.init()
    pygame.display.set_caption("Chess 2") # window title

    # game clock, limits fps
    clock = pygame.time.Clock()

    # starting global objects
    gui.init()
    grid.init(gui.screen, gui.square_size, gui.offset)

    # debug flag
    debug_mode = False
    current_time,dt = 0,0
    fps,prev_fps = 0,0

    while True:
        # reading inputs
        clicked, action, keyboard, exit = gui.input()

        # if exit close the game
        if exit:
            pygame.quit()
            return
        
        # if code matches turn on debug flag
        if keyboard == DEBUG_CODE:
            debug_mode = True


        # updates main game and GUI
        changes = grid.update(current_time, clicked, action)        
        gui.update()


        # # random events
        # for _ in range(dt * grid.turn_speed):
        #     if random.random() < 0.001:
        #         event.random_event()


        # debugging things
        if debug_mode:
            if abs(fps - prev_fps) > 2:
                prev_fps = round(fps)

                font = pygame.font.Font(FONT_STYLE, FONT_SIZE)

                fps_text = "FPS: " + str(round(fps))
                text = font.render(fps_text, True, WHITE, GRAY)
                text_rect = text.get_rect(
                    topright = (gui.screen.get_width(), 0))
                gui.screen.blit(text, text_rect)

        # limit FPS (0 for unlimited)
        dt = clock.tick(0)
        fps += (clock.get_fps() - fps) * dt / 1000
        current_time += dt / 1000


if __name__ == "__main__":
    main()
