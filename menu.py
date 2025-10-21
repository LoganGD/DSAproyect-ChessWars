import pygame
from constants import *
from button import *

class Menu:
    def __init__(self, size: tuple[int], functions: list):
        self.size = size
        self.back = pygame.Surface(self.size)
        self.lenght = len(functions) 
        self.buttons = []

        offset = 0
        for function in functions:
            button_size = (self.size[0] // self.lenght - 10, self.size[1] - 10)
            button_position = (offset + (button_size[0] // 2) + 5, self.size[1] // 2 + 5)
            button = Button(button_size, button_position, function)
            offset +=  button_size[0]
            self.buttons.append(button)
 

    def draw(self, container: pygame.Surface, position: tuple[int], mouse):
        self.back.fill(BEIGE)
        for button in self.buttons:
            button.draw(self.back, mouse)
        
        back_rect = self.back.get_rect(topleft = position)
        container.blit(self.back, back_rect)


    def click(self, mouse: tuple[int], clicked: tuple[int]):
        
        for button in self.buttons:
            button.click(clicked)