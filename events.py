from pieces.pieces import *

def create_default(team: int):
    if team == 0:
        col1,col2 = 0,1
    else:
        col1,col2 = 15,14
    
    order: list[type[Piece]] = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece in enumerate(order):
        piece((col1, i+2), team)
        Pawn((col2, i+2), team)