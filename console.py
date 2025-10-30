import pygame
from constants import *
from pieces.pieces import *
from events import create_default

class Console:
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect):
        self.surface = surface
        self.rect = rect
        self.input = ""
        self.output = ""
    
        self.back = pygame.Surface(rect.size)
        self.back.fill(BLACK)
    
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

        if len(cmds) >= 4:
            if (cmds[0] == "create"
                and cmds[1] in pieces_dict
                and cmds[2].isdigit()
                and cmds[3].isdigit()
                and int(cmds[2]) < GRID_WIDTH
                and int(cmds[3]) < GRID_HEIGHT
            ):
                position = int(cmds[2]), int(cmds[3])
                is_enemy = int(len(cmds) > 4 and cmds[4] == "black")
                pieces_dict[cmds[1]](position, is_enemy)
                if is_enemy:
                    self.output = "black " + cmds[1]
                else:
                    self.output = "white " + cmds[1]
                self.output += " created in " + cmds[2] + " " + cmds[3]

            if (cmds[0] == "event"
                and cmds[1] == "create"
                and cmds[2] == "default"
                and cmds[3] in ("0","1")
            ):
                create_default(int(cmds[3]))
                self.output = "default placement created"
        
        if len(cmds) > 0 and cmds[0] == "nuke":
            if len(cmds) > 1 and cmds[1] == "2":
                raise Exception("NUKE")
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
        self.surface.blit(self.back, self.rect)
        
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        offset = pygame.Vector2(self.rect.topleft)

        line = font.render(self.input, True, WHITE) # input
        self.surface.blit(line, offset + (5,5))

        line = font.render(self.output, True, WHITE) # output
        self.surface.blit(line, offset + (5,25))
