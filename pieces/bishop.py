from .piece import Piece
from constants import *

class Bishop(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
                 
        self.stamina = 4
        self.max_stamina = 4
        self.level = 0
        self.range = 3

        # Weights for different situations
        self.value = 6 
        self.support = 0
        self.attacked = 0
        self.recomended_x = 0
        self.initiative = 0

    def get_moves_and_vision(self):
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

        moves = [self.position]
        vision =[]
        

        pos_x = self.position[0]
        pos_y = self.position[1]

        #Moves of the piece

        for x , y in directions:
            for i in range(1,self.range + 1):
                if  self.valid(pos_x + x * i, pos_y + y * i):
                    piece = self.grid.get(pos_x + x, pos_y + y)
                    if not piece or piece.team != self.team:
                        moves.append((pos_x + x, pos_y + y))

        # Vision of the piece

        for x,y in moves:
            if self.grid.get(x,y):
                continue

            for i in range(-1,2):
                if not (x + i, y) in self.vision and abs(x + i - pos_x) <= self.range:
                    vision.append((x + i, y))
                
                if not (x, y + i) in self.vision and abs(y + i - pos_y) <= self.range:
                    vision.append((x, y + i))

        return moves, vision