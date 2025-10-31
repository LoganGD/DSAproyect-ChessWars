import random
import grid
from pieces import *
from constants import *

def random_event():
    return 
    opts = []
    probs = []

    opts.append(attack_wave)
    probs.append(1)

    opts.append(create_pieces)
    probs.append(1)

    opts.append(retreat)
    probs.append(1)

    random.choices(opts,probs)()

def attack_wave():
    options = Piece.deque[1][:]
    random.shuffle(options)
    for piece in options[:5]:
        piece.current_order = "Attack"

def create_pieces():
    pass

def retreat():
    for piece in Piece.deque[1]:
        piece.current_order = "Defend"