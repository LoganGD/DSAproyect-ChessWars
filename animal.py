import pygame
from constants import *

class Animal():
    def __init__(self):
        pass

class Cow(Animal):
    def __init__(self, pos_x, pos_y):
        self.position = pygame.Vector2(pos_x, pos_y)
    
    def draw(self, world: pygame.Surface, camera: pygame.Vector3):
        pos_x = ( self.position.x - camera.x + 1/2) * camera.z
        pos_y = ( self.position.y - camera.y + 1/2) * camera.z

        font_size = round(camera.z)
        font = pygame.font.Font(None, font_size) # None for default
        self.text = font.render("cow", True, BLACK, WHITE)
        text_rect = self.text.get_rect(center=(pos_x, pos_y))
        world.blit(self.text, text_rect)
