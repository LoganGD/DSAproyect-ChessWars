import pygame
from .piece import Piece
from constants import *

class King(Piece):
    
    def __init__(self, position, team = 0):
        self.stamina = 5
        self.max_stamina = 5
        self.range = 1
        
        super().__init__(position, team)

        self.directions = [(1,0),(1,1),(1,-1),(0,1),
                           (0,-1),(-1,1),(-1,0),(-1,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))
        self.adjacents =[(1,0),(1,1),(1,-1),(0,1),
                         (0,-1),(-1,1),(-1,0),(-1,-1)]
        self.adjacents = list(map(pygame.Vector2, self.adjacents))

        # Weights for different situations
        self.value = 1000
        self.support = 5
        self.attacked = -1000
        self.recomended_x = (0 if self.team == 0 else GRID_WIDTH - 0)
        self.initiative = 0
        self.restore = 10

    def tick(self):
        # enemy team AI
        if self.team == 1:
            pass

        super().tick()