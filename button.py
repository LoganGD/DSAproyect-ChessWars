import pygame
from constants import *

class Button:
    def __init__(self, text: str, width: int, height: int, pos_x = 0, pos_y = 0):
        self.position = pygame.Vector2(pos_x, pos_y)
        self.width = width
        self.height = height
        self.text = text

    def click(self, mouse: tuple):
        if abs(mouse[0] - self.position.x) < self.width / 2 and abs(mouse[1] - self.position.y) < self.height / 2:
            print(self.text)

    def set_pos(self, pos_x: float, pos_y: float):
        self.position = pygame.Vector2(pos_x, pos_y)
    
    def get_width(self):
        return self.width

    def draw(self, surface: pygame.Surface, mouse: tuple):
        color = COLOR_LIGHT
        if abs(mouse[0] - self.position.x) < self.width / 2 and abs(mouse[1] - self.position.y) < self.height / 2:
            color = COLOR_DARK

        font_size = 20
        font = pygame.font.Font(TEXT_FONT, font_size)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center = (self.width / 2, self.height / 2))
        
        back = pygame.Surface((self.width, self.height))
        back.fill(color)
        back.blit(text, text_rect)
        back_rect = back.get_rect(center=self.position)
        
        surface.blit(back, back_rect)