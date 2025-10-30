import pygame
from constants import *
from deque import Deque
from pqueue import Pqueue
from typing import TYPE_CHECKING
from pieces import Piece
from pieces import valid

class Pawn(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)

        self.moves = [(1,1),(1,-1),(1,0),(2,0)]

        self.vision =[]

        # Vision of the piece

        for x in range(3):
            for y in range(-2,3):
                if x==y and x==0:
                    continue
                if self.team == 0:
                    self.vision.append((x,y))
                else:
                    self.vision.append((-x,y))
        
        if self.team == 1:
            self.moves = [(-1,1),(-1,-1),(-1,0),(-2,0)]

        self.stamina = 3
        self.level = 0

        # Weights for different situations
        self.value = 5
        self.support = 10
        self.attacked = -15
        self.recomended_x =10
        self.initiative = 5


    def tick(self):

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()

        for x,y in self.moves:
            if valid(pos_x + x, pos_y + y):
                # Weight of position
                cells.add((pos_x + x,pos_y + y), -2*abs(self.recomended_x -pos_x -x)) 

        for x,y in self.vision:
            if valid(pos_x + x, pos_y + y):
                piece = self.grid.get(pos_x + x ,pos_y + y)
                if piece:
                    for u,v in piece.moves:
                        if valid(pos_x + x + u, pos_y + y +v):
                            if (x+u,y+v) in self.moves:
                                # Weight of incoming attacks or support of other pieces 
                                if piece.team != self.team:
                                    cells.change_priority((x+u,y+v), self.attacked)
                                else:
                                    cells.change_priority((x+u,y+v), piece.support)

        #Delete not possible moves and add weight of possibles attacks or support

        for x,y in self.moves:
            if valid(pos_x + x, pos_y + y):
                piece = self.grid.get((pos_x + x ,pos_y + y ))

                if piece:
                    if self.team == 1:
                        cells.erase((pos_x + x -1,pos_y + y ))
                    else:  
                        cells.erase((pos_x + x + 1,pos_y + y ))

                    if piece.team == self.team:
                        cells.erase((pos_x + x ,pos_y + y )) 

                    else:
                        # Attack in the next move
                        cells.change_priority((pos_x + x ,pos_y + y ), 0, piece.value)
                else:
                    for u,v in self.moves:
                        if valid(pos_x + x + u, pos_y + y + v):
                            if self.grid.get((pos_x + x + u, pos_y + y + v)):
                                cells.change_priority((pos_x + x ,pos_y + y), 0, self.initiative)

        top = cells.top()

        if top == (pos_x, pos_y):
            self.stamina +=1   
        else:
            self.grid.clear()
            self.position = top
            piece = self.grid.get(self.position)
            if piece:
                piece.delete()
            self.grid.set()
        print(self.position)
