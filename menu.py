import pygame
from constants import *
from button import *

class Menu:
    def __init__(self, size: tuple[int], functions: list):
        self.size = size
        self.back = pygame.Surface(self.size)
        self.lenght = len(functions) 
        self.bottons = []

        offset=0
        for function in functions:
            size_botton = [self.size[0]//self.lenght ,self.size[1]]
            botton = Button(size_botton, [offset + (size_botton[0]//2),self.size//2], function)
            offset +=  size_botton[0]
            self.bottons.insert(botton)
 

    def draw(self, container: pygame.Surface, position: tuple[int], mouse):
        
        for botton in self.bottons:
            botton.draw(self.back, mouse)
        
        back_rect = self.back.get_rect(topleft = position)
        container.blit(self.back,back_rect)


    def click(self, mouse: tuple[int]):
        
        for botton in self.bottons:
            botton.click(mouse)
        

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
        

        

        
        
       