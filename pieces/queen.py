import pygame
from .piece import Piece

class Queen(Piece):
    
    def __init__(self, position, team = 0):
        super().__init__(position, team)
                 
        self.stamina = 8
        self.max_stamina = 8
        self.range = 3
        self.directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))

        # Weights for different situations
        self.value = 15
        self.support = 0
        self.attacked = 0
        self.recomended_x = 0
        self.initiative = 0
        self.restore = 0

    