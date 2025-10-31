import pygame
from constants import *
from structures.deque import Deque 
from structures.pqueue import Pqueue 
import grid

class Piece:
    deque = Deque['Piece'](),Deque['Piece']()
    king = [None, None]
    danger = 0

    def __init__(self, position: tuple[int, int], team: int):
        
        self.deque[team].push_back(self)

        self.position = pygame.Vector2(position)
        self.team = team
        self.selected = False
        self.current_order = "Defend"

        self.captured_value = 0
        self.L1 = lambda:None
        self.L2 = lambda:None

        self.adjacents =[(1,0),(0,1),(-1,0),(0,-1)]
        self.adjacents = list(map(pygame.Vector2, self.adjacents))

        self.level = 0
        
        if team == 0:
            Piece.danger -= self.value
        else:
            Piece.danger += self.value

        grid.set_piece(self)


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
    
    
    def has_piece(
        self, 
        position: pygame.Vector2, 
        vision: list[pygame.Vector2] = None, 
        attack: bool = False
    ):
        if not self.valid(position):
            return False
        if vision and position not in vision:
            return False
        piece = grid.get_piece(position)
        if not piece:
            return False
        if not attack:
            return True
        return piece.team != self.team


    def get_vision(self):
        vision = [self.position]
                
        for direction in self.directions:
            for i in range(1,self.range + 1):
                new_position = self.position + direction * i
                if  self.valid(new_position):
                    
                    if not new_position in vision:
                        vision.append(new_position)

                    if grid.get_piece(new_position):
                        break
                    
                    for adjacent in self.adjacents:
                        if self.valid(new_position + adjacent):
                            if not (new_position + adjacent) in vision:
                                vision.append(new_position + adjacent)
        
        return vision

    
    def get_moves(self, vision: list[pygame.Vector2], attack: bool):
        moves = []
        for direction in self.directions:
            for i in range(1, self.range + 1):
                if  self.valid(self.position + direction * i):
                    if not (self.position + direction * i) in vision:
                        continue
                    piece = grid.get_piece(self.position + direction * i)

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
        
        pos_x = self.position[0]
        pos_y = self.position[1]

        if self.stamina == 0:
            self.stamina +=1
            grid.set_piece(self)
            return

        cells = Pqueue()

        for x,y in moves:
                # Weight of position
                cells.add((x, y),0) 

                if self.team == 0 and pos_x <= self.recomended_x:
                    cells.change_priority((x,y), 10 * abs((x - pos_x)) + abs(y -pos_y)) 
                elif self.team == 1 and pos_x >= self.recomended_x:
                    cells.change_priority((x,y), 10 * abs((x - pos_x)) + abs(y -pos_y)) 
                else:
                    cells.change_priority((x,y), 5 * abs((x - pos_x)) + abs(y -pos_y)) 


        for x,y in vision:
            piece = grid.get_piece((x ,y))
            if piece:
                for u,v in piece.get_moves(vision,0):
                    if (u,v) in moves:
                        # Weight of incoming attacks or support of other pieces 
                        if piece.team != self.team:
                            cells.change_priority((u,v), self.attacked)
                        else:
                            cells.change_priority((u,v), self.support)

        #Weight of possibles attacks or support

        for x,y in moves:

            piece = grid.get_piece((x,y))

            #Direct attack pieces
            if piece:
                cells.change_priority((x,y), 2 * piece.value + 5)
                    
            self.position = pygame.Vector2(x,y)
            moves2 = self.get_moves(vision, attack = False)

            for u,v in moves2:
                if (u,v) == (x,y):
                    continue
                if (u,v):
                    piece = grid.get_piece((u, v))
                    if piece:
                        cells.change_priority((x ,y), self.initiative)


        self.position = pygame.Vector2(pos_x, pos_y)

        if self.stamina <= self.max_stamina// 2 :
            cells.change_priority((pos_x ,pos_y), self.restore)


        top = cells.top()


        if top == (pos_x, pos_y):
            if self.stamina < self.max_stamina:
                self.stamina +=1 
            grid.set_piece(self)
              
        else:
            self.stamina -= 1
            grid.clear(self)
            self.position = pygame.Vector2(top)
            piece = grid.get_piece(self.position)
            
            if piece:
                Piece.king[not piece.team].low_piece_value += 1
                if self.value != 4:
                    Piece.king[not piece.team].high_piece_value += 1
                if self.value == 15:
                    Piece.king[not piece.team].high_piece_value += 1

                if piece.team == 0:
                    Piece.danger += piece.value
                else:
                    Piece.danger -= piece.value

                self.captured_value += piece.value

                # if captured enough, level up and call it's upgrades
                if self.captured_value // self.value > self.level:
                    self.level += 1
                    if self.level == 1:
                        self.L1()
                    if self.level == 2:
                        self.L2()
                    

                piece.delete()
            grid.set_piece(self)
                           
            self.attempt_promotion()


    def attempt_promotion(self):
        pass

def main():
    from bishop import Bishop
    prueba = Bishop(0,0,1)
    print(prueba.get_moves())

if __name__ == "main":
    main()

    
# Para cada casilla:
# 1. - Cantidad de piezas que la atacan
# 2. + Cantidad de piezas que la protegen (atacan pero son del mismo bando)
# 3. + Piezas potenciales a las que puedes atacar si te mueves ahi 
# 4. - Cordenada en x
# 5. + Piezas potenciales a las que puedes proteger si te mueves ahi 
# 6. casilla inicial += f(stamina)
# Futuro: 
# 7. Recursos
