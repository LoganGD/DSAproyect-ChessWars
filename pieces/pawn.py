import pygame
from constants import *
from .piece import Piece
from .queen import Queen

class Pawn(Piece):
    def __init__(self, position: tuple[int, int], team: int):
        self.stamina = 3
        self.max_stamina = 3

        super().__init__(position, team)

        self.captured_value = 0
        def L1():
            self.max_stamina += 1
        self.L1 = L1
        def L2():
            self.max_stamina += 1
        self.L2 = L2

        # Weights for different situations
        self.value = 4
        self.support = 2
        self.attacked = -2
        self.recomended_x = (5 if self.team == 0 else GRID_WIDTH - 5)
        self.initiative = 2
        self.restore = 10



    def get_vision(self):
        d = 1 if self.team == 0 else -1 # direction

        vision = [
            self.position + (0,-1),
            self.position + (0,0),
            self.position + (0,1),
            self.position + (d,-1),
            self.position + (d,0),
            self.position + (d,1),
        ]

        new_position = self.position + (d,0)
        if not self.has_piece(new_position):
            new_position = self.position + (d*2,0)
            vision.append(new_position)
            if not self.has_piece(new_position) and self.level == 3:
                vision += [
                    self.position + (d*2,-1),
                    self.position + (d*2,1),
                    self.position + (d*3,-1),
                    self.position + (d*3,0),
                    self.position + (d*3,1),
                ]

        return [position for position in vision if self.valid(position)]


    def get_moves(self, vision: list[pygame.Vector2], attack: bool):
        d = 1 if self.team == 0 else -1 # direction

        moves = [self.position]

        new_position = self.position + (d,-1)
        if self.has_piece(new_position, vision, attack):
            moves.append(new_position)

        new_position = self.position + (d,1)
        if self.has_piece(new_position, vision, attack):
            moves.append(new_position)

        new_position = self.position + (d,0)
        if not self.has_piece(new_position, vision):
            moves.append(new_position)
            
            new_position = self.position + (d*2,0)
            if not self.has_piece(new_position, vision):
                moves.append(new_position)

        return [position for position in moves if self.valid(position)]
        

    def attempt_promotion(self):
        
        if self.position[0] == (GRID_WIDTH - 1 if self.team == 0 else 0):
            Queen(self.position, self.team)
            self.delete()
# Piece
# + LV: capture_value >= self.value
# + LV: Polvo magico (Cocaina)

# Pawn
# Value: 3
# Stamina: 3
# Range: 1 or 2
# Special movement : 2 (requires 3)
# Becomes queen at the opposite edge

# L2: Stamina + 2
# L3: Visibilidad + 1

# V V 3 3
# P V V 3
# V V 3 3

# Rook
# Value: 10
# Stamina: 5
# Range: 3

# L2: Range + 1
# L3: Stamina + 3

# Knight
# Value: 7
# Stamina: 4
# Range: yes

# L2: see adyacents
# L3: stamina + 2

#Bishop
# Value: 6
# Stamina: 4
# Range: 3

# L2: Range + 1
# L3: Stamina + 2

# Queen
# Value: 15
# Stamina: 8
# Range: 3
 
# L2: Range + 2 
# L3: Stamina + 2

# Movement map = Rook + Bishop

# King
# Value: 1e9
# Stamina: 5
# Range: 1

# L2: N/A
# L3: N/A

# V V V V V
# V V V V V
# V V P V V
# V V V V V
# V V V V V