import pygame
from constants import *
from button import *

class Menu:
    def __init__(self, size: tuple[int], buttons_settings: list[tuple[str, 'function']]):
        self.size = size
        self.back = pygame.Surface(self.size)
        self.lenght = len(buttons_settings) 
        self.buttons = []

        
        offset = 5
        for [text, function] in buttons_settings:
            button_size = (self.size[0] - 10, ( self.size[1] - 5 ) // self.lenght - 5)
            button_position = (self.size[0] // 2, offset + button_size[1] // 2)
            button = Button(button_size, button_position, text, function)
            offset +=  button_size[1] + 5
            self.buttons.append(button)
 

    def draw(self, container: pygame.Surface, position: pygame.Vector2, mouse: pygame.Vector2):
        if position.x < 0:
            return

        self.back.fill(BEIGE)
        for button in self.buttons:
            button.draw(self.back, mouse - position)
        
        if position[0] + self.size[0] <= container.get_width():
            if position[1] + self.size[1] <= container.get_height():
                back_rect = self.back.get_rect(topleft = position)
            else:
                back_rect = self.back.get_rect(bottomleft = position)
        else:
            if position[1] + self.size[1] <= container.get_height():
                back_rect = self.back.get_rect(topright = position)
            else:
                back_rect = self.back.get_rect(bottomright = position)

        container.blit(self.back, back_rect)
        

    def click(self, position: pygame.Vector2, mouse: pygame.Vector2):
        
        for button in self.buttons:
            button.click(mouse - position, position)