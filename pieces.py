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

    def __init__(self, position: tuple[int, int], team: int = 0):
        self.pieces_deque.push_back(self)
        self.grid.set(position, self)

        self.position = position
        self.team = team
        self.piece_color = BLACK if team else WHITE
        self.draw()


    def draw(self):
        piece_offset = self.offset + pygame.Vector2(self.square_size) / 2
        position = pygame.Vector2(self.position) * self.square_size + piece_offset
        
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        piece_name = type(self).__name__
        text = font.render(piece_name, True, self.piece_color, GRAY)
        text_rect = text.get_rect(center = (55 / 2, 20 / 2))
        
        back = pygame.Surface((55,20))
        back.fill(GRAY)
        back.blit(text, text_rect)
        back_rect = back.get_rect(center = position)
        self.screen.blit(back, back_rect)


    def undraw(self):
        color = BLACK if sum(self.position) % 2 else WHITE
        position = self.position * self.square_size + self.offset
        draw_position = (*position, self.square_size, self.square_size)
        pygame.draw.rect(self.screen, color, draw_position)


    def delete(self):
        # self.pieces_deque.delete(self)
        self.grid.set(self.position, None)
        self.grid.clear(self.position)


    def tick(self):
        pass

class Pawn(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = [(1,0),(2,0),(1,1),(1,-1)]
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
            if pos_x + x >= 0 and pos_x + x <=16 :
                for y in range(-2,3):
                    if pos_y + y <= 12 and pos_y + y>= 0:
                        cells.add(0,(pos_x + x , pos_y + y))
        
        for x in range(3):
            if pos_x + x >= 0 and pos_x + x <=16 :
                for y in range(-2,3):
                    if pos_y + y <= 12 and pos_y + y >= 0:
                        piece = self.grid.get((pos_x + x ,pos_y + y ))
                        if piece:
                            for u,v in piece.moves:
                                cells.change_priority((pos_x + x + u,pos_y + y +v), 0, -15)
        
        for x,y in self.moves:
            if pos_x + x >=0 and pos_x + x <= 16 and pos_y + y >=0 and pos_y + y <= 12:
                piece = self.grid.get((pos_x + x ,pos_y + y ))

                if piece and abs(y)==1:
                    cells.change_priority((pos_x + x ,pos_y + y ), 0, 25)
                elif piece:
                    cells.erase((pos_x + x ,pos_y + y ))
                else:
                    if pos_x + x +1 <= 16 and pos_y + y +1 <=12:
                        if self.grid.get((pos_x + x ,pos_y + y +1)):
                            cells.change_priority((pos_x + x ,pos_y + y ), 0, 10)

                        if pos_y + y -1 >=0:   
                            if self.grid.get((pos_x + x ,pos_y + y -1)):
                                cells.change_priority((pos_x + x ,pos_y + y ), 0, 10)
        
        if self.stamina <=1:
            cells.change_priority((pos_x,pos_y),0,12)

        for x in range(3):
            if pos_x + x >= 0 and pos_x + x <=16 :
                for y in range(-2,3):
                    if (x,y) not in self.moves:
                        cells.erase((x,y))

        top = cells.top()   

        if top == (pos_x, pos_y):
            self.stamina +=1   
        else:
            self.position = top  
            piece = self.grid.get(self.position)
            if piece:
                piece.delete()

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

class Bishop(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        
        for i in range(-3,4):
            for j in range(-3,4):
                if abs(i)==abs(j) and i!=0:
                    self.moves.append((i,j))

        self.stamina = 4
        self.level = 0

class Rook(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        for i in range(-3,4):
            if i!=0:
                self.moves.append((0,i))
                self.moves.append((i,0))

        self.stamina = 5
        self.level = 0


class Queen(Piece):
    def __init__(self, position, team = 0):
        super().__init__(position, team)
        self.moves = []
        for i in range(-3,4):
            if i!=0:
                self.moves.append((0,i))
                self.moves.append((i,0))
        
        for i in range(-3,4):
            for j in range(-3,4):
                if abs(i)==abs(j) and i!=0:
                    self.moves.append((i,j))

        self.stamina = 6
        self.level = 0


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


pieces_dict: dict[str, type[Piece]] = dict()
for piece in Piece.__subclasses__():
    pieces_dict[piece.__name__.lower()] = piece
