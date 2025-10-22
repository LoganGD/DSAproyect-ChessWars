import pygame
from constants import *
from pieces import *

class Console:
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2):
        self.screen = screen
        self.console = pygame.Surface(position)
        self.input = ""
        self.output = ""
        
    def process_key(self, key: int, unicode: str):
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            words = self.input.split(" ")
            self.output = ""
            if len(words) > 3 and words[0] == "create" and words[1] in pieces_dict and words[2].isdigit() and words[3].isdigit():
                if int(words[2]) < GRID_WIDTH and int(words[3]) < GRID_HEIGHT:
                    position = int(words[2]), int(words[3])
                    is_enemy = len(words) > 4 and words[4] == "enemy"
                    pieces_dict[words[1]](position, is_enemy)
                    if is_enemy:
                        self.output = "enemy "
                    self.output += words[1] + " created in " + words[2] + " " + words[3]
                else:
                    self.output = words[1] + " created, but it fell from the board"

            if len(words) > 0 and words[0] == "nuke":
                while len(piece.pieces_deque) > 0:
                    piece.pieces_deque.front().clear()
                    piece.pieces_deque.pop_front()
                self.output = "nuked"

            if self.output == "":
                self.output = "huh?"
            self.input = ""
        elif key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
        else:
            self.input += unicode.lower()
    
    def show_fps(self, fps: float):
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        text = font.render("FPS: " + str(int(fps)), True, WHITE, GRAY)
        text_rect = text.get_rect(topright = (self.screen.get_width(), 0))
        self.screen.blit(text, text_rect)
    
    def draw(self):
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        self.console.fill(BLACK)
        line = font.render(self.input, True, WHITE)
        self.console.blit(line,(5,5))
        line = font.render(self.output, True, WHITE)
        self.console.blit(line,(5,25))
        console_rect = self.console.get_rect(bottomleft = (5, self.screen.get_height() - 5))
        self.screen.blit(self.console, console_rect)