import pygame
from constants import *
from .piece import Piece

class Rook(Piece):
    def __init__(self, position, team = 0):
        self.stamina = 5
        self.max_stamina = 5
        self.range = 3

        super().__init__(position, team)
                 
        self.captured_value = 0
        def L1():
            self.max_stamina += 1
        self.L1 = L1
        def L2():
            self.range += 1
        self.L2 = L2

        self.directions = [(1,0),(0,1),(-1,0),(0,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))

        # Weights for different situations
        self.value = 10
        self.support = 8
        self.attacked = -15
        self.recomended_x = ( 8 if self.team == 0 else GRID_WIDTH - 8)
        self.initiative = 5
        self.restore = 10

    