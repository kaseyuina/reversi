"""
Library
"""
import numpy as np
 
"""
Variables
"""
# Square status
EMPTY = 0
LIGHT = -1
DARK = 1
WALL = 2
 
# Size of the board
BOARD_SIZE = 8
 
"""
Board class
"""
class Board:
 
    def __init__(self):
 
        # Set all the squares as empty
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
 
        # Setting walls
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL
 
        # Initial disk placement
        self.RawBoard[4, 4] = LIGHT
        self.RawBoard[5, 5] = LIGHT
        self.RawBoard[4, 5] = DARK
        self.RawBoard[5, 4] = DARK
 
        # Turns
        self.Turns = 0
 
        # Current color
        self.CurrentColor = DARK


# Creating board instance
board = Board()
 
# Checking contents of RawBoard
print(board.RawBoard)