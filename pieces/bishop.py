import pygame
from constants import *
from .piece import Piece

class Bishop(Piece):

    def __init__(self, position, team = 0):
        self.value = 6 
        self.stamina = 4
        self.max_stamina = 4
        self.range = 3

        super().__init__(position, team)

        self.captured_value = 0
        def L1():
            self.max_stamina += 1
        self.L1 = L1
        def L2():
            self.range += 1
        self.L2 = L2

        self.directions = [(1,1),(-1,1),(-1,-1),(1,-1)]
        self.directions = list(map(pygame.Vector2, self.directions))

        # Weights for different situations
        self.support = 5
        self.attacked = -15
        self.recomended_x = (12 if self.team == 0 else GRID_WIDTH - 12)
        self.initiative = 15
        self.restore = 10
