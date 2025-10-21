import pygame
from constants import *

class Button:
    def __init__(self, size: tuple[int], position: tuple[int], text: str, function: 'function'):
        self.size = size
        self.position = pygame.Vector2(position)
        self.text = text
        self.function = function

        self.back = pygame.Surface(size)
        font_size = 20
        font = pygame.font.Font(FONT_STYLE, font_size)
        self.text = font.render(self.text, True, BLACK)
        
    
    def click(self, clicked: pygame.Vector2, position: pygame.Vector2):
        if abs(clicked.x - self.position.x) < self.size[0] / 2 and abs(clicked.y - self.position.y) < self.size[1] / 2:
            self.function(position)
            


    def draw(self, container: pygame.Surface, mouse: pygame.Vector2):
        color = COLOR_LIGHT
        if abs(mouse.x - self.position.x) < self.size[0] / 2 and abs(mouse.y - self.position.y) < self.size[1] / 2:
            color = COLOR_DARK

        self.back.fill(color)
        text_rect = self.text.get_rect(center = (self.size[0] / 2, self.size[1] / 2))
        self.back.blit(self.text, text_rect)
        back_rect = self.back.get_rect(center=self.position)
        container.blit(self.back, back_rect)
    