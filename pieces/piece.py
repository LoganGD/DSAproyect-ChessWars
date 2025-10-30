import pygame
from constants import *
from structures.pqueue import Pqueue 
import grid

class Piece:
    deque: tuple[list['Piece'], list['Piece']] = [],[]

    def __init__(self, position: tuple[int, int], team: int):
        self.deque[team].append(self)
        self.position = pygame.Vector2(position)
        self.team = team
        self.selected = False
        self.current_order = "Defend"

        self.adjacents =[(1,0),(0,1),(-1,0),(0,-1)]
        self.adjacents = list(map(pygame.Vector2, self.adjacents))
        self.level = 1

        grid.set(self)


    def valid(self, position):
        x,y = position
        x = round(x)
        y = round(y)
        if x < 0 or x >= GRID_WIDTH:
            return False
        if y < 0 or y >= GRID_HEIGHT:
            return False
        return True
    
    def delete(self):
        self.deque[self.team].remove(self)
    
    
    def has_piece(self, position: pygame.Vector2, vision: list[pygame.Vector2] = None, attack: bool = False):
        if not self.valid(position):
            return False
        if vision and position not in vision:
            return False
        piece = grid.get(position)
        if not piece:
            return False
        if not attack:
            return True
        return piece.team != self.team


    def get_vision(self):
        vision = [self.position]
                
        for direction in self.directions:
            for i in range(1,self.range + 1):
                if  self.valid(self.position + direction * i):
                    
                    if not self.position + direction * i in vision:
                        vision.append(self.position + direction * i)

                    piece = grid.get(self.position + direction * i)

                    if piece:
                        break
                    else:
                        for adjacent in self.adjacents:
                            if self.valid(self.position + direction * i + adjacent):
                                if not (self.position + direction * i + adjacent) in vision:
                                    vision.append(self.position + direction * i + adjacent)
        
        return vision

    
    def get_moves(self, vision, attack):
        moves = []
        for direction in self.directions:
            for i in range(1, self.range + 1):
                if  self.valid(self.position + direction * i):
                    if not (self.position + direction * i) in vision:
                        continue
                    piece = grid.get(self.position + direction * i)

                    if not piece:
                        moves.append(self.position + direction * i)
                        continue

                    if not attack or piece.team != self.team:
                        moves.append(self.position + direction * i)
                    
                    break
        if attack:
            moves.append(self.position)
        
        return moves
    

    def tick(self):
        # name = self.__class__.__name__
        # vision = self.get_vision()
        # moves = self.get_moves(vision, True)

        # print(name, self.team, self.current_order)
        # print(vision)
        # print(moves)
        # # ^^^ debuging ^^^ 

        # return
        vision = self.get_vision()
        moves = self.get_moves(vision, attack = True)

        if self.stamina == 0:
            self.stamina +=1
            return

        cells = Pqueue()

        for x,y in moves:
                # Weight of position
                cells.add((x, y), - 2 * abs(self.recomended_x - x)) 

        for x,y in vision:
            piece = grid.get((x ,y))
            if piece:
                for u,v in piece.get_moves(vision,0):
                    if (u,v) in moves:
                        # Weight of incoming attacks or support of other pieces 
                        if piece.team != self.team:
                            cells.change_priority((u,v), self.attacked)
                        else:
                            cells.change_priority((u,v), self.support)

        #Weight of possibles attacks or support
        
        pos_x = self.position[0]
        pos_y = self.position[1]

        for x,y in moves:

            piece = grid.get((x,y))

            #Direct attack pieces
            if piece:
                cells.change_priority((x,y), piece.value)
                    
            self.position = pygame.Vector2(x,y)
            moves2 = self.get_moves(vision, attack = False)

            for u,v in moves2:
                if (u,v):
                    piece = grid.get((u, v))
                    if piece:
                        cells.change_priority((x ,y), self.initiative)


        self.position = pygame.Vector2(pos_x, pos_y)

        if self.stamina <= self.max_stamina :
            cells.change_priority((pos_x ,pos_y), self.restore)


        top = cells.top()


        if top == (pos_x, pos_y):
            self.stamina +=1 
              
        else:
            grid.clear(self)
            self.position = pygame.Vector2(top)
            piece = grid.get(self.position)
            if piece:
                piece.delete()
            grid.set(self)

# Para cada casilla:
# 1. - Cantidad de piezas que la atacan
# 2. + Cantidad de piezas que la protegen (atacan pero son del mismo bando)
# 3. + Piezas potenciales a las que puedes atacar si te mueves ahi 
# 4. - Cordenada en x
# 5. + Piezas potenciales a las que puedes proteger si te mueves ahi 
# 6. casilla inicial += f(stamina)
# Futuro: 
# 7. Recursos
