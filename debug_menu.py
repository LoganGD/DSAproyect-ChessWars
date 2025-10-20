import pygame
from constants import *
from button import *

class Menu:
    def __init__(self , width, height, list_objects: list[Button]):
        self.width = width
        self.height = height
        self.list_objects = list_objects
        self.offset = 0

        self.back = pygame.Surface((self.width, self.height))
        self.back.fill(BEIGE)

        for object in list_objects:
            object.set_pos(0,self.offset)
            self.offset += object.get_width()
    
    def draw(self, world, mouse: tuple):
        for object in self.list_objects:
            object.draw(self.back, mouse)
        
        back_rect = self.back.get_rec(topleft = mouse)

        world.blit(self.back, back_rect)
        

        

        
        
       