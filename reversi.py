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

# Direction(binary)
NONE = 0
LEFT = 2**0 # =1
UPPER_LEFT = 2**1 # =2 
UPPER = 2**2 # =4
UPPER_RIGHT = 2**3 # =8
RIGHT = 2**4 # =16
LOWER_RIGHT = 2**5 # =32
LOWER = 2**6 # =64
LOWER_LEFT = 2**7 # =128
 
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
    
        # Postion where disk can be placed and direction for flipping
        self.ValidPos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.ValidDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
 
        # Initializing ValidPos and ValidDir
        self.initValidation()
    
    """
    Checking which direction disks can flip
    """
    def checkValidation(self, x, y, color):
 
        # Stores direction
        dir = 0
 
        # Invalid when disk already exists
        if(self.RawBoard[x, y] != EMPTY):
            return dir
 
        ## Left
        if(self.RawBoard[x - 1, y] == - color): #Checking if the other color exists
            
            x_tmp = x - 2
            y_tmp = y
 
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LEFT
 
        ## Upper left
        if(self.RawBoard[x - 1, y - 1] == - color): #Checking if the other color exists
            
            x_tmp = x - 2
            y_tmp = y - 2
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_LEFT
 
        ## Upper
        if(self.RawBoard[x, y - 1] == - color): #Checking if the other color exists
            
            x_tmp = x
            y_tmp = y - 2
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER
 
        ## Upper right
        if(self.RawBoard[x + 1, y - 1] == - color): #Checking if the other color exists
            
            x_tmp = x + 2
            y_tmp = y - 2
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_RIGHT
 
        ## Right
        if(self.RawBoard[x + 1, y] == - color): #Checking if the other color exists
 
            x_tmp = x + 2
            y_tmp = y
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | RIGHT
 
        ## Lower right
        if(self.RawBoard[x + 1, y + 1] == - color): #Checking if the other color exists
            
            x_tmp = x + 2
            y_tmp = y + 2
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_RIGHT
 
        ## Lower
        if(self.RawBoard[x, y + 1] == - color): #Checking if the other color exists
            
            x_tmp = x
            y_tmp = y + 2
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER
 
        ## Lower left
        if(self.RawBoard[x - 1, y + 1] == - color): #Checking if the other color exists
            
            x_tmp = x - 2
            y_tmp = y + 2
            
            # Loops while the other color continues
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_LEFT
 
        return dir
 
 
    
    """
    Applying changes on the board by placing disks
    """
    def flipDisks(self, y, x):
 
        # Placing disk
        self.RawBoard[y, x] = self.CurrentColor
 
        # Flipping disks
        # Inputting dir in (y, x) in ValidDir
        dir = self.ValidDir[x, y]
 
        ## LEFT
        if dir & LEFT: 
 
            x_tmp = x - 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x_tmp, y] = self.CurrentColor
 
                # Next loop to the LEFT
                x_tmp -= 1
 
        ## UPPER LEFT
        if dir & UPPER_LEFT: 
 
            x_tmp = x - 1
            y_tmp = y - 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                
                # Next loop to the UPPER LEFT
                x_tmp -= 1
                y_tmp -= 1
 
        ## UPPER
        if dir & UPPER: 
 
            y_tmp = y - 1
 
            # Loops until hitting other color
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x, y_tmp] = self.CurrentColor
 
                # Next loop to the UPPER
                y_tmp -= 1
 
        ## UPPER RIGHT
        if dir & UPPER_RIGHT: 
 
            x_tmp = x + 1
            y_tmp = y - 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
 
                # Next loop to the UPPER RIGHT
                x_tmp += 1
                y_tmp -= 1
 
        ## RIGHT
        if dir & RIGHT: 
 
            x_tmp = x + 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x_tmp, y] = self.CurrentColor
                
                # Next loop to the RIGHT
                x_tmp += 1
 
        ## LOWER RIGHT
        if dir & LOWER_RIGHT: 
 
            x_tmp = x + 1
            y_tmp = y + 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
 
                # Next loop to the LOWER RIGHT
                x_tmp += 1
                y_tmp += 1
 
        ## LOWER
        print(dir, LOWER)
        if dir & LOWER: 
 
            y_tmp = y + 1
 
            # Loops until hitting other color
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:
 
                # Changing color
                self.RawBoard[x, y_tmp] = self.CurrentColor
 
                # Next loop to the LOWER
                y_tmp += 1
 
        ## LOWER LEFT
        if dir & LOWER_LEFT: 
 
            x_tmp = x - 1
            y_tmp = y + 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                
                # Changing color
                self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
 
                # Next loop to the LOWER LEFT
                x_tmp -= 1
                y_tmp += 1

    """
    Placing disk
    """
    def place_disk(self, x, y):
 
        # Validating square position
        if x < 1 or BOARD_SIZE < x:
            return False
        if y < 1 or BOARD_SIZE < y:
            return False
        if self.ValidPos[x, y] == 0:
            return False
 
        # Flipping disk
        self.flipDisks(x, y)
 
        # Next turn
        self.Turns += 1
 
        # Switching color
        self.CurrentColor = - self.CurrentColor
        
        # Updating ValidPos and ValidDir
        self.initValidation()
 
        return True

    """
    Updating ValidPos and ValidDir
    """
    def initValidation(self):
 
        # Initializing ValidPos (initialized to False for all)
        self.ValidPos[:, :] = False
 
        # Loops in all squares besides WALL
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):
 
                # Running checkValidation function
                dir = self.checkValidation(x, y, self.CurrentColor)
 
                # Inputting dir to ValidDir in each square
                self.ValidDir[x, y] = dir
 
                # Input True into ValidPos if dir is not 0
                if dir != 0:
                    self.ValidPos[x, y] = True

# Creating board instance
board = Board()

# Placing a disk
# if not board.place_disk(4, 3):
if not board.place_disk(1, 3):
    print('Invalid square')
 
# Test
# Confirming the contents of RawBoard
print('RawBoard')
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.RawBoard[x, y]), end = '')
    print()
 
# Confirming the contents of ValidPos
print('ValidPos')
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.ValidPos[x, y]), end = '')
    print()
 
# Confirming the contents of ValidDir
print('ValidDir')
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.ValidDir[x, y]), end = '')
    print()