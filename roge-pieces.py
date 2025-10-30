import pygame
from constants import *
from deque import Deque
from pqueue import Pqueue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grid import Grid

class Piece:
    screen: pygame.Surface
    grid: 'Grid'
    pieces_deque: Deque['Piece']
    square_size: int
    offset: pygame.Vector2

    moves: list[tuple[int, int]]

    def __init__(self, position: tuple[int, int], team: int = 0):
        self.pieces_deque.push_back(self)
        self.grid.set(position, self)

        self.position = position
        self.team = team
        self.piece_color = BLACK if team else WHITE
        
        # preparing base rect
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        piece_name = type(self).__name__
        text = font.render(piece_name, True, self.piece_color, GRAY)
        text_rect = text.get_rect(center = (55 / 2, 20 / 2))
        
        self.back = pygame.Surface((55,20))
        self.back.fill(GRAY)
        self.back.blit(text, text_rect)

        # first draw

        self.draw()


    def draw(self):
        piece_offset = self.offset + pygame.Vector2(self.square_size) / 2
        position = pygame.Vector2(self.position) * self.square_size + piece_offset
        
        back_rect = self.back.get_rect(center = position)
        self.screen.blit(self.back, back_rect)


    def undraw(self):
        self.grid.clear(self.position)


    def delete(self):
        self.grid.clear(self.position)

    def tick(self):
        pass

def valid(move_x, move_y):
    if move_x < 0 or move_x >= GRID_WIDTH:
        return False
    if move_y < 0 or move_y >= GRID_HEIGHT:
        return False
    return True


class Knight(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
    
        for i in range(-2,3):
            for j in range(-2,3):
                if abs(i)+abs(j)==3:
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
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x , pos_y + y):
                        if (abs(x) <= 2 and abs(y) <=2) or abs(x) == 1 or abs(y) == 1:
                            cells.add(reward(self,self.team, pos_x + x),(pos_x + x , pos_y + y))
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x, pos_y + y):
                        if (abs(x) <= 2 and abs(y) <=2) or abs(x) == 1 or abs(y) == 1:
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

class Bishop(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        self.paths =[[],[],[],[]]
        
        for i in range(-3,4):
            for j in range(-3,4):
                if abs(i)==abs(j) and i!=0:
                    self.moves.append((i,j))

        for i in range(4):
            self.paths[0].append((i,i))
            self.paths[1].append((i,-i))
            self.paths[2].append((-i,i))
            self.paths[3].append((-i,-i))

        self.stamina = 4
        self.level = 0
    
    
    def tick(self):

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x, pos_y + y):
                        if abs(abs(x)-abs(y)) <= 1:
                            cells.add(reward(self,self.team, pos_x + x),(pos_x + x , pos_y + y))
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x, pos_y + y):
                        if abs(abs(x)-abs(y)) <= 1:
                            piece = self.grid.get((pos_x + x ,pos_y + y ))
                            if piece:
                                for u,v in piece.moves:
                                    if piece.team != self.team:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, -15)
                                    else:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, 15)
        
        for path in self.paths:
            complete = True
            for x,y in path:
                if not complete:
                    break

                if valid(pos_x + x, pos_y + y):    
                    piece = self.grid.get((pos_x + x ,pos_y + y ))

                    if piece.team == self.team:
                        cells.erase((pos_x + x ,pos_y + y ))
                        complete = False
                        continue
                        

                    elif piece:
                        cells.change_priority((pos_x + x ,pos_y + y ), 0, 25)
                        complete = False
                        continue

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

class Rook(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        self.paths = [[],[],[],[]]

        for i in range(-3,4):
            if i!=0:
                self.moves.append((0,i))
                self.moves.append((i,0))

        
        for i in range(4):
            self.paths[0].append((0,i))
            self.paths[1].append((i,0))
            self.paths[2].append((-i,0))
            self.paths[3].append((0,-i))

        self.stamina = 5
        self.level = 0
    
    
    def tick(self):

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x ,pos_y + y):
                        if min(abs(x),abs(y)) <= 1:
                            cells.add(reward(self,self.team, pos_x + x),(pos_x + x , pos_y + y))
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x ,pos_y + y):
                        if min(abs(x),abs(y)) <= 1:
                            piece = self.grid.get((pos_x + x ,pos_y + y ))
                            if piece:
                                for u,v in piece.moves:
                                    if piece.team != self.team:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, -15)
                                    else:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, 15)
        
        for path in self.paths:
            complete = True
            for x,y in path:
                if not complete:
                    break
                
                if valid(pos_x + x ,pos_y + y):
                    piece = self.grid.get((pos_x + x ,pos_y + y ))

                    if piece.team == self.team:
                        cells.erase((pos_x + x ,pos_y + y ))
                        complete = False
                        continue
                        

                    elif piece:
                        cells.change_priority((pos_x + x ,pos_y + y ), 0, 25)
                        complete = False
                        continue

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

class Queen(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        self.paths = [[] for _ in range(8)]
        
        for i in range(-3,4):
            if i!=0:
                self.moves.append((0,i))
                self.moves.append((i,0))
            
        for i in range(-3,4):
            for j in range(-3,4):
                if abs(i)==abs(j) and i!=0:
                    self.moves.append((i,j))

        for i in range(4):
            self.paths[0].append((0,i))
            self.paths[1].append((i,0))
            self.paths[2].append((-i,0))
            self.paths[3].append((0,-i))

        
        for i in range(4):
            self.paths[4].append((i,i))
            self.paths[5].append((i,-i))
            self.paths[6].append((-i,i))
            self.paths[7].append((-i,-i))
        
        self.stamina = 6
        self.level = 0

    
    def tick(self):

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x ,pos_y + y):
                            cells.add(reward(self,self.team, pos_x + x),(pos_x + x , pos_y + y))
        
        for x in range(-3,4):
                for y in range(-3,4):
                    if valid(pos_x + x ,pos_y + y):
                            piece = self.grid.get((pos_x + x ,pos_y + y ))
                            if piece:
                                for u,v in piece.moves:
                                    if piece.team != self.team:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, -15)
                                    else:
                                        cells.change_priority((pos_x + x + u,pos_y + y +v), 0, 15)
        
        for path in self.paths:
            complete = True
            for x,y in path:
                if not complete:
                    break
                
                if valid(pos_x + x ,pos_y + y):
                    piece = self.grid.get((pos_x + x ,pos_y + y ))

                    if piece.team == self.team:
                        cells.erase((pos_x + x ,pos_y + y ))
                        complete = False
                        continue
                        

                    elif piece:
                        cells.change_priority((pos_x + x ,pos_y + y ), 0, 25)
                        complete = False
                        continue

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


pieces_dict: dict[str, type[Piece]] = dict()
for piece in Piece.__subclasses__():
    pieces_dict[piece.__name__.lower()] = piece
