import pygame
from constants import *


class Button:
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, button_text: str):
        self.surface = surface
        self.rect = rect
        self.text = button_text
        self.color = None

        # preparing button sprite
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        position = self.rect.w / 2, self.rect.h / 2
        text = font.render(button_text, True, BLACK)
        text_rect = text.get_rect(center = position)
        
        # light default sprite
        self.back_light = pygame.Surface(self.rect.size)
        self.back_light.fill(COLOR_LIGHT)
        self.back_light.blit(text, text_rect)

        # dark sprite for mouse hovering on button
        self.back_dark = pygame.Surface(self.rect.size)
        self.back_dark.fill(COLOR_DARK)
        self.back_dark.blit(text, text_rect)


    def mouse_in_range(self, mouse: tuple[int, int]):
        x = mouse[0] - self.rect.x
        y = mouse[1] - self.rect.y
        return (0 <= x and x < self.rect.width 
                and 0 <= y and y < self.rect.height)


    def click(self, mouse: tuple[int, int]):
        if self.mouse_in_range(mouse):
            return self.text


    def draw(self, mouse: tuple[int, int]):
        # if mouse in range use a darker tone

        if self.mouse_in_range(mouse):
            if self.color == COLOR_DARK:
                return
            self.color = COLOR_DARK
            self.surface.blit(self.back_dark, self.rect)
        
        else:
            if self.color == COLOR_LIGHT:
                return
            self.color = COLOR_LIGHT
            self.surface.blit(self.back_light, self.rect)
