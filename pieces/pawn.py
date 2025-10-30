import grid
from .piece import Piece

class Pawn(Piece):
    def __init__(self, position: tuple[int, int], team: int):
        super().__init__(position, team)

        self.stamina = 3
        self.max_stamina = 3
        def L2():
            self.max_stamina += 2
        self.L2 = L2
        self.L3 = lambda:None

        # Weights for different situations
        self.value = 5
        self.support = 10
        self.attacked = -15
        self.recomended_x =10
        self.initiative = 5


    def get_vision(self):
        d = 1 if self.team == 0 else -1 # direction

        vision = [
            self.position + (0,-1),
            self.position + (0,0),
            self.position + (0,1),
            self.position + (d,-1),
            self.position + (d,0),
            self.position + (d,1),
        ]

        position = self.position + (d,0)
        if not self.any_piece(position):
            position = self.position + (d*2,0)
            vision.append(position)
            if not self.any_piece(position) and self.level == 3:
                vision += [
                    self.position + (d*2,-1),
                    self.position + (d*2,1),
                    self.position + (d*3,-1),
                    self.position + (d*3,0),
                    self.position + (d*3,1),
                ]

        return [position for position in vision if self.valid(position)]


    def get_moves(self, vision: list[tuple[int, int]], defend: bool):
        pass


        if self.enemy(position):
            moves.append(position)
        
        position = self.position + (d,-1)
        if self.enemy(position):
            moves.append(position)
        
        position = self.position + (d,-1)
        if self.enemy(position):
            moves.append(position)
        
        position = self.position + (d,-1)
        if self.enemy(position):
            moves.append(position)
        
        position = self.position + (d,-1)
        if self.enemy(position):
            moves.append(position)
        
        position = self.position + (d,-1)
        if self.enemy(position):
            moves.append(position)
# V V 3 3
# P V V 3
# V V 3 3

# V V
# P V E
# V V

# V V
# P E
# V V

        vision = []
        position = self.position + (0,0-10)

    def get_moves_and_vision(self):
        d = 1 if self.team == 0 else -1 # direction

        # moves of the piece
        moves = []

        position = self.position + (d,-1)
        if self.enemy(position):
            moves.append(position)

        position = self.position + (d,1)
        if self.enemy(position):
            moves.append(position)
        
        position = self.position + (d,0)
        if not self.any_piece(position):
            moves.append(position)
            
            position = self.position + (d*2,0)
            if not self.any_piece(position):
                moves.append(position)




#####Porque hay un get vision en piece?
# Se ocupa prototipo? lo
# es el prototipo, literalmente ya esta completo asi, no

# Target
#
# (Bishop)
#
# Rook           Queen

# Aqui queen no cosideraria ir a target porque lo ataca rook, ese es mi punto wey
# pero esta cabron, porque y si si lo ve?

# mira mira facil, si lo separamos
# en vision y moves
# entonces en este caso sacariamos Rook.get_moves(Queen.get_vision())
# osea sacamos los movimientos de rook pero solo las piezas que ve queen puede bloquearlos
# y el nomral seria Rook.get_moves(Rook.get_vision())
# segun yo no, como no lo sacarias? no veo un caso imposible
# si, pero puedes sacar la vision directamente (mas codigo)
# ????
# mas o menos, osea no ocupas moves para sacar vision, pero si lo haria mas facil

#alv, va, osea y None es como todo el tablero o es un metodo aparte?
#Nmms, he pero para sacar vision no ocupas get moves?
#Como sacas vision?
#Osea yo saco los movimientos y despues veo cuales son las adyacentes
#Hmmm, como?
#Osea creo que ya 
#Hacer el get moves and vision pero solo retornar vision?
#OKOK, entonces implemento get_moves(vision) y get_vision() ? si
#Va

#Nononon pq al sacar los movimientos de la torre este mismo marcaria que no puede ir
#A target, osea como el get moves and vision
#a nmms y si la reyna no ve el bishop?, soy de lento aprendizaje
#Jajajajj
#Mejor que sean amigos y que rook le dija a cuales va
#Osea que es el parametro Queen.get_vision?



# Piece
# + LV: capture_value >= self.value
# + LV: Polvo magico (Cocaina)

# Pawn
# Value: 3
# Stamina: 3
# Range: 1 or 2
# Special movement : 2 (requires 3)
# Becomes queen at the opposite edge

# L2: Stamina + 2
# L3: Visibilidad + 1

# V V 3 3
# P V V 3
# V V 3 3

# Rook
# Value: 10
# Stamina: 5
# Range: 3

# L2: Range + 1
# L3: Stamina + 3

# Knight
# Value: 7
# Stamina: 4
# Range: yes

# L2: see adyacents
# L3: stamina + 2

#Bishop
# Value: 6
# Stamina: 4
# Range: 3

# L2: Range + 1
# L3: Stamina + 2

# Queen
# Value: 15
# Stamina: 8
# Range: 3
 
# L2: Range + 2 
# L3: Stamina + 2

# Movement map = Rook + Bishop

# King
# Value: 1e9
# Stamina: 5
# Range: 1

# L2: N/A
# L3: N/A

# V V V V V
# V V V V V
# V V P V V
# V V V V V
# V V V V V