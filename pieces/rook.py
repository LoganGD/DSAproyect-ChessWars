from .piece import Piece
from constants import *

class Rook(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
                 
        self.stamina = 5
        self.max_stamina = 5
        self.level = 0
        self.range = 3
        self.directions = [(1,0),(0,1),(-1,0),(0,-1)]

        # Weights for different situations
        self.value = 10
        self.support = 0
        self.attacked = 0
        self.recomended_x = 0
        self.initiative = 0
    
    def get_vision(self):
        
        vision =[]

        pos_x = self.position[0]
        pos_y = self.position[1]

        for x , y in self.directions:
            for i in range(1,self.range + 1):
                if  self.valid(pos_x + x * i, pos_y + y * i):
                    
                    vision.append((pos_x + x * i, pos_y + y))
                    piece = self.grid.get(pos_x + x * i, pos_y + y * i)

                    if piece:
                        break
                    elif x != 0:
                        if not (pos_x + x * i, pos_y + 1) in vision:
                            vision.append((pos_x + x * i, pos_y + 1))
                        if not (pos_x + x * i, pos_y - 1) in vision:
                            vision.append((pos_x + x * i, pos_y - 1))
                    else:
                        if not (pos_x + 1, pos_y + y * i) in vision:
                            vision.append((pos_x + 1, pos_y + y * i))
                        if not (pos_x - 1, pos_y + y * i) in vision:
                            vision.append((pos_x - 1, pos_y + y * i))
        
        return vision
                    
    def get_moves(self, vision, defend):
        moves = []
        pos_x = self.position[0]
        pos_y = self.position[1]
        for x , y in self.directions:
            for i in range(1, self.range + 1):
                if  self.valid(pos_x + x * i, pos_y + y * i):
                    if not (pos_x + x * i, pos_y + y * i) in vision:
                        continue
                    piece = self.grid.get((pos_x + x * i, pos_y + y * i))

                    if not piece:
                        moves.append((pos_x + x * i, pos_y + y * i))
                        continue

                    if (piece.team == self.team) == defend:
                        break
                    else 
    



    def get_moves_and_vision(self):
        pass