import pygame
from constants import *

class Button:
    def __init__(self, size: tuple[int], position: tuple[int], function):
        self.width = size[0]
        self.height = size[1]
        self.position = pygame.Vector2(position)
        self.function = function
        self.back = pygame.Surface(size)
    
    def click(self, mouse: tuple[int]):
        if abs(mouse[0] - self.position[0]) < self.width / 2 and abs(mouse[1] - self.position[1]) < self.height / 2:
            print(self.text)

    def draw(self, container: pygame.Surface, mouse: tuple[int]):
        color = COLOR_LIGHT
        if abs(mouse[0] - self.position.x) < self.width / 2 and abs(mouse[1] - self.position.y) < self.height / 2:
            color = COLOR_DARK

        self.back.fill(color)
        back_rect = self.back.get_rect(center = self.position)
        
        container.blit(self.back,back_rect)
    