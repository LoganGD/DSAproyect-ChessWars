from pieces import Piece
from constants import *


class King(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        for i in range(-1,2):
            for j in range(-1,2):
                if abs(i)+abs(j) > 0:
                    self.moves.append((i,j))
        self.stamina = 4
        self.level = 0
    
    
    def tick(self):

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()
        
        for x in range(-2,3):
                for y in range(-2,3):
                    if valid(pos_x + x , pos_y + y):
                            cells.add(reward(self,self.team, pos_x + x),(pos_x + x , pos_y + y))
        
        for x in range(-2,3):
                for y in range(-2,3):
                    if valid(pos_x + x , pos_y + y):
                            piece = self.grid.get((pos_x + x ,pos_y + y ))
                            if piece:
                                for u,v in piece.moves:
                                    if piece.team != self.team:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, -15)
                                    else:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, 15)
        
        for x,y in self.moves:
            if valid(pos_x + x, pos_y + y):
                piece = self.grid.get((pos_x + x ,pos_y + y ))

                if piece.team == self.team:
                    cells.erase((pos_x + x ,pos_y + y ))

                elif piece:
                    cells.change_priority((pos_x + x ,pos_y + y ), 0, 25)
                else:
                    for u,v in self.moves:
                        if valid(pos_x + x + u, pos_y + y + v):
                            if self.grid.get((pos_x + x + u, pos_y + y + v)):
                                cells.change_priority((pos_x + x + u,pos_y + y + v), 0, 10)

        
        if self.stamina <=1:
            cells.change_priority((pos_x,pos_y),0,13)

        for x in range(3):
                for y in range(-2,3):
                    if (x,y) not in self.moves:
                        cells.erase((pos_x + x,pos_y + y))

        top = cells.top()   

        if top == (pos_x, pos_y):
            self.stamina +=1   
        else:
            self.position = top  
            piece = self.grid.get(self.position)
            if piece:
                piece.delete() 
