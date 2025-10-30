import pygame
from .piece import Piece

class Knight(Piece):
 
    def __init__(self, position, team = 0):
        super().__init__(position, team)

        self.stamina = 4
        self.max_stamina = 4
        self.range = 1
        self.directions = [(1,2),(-1,2),(1,-2),(-1,-2),
                           (2,1),(2,-1),(-2,1),(-2,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))

        # Weights for different situations
        self.value = 6
        self.support = 0
        self.attacked = 0
        self.recomended_x = 0
        self.initiative = 0
    