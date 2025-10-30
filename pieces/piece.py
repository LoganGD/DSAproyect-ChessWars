import pygame
from constants import *
import grid

class Piece:
    deque: tuple[list['Piece'], list['Piece']] = [],[]

    def __init__(self, position: tuple[int, int], team: int):
        self.deque[team].append(self)
        self.position = pygame.Vector2(position)
        self.team = team
        self.selected = False
        self.current_order = "Sleep"

        self.level = 1

        grid.set(self)


    def valid(self, position):
        if position.x < 0 or position.x >= GRID_WIDTH:
            return False
        if position.y < 0 or position.y >= GRID_HEIGHT:
            return False
        return True
    

    def empty(self, position):
        return not self.valid(position) or not grid.get(position)


    def enemy_piece(self, position):
        if not self.valid():
            return False
        piece = grid.get(position)
        if not piece:
            return False
        return piece.team != self.team
    
    
    def any_piece(self, position):
        if not self.valid():
            return True
        return grid.get(position)


    def get_vision(self):
        pass
    def get_moves(self, vision):
        pass


    def tick(self):
        name = self.__class__.__name__
        print(name, self.team, self.current_order)
        # ^^^ debuging ^^^ 

        moves,vision = self.get_moves_and_vision()

        if self.stamina == 0:
            self.stamina +=1
            return

        pos_x = self.position[0]
        pos_y = self.position[1]

        cells = Pqueue()

        for x,y in self.moves:
                # Weight of position
                cells.add((x, y), - 2 * abs(self.recomended_x - x)) 

        for x,y in self.vision:
            piece = self.grid.get(x ,y)
            if piece:
                for u,v in piece.moves:
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

# Para cada casilla:
# 1. - Cantidad de piezas que la atacan
# 2. + Cantidad de piezas que la protegen (atacan pero son del mismo bando)
# 3. + Piezas potenciales a las que puedes atacar si te mueves ahi 
# 4. - Cordenada en x
# Futuro:  
# 5. + Piezas potenciales a las que puedes proteger si te mueves ahi 
# 6. casilla inicial += f(stamina)
# 7. Recursos
# es que justo pense en un caso
# una torre no se quitaria del camino si esta protegiendo al rey
