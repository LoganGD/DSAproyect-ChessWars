import pygame
import gui
import grid
from constants import *
from pieces import *

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
        grid.update(dt, clicked, action)
        gui.output(Piece.king[0])


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


if __name__ == "__main__":
    main()
