from pieces import Piece
from constants import *

class Pawn(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)

        self.moves = [(1,1),(1,-1),(1,0),(2,0)]
        if self.team == 1:
            self.moves = [(-1,1),(-1,-1),(-1,0),(-2,0)]

        self.stamina = 3
        self.level = 0

    def tick(self):

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()
        
        for x in range(3):
            if pos_x + x >= 0 and pos_x + x < GRID_WIDTH :
                for y in range(-2,3):
                    if pos_y + y <= GRID_HEIGHT and pos_y + y>= 0:
                        cells.add(reward(self,self.team, pos_x + x),(pos_x + x , pos_y + y))
        
        for x in range(3):
            if pos_x + x >= 0 and pos_x + x < GRID_WIDTH :
                for y in range(-2,3):
                    if pos_y + y <= GRID_HEIGHT and pos_y + y >= 0:
                        piece = self.grid.get((pos_x + x ,pos_y + y ))
                        if piece:
                            for u,v in piece.moves:
                                if piece.team != self.team:
                                    cells.change_priority((pos_x + x + u,pos_y + y +v), 0, -15)
                                else:
                                    cells.change_priority((pos_x + x + u,pos_y + y +v), 0, 15)

        
        for x,y in self.moves:
            if pos_x + x >=0 and pos_x + x <=  GRID_WIDTH and pos_y + y >=0 and pos_y + y <= GRID_HEIGHT:
                piece = self.grid.get((pos_x + x ,pos_y + y ))

                if piece.team == self.team:
                    cells.erase((pos_x + x ,pos_y + y ))
                    if y==0:
                        cells.erase((pos_x + x +1 ,pos_y + y ))

                if piece and abs(y)==1:
                    cells.change_priority((pos_x + x ,pos_y + y ), 0, 25)

                elif piece:
                    cells.erase((pos_x + x ,pos_y + y ))
                    if y==0:
                        cells.erase((pos_x + x +1 ,pos_y + y ))

                else:
                    for u,v in self.moves:
                        if abs(v) == 1:
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
            self.undraw()
            self.position = top
            piece = self.grid.get(self.position)
            if piece:
                piece.delete()
            self.draw()
        print(self.position)
