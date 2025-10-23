import pygame
from constants import *
from pieces import *

class Console:
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect):
        self.surface = surface
        self.rect = rect
        self.input = ""
        self.output = ""
    
    
    def process_key(self, key: int, unicode: str):
        if key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
            return
        
        if key not in [pygame.K_RETURN,pygame.K_KP_ENTER]:
            self.input += unicode
            return
        
        # enter key pressed, processing input
        cmds = self.input.split(" ")

        self.input = ""
        self.output = ""

        if len(cmds) >= 3:
            if cmds[0] == "create" and cmds[1] in pieces_dict and cmds[2].isdigit() and cmds[3].isdigit():
                if int(cmds[2]) < GRID_WIDTH and int(cmds[3]) < GRID_HEIGHT:
                    position = int(cmds[2]), int(cmds[3])
                    is_enemy = int(len(cmds) > 4 and cmds[4] == "enemy")
                    pieces_dict[cmds[1]](position, is_enemy)
                    if is_enemy:
                        self.output = "enemy "
                    self.output += cmds[1] + " created in " + cmds[2] + " " + cmds[3]
                else:
                    self.output = cmds[1] + " created, but it fell from the board"
        
        if len(cmds) > 0 and cmds[0] == "nuke":
            while len(piece.pieces_deque) > 0:
                piece.pieces_deque.front().undraw()
                piece.pieces_deque.pop_front()
            self.output = "nuked"
        
        if self.output == "":
            self.output = "invalid command"


    def show_fps(self, fps: float):
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        text = font.render("FPS: " + str(int(fps)), True, WHITE, GRAY)
        text_rect = text.get_rect(topright = (self.surface.get_width(), 0))
        self.surface.blit(text, text_rect)
    

    def draw(self):
        pygame.draw.rect(self.surface, BLACK, self.rect) # fill black
        
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        offset = pygame.Vector2(self.rect.topleft)

        line = font.render(self.input, True, WHITE) # input
        self.surface.blit(line, offset + (5,5))

        line = font.render(self.output, True, WHITE) # output
        self.surface.blit(line, offset + (5,25))
