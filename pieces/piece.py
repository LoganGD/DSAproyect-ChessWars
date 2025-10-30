import pygame
from constants import *


class Piece:
    deque = [],[]

    def __init__(self, position: tuple[int, int], team: int):
        self.deque[team].append(self)
        self.position = position
        self.team = team

    def tick(self):
        print(self.team, self.__class__)