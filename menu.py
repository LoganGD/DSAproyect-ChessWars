import pygame
from constants import *
from button import *

class Menu:
    def __init__(self, size: tuple[int], buttons_settings: list[tuple[str, 'function']]):
        self.size = size
        self.back = pygame.Surface(self.size)
        self.lenght = len(buttons_settings) 
        self.buttons = []
        self.corner_offset = pygame.Vector2(0,0)

        
        offset = 5
        for [text, function] in buttons_settings:
            button_size = (self.size[0] - 10, ( self.size[1] - 5 ) // self.lenght - 5)
            button_position = (self.size[0] // 2, offset + button_size[1] // 2)
            button = Button(button_size, button_position, text, function)
            offset +=  button_size[1] + 5
            self.buttons.append(button)

    def click(self, position: pygame.Vector2, mouse: pygame.Vector2):
        for button in self.buttons:
            button.click(mouse - position, position) 

    def draw(self, container: pygame.Surface, position: pygame.Vector2, mouse: pygame.Vector2):
        if position.x < 0:
            return

        self.back.fill(BEIGE)
        
        if position[0] + self.size[0] <= container.get_width():
            if position[1] + self.size[1] <= container.get_height():
                back_rect = self.back.get_rect(topleft = position)
                self.corner_offset = pygame.Vector2(0,0)
            else:
                back_rect = self.back.get_rect(bottomleft = position)
                self.corner_offset = pygame.Vector2(0,self.size[1])
        else:
            if position[1] + self.size[1] <= container.get_height():
                back_rect = self.back.get_rect(topright = position)
                self.corner_offset = pygame.Vector2(self.size[0],0)
            else:
                back_rect = self.back.get_rect(bottomright = position)
                self.corner_offset = pygame.Vector2(self.size[0],self.size[1])
        
        
        for button in self.buttons:
            button.draw(self.back, mouse - position + self.corner_offset)

        container.blit(self.back, back_rect)