import pygame
from .piece import Piece
from constants import *

class Queen(Piece):
    
    def __init__(self, position, team = 0):
        super().__init__(position, team)
                 
        self.stamina = 8
        self.max_stamina = 8
        self.range = 3
        self.directions = [(1,0),(0,1),(-1,0),(0,-1),
                           (1,1),(-1,1),(-1,-1),(1,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))

        # Weights for different situations
        self.value = 15
        self.support = 5
        self.attacked = -20
        self.recomended_x = ( 7 if self.team == 0 else GRID_WIDTH - 7)
        self.initiative = 5
        self.restore = 5

    