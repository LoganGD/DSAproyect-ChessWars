import pygame
from constants import *


class Piece:
    deque = [],[]

    def __init__(self, position: tuple[int, int], team: int):
        self.deque[team].append(self)
        self.position = position
        self.team = team
        self.selected = False
        self.mood = "Empty thoughts"

    def tick(self):
        name = self.__class__.__name__
        print(name, self.team, self.mood)