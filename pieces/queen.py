from .piece import Piece

class Queen(Piece):
    
    def __init__(self, position, team = 0):
        super().__init__(position, team)
                 
        self.stamina = 8
        self.max_stamina = 8
        self.range = 3
        self.directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]

        # Weights for different situations
        self.value = 15
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
                    
                    if not (pos_x + x * i, pos_y) in vision:
                        vision.append((pos_x + x * i, pos_y + y))

                    piece = self.grid.get(pos_x + x * i, pos_y + y * i)

                    if piece:
                        break
                    else:
                        for u,v in self.adjacents:
                            if abs(x * i + u) <= self.range and abs(y * i + v) <= self.range:
                                if not ((x * i + u, y * i + v)) in vision:
                                    vision.append((x * i + u, y * i + v))
        
        return vision
                    
    def get_moves(self, vision, attack):
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

                    if not attack or piece.team != self.team:
                        moves.append((pos_x + x * i, pos_y + y * i))
                    
                    break
        if attack:
            moves.append(self.position)
        
        return moves
