import pygame
from .piece import Piece

class King(Piece):
    
    def __init__(self, position, team = 0):
        super().__init__(position, team)

        self.stamina = 5
        self.max_stamina = 5
        self.range = 1
        self.directions = [(1,0),(1,1),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))
        self.adjacents =[(1,0),(1,1),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        self.adjacents = list(map(pygame.Vector2, self.adjacents))

        # Weights for different situations
        self.value = 10
        self.support = 10
        self.attacked = 0
        self.recomended_x = 10
        self.initiative = 0
        self.restore = 10

    