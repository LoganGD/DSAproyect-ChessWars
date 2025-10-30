from .piece import Piece
from .piece import valid
from constants import *
from pqueue import Pqueue

class Knight(Piece):
 
    def __init__(self, position, team = 0):
        super().__init__(position, team)

        self.moves = []
        self.vision =[]

        # Vision of the piece

        for x in range(3):
            for y in range(-2,3):
                continue

        self.stamina = 3
        self.level = 0

        # Weights for different situations
        self.value = 0
        self.support = 0
        self.attacked = 0
        self.recomended_x = 0
        self.initiative = 0
    
    def get_moves_and_vision(self):
        moves = []
        vision =[]

        pos_x = self.position[0]
        pos_y = self.position[1]

        #Moves
        
        # Vision of the piece

        for x in range(-3,4):
            for y in range(-3,4):
                if valid(pos_x + x , pos_y + y):
                    if (abs(x) <= 2 and abs(y) <=2) or abs(x) == 1 or abs(y) == 1:
                        vision.append((x,y))
    
        return moves,vision
            