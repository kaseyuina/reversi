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
    
    """
    Applying changes on the board by placing disks
    """
    def flipDisks(self, y, x):
 
        # Placing disk
        self.RawBoard[y, x] = self.CurrentColor
 
        # Fliping process will continue below
        # …

    """
    Placing disk
    """
    def place_disk(self, x, y):
 
        # Validating square position
        if x < 1 or BOARD_SIZE < x:
            return False
        if y < 1 or BOARD_SIZE < y:
            return False
        # if self.ValidPos[x, y] == 0:
            # return False
 
        # Fliping disk
        self.flipDisks(x, y)
 
        # Next turn
        self.Turns += 1
 
        # Switching color
        self.CurrentColor = - self.CurrentColor
        
        # Updating ValidPos and ValidDir
        # self.initValidation()
 
        return True
    

# Creating board instance
board = Board()
 
# Checking contents of RawBoard
# print(board.RawBoard)

# Calling place_disk function
print(board.place_disk(4, 3))

# Checking contents of RawBoard
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.RawBoard[x, y]), end = '')
    print()