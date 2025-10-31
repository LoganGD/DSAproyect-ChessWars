import pygame
from constants import *
from .piece import Piece
from structures.deque import Deque
import random

class King(Piece):
    
    def __init__(self, position, team = 0):
        Piece.king[team] = self
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


        # resources
        self.low_piece_value = 0
        self.high_piece_value = 0

        # events for enemy AI
        self.events = Deque[str]()
        self.events.push_back("Retreat")

    def tick(self):
        # enemy team AI

        empty = []

        for adjacent in self.adjacents:
            position = self.position + adjacent
            if self.valid(position) and not self.has_piece(position):
                empty.append(position)

        opts = []
        from .pawn import Pawn
        from .rook import Rook
        from .knight import Knight
        from .bishop import Bishop
        if self.low_piece_value >= 3:
            opts.append(Pawn)
        if self.high_piece_value >= 3:
            opts.append(Rook)
            opts.append(Knight)
            opts.append(Bishop)

        if len(empty) and len(opts):
            piece = random.choice(opts)
            if piece == Pawn:
                self.low_piece_value -= 3
            else:
                self.high_piece_value -= 3

            piece(random.choice(empty), self.team)

        if self.team == 1:
            event = self.events.front()
            self.events.pop_front()

            if event == "Charge":

                for piece in self.deque[self.team]:
                    if random.random() < 0.2:
                        piece.current_order = "Attack"

                self.low_piece_value += 15
                self.high_piece_value += 5

            if event == "Retreat":

                for piece in self.deque[self.team]:
                    piece.current_order = "Defend"

                attacks = random.randint(2,4)
                for _ in range(attacks):
                    cooldown = 2 ** random.randint(4,7)
                    for _ in range(cooldown):
                        self.events.push_back("Wait")
                    self.events.push_back("Charge")
                self.events.push_back("Retreat")



        super().tick()