import pygame
from constants import *
from typing import Callable

class Button:

    buttons_list: list['Button']

    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, button_text: str, function: Callable):
        self.surface = surface
        self.rect = rect
        self.text = button_text
        self.function = function
        self.color = None

        self.buttons_list.append(self)

        # preparing base rect
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        position = self.rect.w / 2, self.rect.h / 2
        text = font.render(button_text, True, BLACK)
        text_rect = text.get_rect(center = position)
        
        self.back_light = pygame.Surface(self.rect.size)
        self.back_light.fill(COLOR_LIGHT)
        self.back_light.blit(text, text_rect)

        self.back_dark = pygame.Surface(self.rect.size)
        self.back_dark.fill(COLOR_DARK)
        self.back_dark.blit(text, text_rect)

    def click(self, mouse: pygame.Vector2):
        x = mouse[0] - self.rect.x
        y = mouse[1] - self.rect.y

        if 0 <= x and x < self.rect.width and 0 <= y and y < self.rect.height:
            print(self.text)
            self.function()

    def draw(self, mouse: pygame.Vector2):
        x = mouse[0] - self.rect.x
        y = mouse[1] - self.rect.y

        if 0 <= x and x < self.rect.width and 0 <= y and y < self.rect.height:
            if self.color == COLOR_DARK:
                return
            self.color = COLOR_DARK
            self.surface.blit(self.back_dark, self.rect)
        else:
            if self.color == COLOR_LIGHT:
                return
            self.color = COLOR_LIGHT
            self.surface.blit(self.back_light, self.rect)
