""" Library """
import numpy as np
import tkinter
import tkinter.messagebox
 
""" Variables """
# Square status
EMPTY = 0
LIGHT = -1
DARK = 1
WALL = 2
 
# Size of the board
BOARD_SIZE = 8
CANVAS_SIZE = 400

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

# Board address
IN_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
IN_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8']
 
# Maximum turns
MAX_TURNS = 60

# Color setting
BOARD_COLOR = 'green'
DARK_COLOR = 'black'
LIGHT_COLOR = 'white'


""" Board class """
class Board:
    def __init__(self, master):
        #Parent wedget
        self.master = master
        self.color = { # Dictionary to hold disk color
            DARK : DARK_COLOR,
            LIGHT : LIGHT_COLOR
        }

        # Set all the squares as empty
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
 
        # Setting walls
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL
 
        # # Initial disk placement
        # self.RawBoard[4, 4] = LIGHT
        # self.RawBoard[5, 5] = LIGHT
        # self.RawBoard[4, 5] = DARK
        # self.RawBoard[5, 4] = DARK
 
        # Turns
        self.Turns = 0
 
        # Current color
        self.CurrentColor = DARK
    
        # Postion where disk can be placed and direction for flipping
        self.ValidPos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.ValidDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
 
        # Initializing ValidPos and ValidDir
        self.initValidation()

        # Creating widgets
        self.createWidgets()

        # Setting events
        self.setEvents()

        # Initializing reversi
        self.initReversi()

    def testBoard(self):
        print('RawBoard')
        for y in range(10):
            for x in range(10):
                print('{:^3}'.format(self.RawBoard[x, y]), end = '')
            print()
        
        # # Confirming the contents of ValidPos
        print('ValidPos')
        for y in range(10):
            for x in range(10):
                print('{:^3}'.format(self.ValidPos[x, y]), end = '')
            print()
        
        # # Confirming the contents of ValidDir
        print('ValidDir')
        for y in range(10):
            for x in range(10):
                print('{:^3}'.format(self.ValidDir[x, y]), end = '')
            print()

    
    ''' Creating widget '''
    def createWidgets(self):

        # Creating canvas
        self.canvas = tkinter.Canvas(
            self.master,
            bg=BOARD_COLOR,
            width=CANVAS_SIZE+1, # +1 is for drawing line
            height=CANVAS_SIZE+1, # +1 is for drawing line
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

    ''' Setting events '''
    def setEvents(self):

        # Detecting mouse click on the canvas
        self.canvas.bind('<ButtonPress>', self.click)

    ''' Initializing game '''
    def initReversi(self):
        # Calculating the size of a square (px)
        self.square_size = CANVAS_SIZE // BOARD_SIZE

        # Drawing squares
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                # Calculating beginning and ending coordinates of the square
                xs = x * self.square_size
                ys = y * self.square_size
                xe = (x + 1) * self.square_size
                ye = (y + 1) * self.square_size
                
                # Drawing a square
                tag_name = 'square_' + str(x) + '_' + str(y)
                self.canvas.create_rectangle(
                    xs, ys,
                    xe, ye,
                    tag=tag_name
                )

        # Calculating a position to draw dark disks
        dark_init_pos_1_x = BOARD_SIZE // 2 - 1
        dark_init_pos_1_y = BOARD_SIZE // 2
        dark_init_pos_2_x = BOARD_SIZE // 2
        dark_init_pos_2_y = BOARD_SIZE // 2 - 1

        dark_init_pos = (
            (dark_init_pos_1_x, dark_init_pos_1_y),
            (dark_init_pos_2_x, dark_init_pos_2_y)
        )

        # Drawing disks
        for x, y in dark_init_pos:
            self.drawDisk(x, y, DARK)

        # Calculating a position to draw light disks
        light_init_pos_1_x = BOARD_SIZE // 2
        light_init_pos_1_y = BOARD_SIZE // 2
        light_init_pos_2_x = BOARD_SIZE // 2 - 1
        light_init_pos_2_y = BOARD_SIZE // 2 - 1

        light_init_pos = (
            (light_init_pos_1_x, light_init_pos_1_y),
            (light_init_pos_2_x, light_init_pos_2_y)
        )

        # Drawing disks
        for x, y in light_init_pos:
            self.drawDisk(x, y, LIGHT)

        self.initValidation()

    def drawDisk(self, x, y, store_color):
        ''' Drawing a disk (circle) '''
        color = self.color[store_color]

        # Calculating a center position of (x,y) square
        center_x = (x + 0.5) * self.square_size
        center_y = (y + 0.5) * self.square_size

        # Calculating start and end from the center
        xs = center_x - (self.square_size * 0.8) // 2
        ys = center_y - (self.square_size * 0.8) // 2
        xe = center_x + (self.square_size * 0.8) // 2
        ye = center_y + (self.square_size * 0.8) // 2
        
        # Drawing a circle
        tag_name = 'disk_' + str(x) + '_' + str(y)
        self.canvas.create_oval(
            xs, ys,
            xe, ye,
            fill=color,
            tag=tag_name
        )
        
        # Storing the color to the board
        self.RawBoard[x+1][y+1] = store_color

    def click(self, event):
        ''' Operation when the board is clicked '''

        # if self.CurrentColor != DARK:
            # Does nothing during COM's turn
            # return

        # Calculating the clicked position
        x = event.x // self.square_size + 1
        y = event.y // self.square_size + 1

        # if self.checkPlacable(x, y):
        # print(self.ValidPos[x,y])
        if not self.place_disk(x, y):
            print('Invalid address')
        
    """ Checking which direction disks can flip """
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
    
    """ Applying changes on the board by placing disks """
    def flipDisks(self, x, y):
        # Placing disk
        self.RawBoard[x, y] = self.CurrentColor
        self.drawDisk(x-1, y-1, self.CurrentColor)
 
        # Flipping disks
        # Inputting dir in (y, x) in ValidDir
        dir = self.ValidDir[x, y]
 
        ## LEFT
        if dir & LEFT: 
            x_tmp = x - 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x_tmp, y] = self.CurrentColor
                self.drawDisk(x_tmp-1, y-1, self.CurrentColor) #GUI version
 
                # Next loop to the LEFT
                x_tmp -= 1
 
        ## UPPER LEFT
        if dir & UPPER_LEFT: 
            x_tmp = x - 1
            y_tmp = y - 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                self.drawDisk(x_tmp-1, y_tmp-1, self.CurrentColor) #GUI version
                
                # Next loop to the UPPER LEFT
                x_tmp -= 1
                y_tmp -= 1
 
        ## UPPER
        if dir & UPPER: 
            y_tmp = y - 1
 
            # Loops until hitting other color
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x, y_tmp] = self.CurrentColor
                self.drawDisk(x-1, y_tmp-1, self.CurrentColor) #GUI version
 
                # Next loop to the UPPER
                y_tmp -= 1
 
        ## UPPER RIGHT
        if dir & UPPER_RIGHT: 
            x_tmp = x + 1
            y_tmp = y - 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                self.drawDisk(x_tmp-1, y_tmp-1, self.CurrentColor) #GUI version
 
                # Next loop to the UPPER RIGHT
                x_tmp += 1
                y_tmp -= 1
 
        ## RIGHT
        if dir & RIGHT: 
            x_tmp = x + 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x_tmp, y] = self.CurrentColor
                self.drawDisk(x_tmp-1, y-1, self.CurrentColor) #GUI version
                
                # Next loop to the RIGHT
                x_tmp += 1
 
        ## LOWER RIGHT
        if dir & LOWER_RIGHT: 
            x_tmp = x + 1
            y_tmp = y + 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                self.drawDisk(x_tmp-1, y_tmp-1, self.CurrentColor) #GUI version
 
                # Next loop to the LOWER RIGHT
                x_tmp += 1
                y_tmp += 1
 
        ## LOWER
        # print(dir, LOWER)
        if dir & LOWER: 
            y_tmp = y + 1
 
            # Loops until hitting other color
            while self.RawBoard[x, y_tmp] == - self.CurrentColor:
 
                # Changing color
                # self.RawBoard[x, y_tmp] = self.CurrentColor
                self.drawDisk(x-1, y_tmp-1, self.CurrentColor) #GUI version
 
                # Next loop to the LOWER
                y_tmp += 1
 
        ## LOWER LEFT
        if dir & LOWER_LEFT: 
            x_tmp = x - 1
            y_tmp = y + 1
 
            # Loops until hitting other color
            while self.RawBoard[x_tmp, y_tmp] == - self.CurrentColor:
                
                # Changing color
                # self.RawBoard[x_tmp, y_tmp] = self.CurrentColor
                self.drawDisk(x_tmp-1, y_tmp-1, self.CurrentColor) #GUI version
 
                # Next loop to the LOWER LEFT
                x_tmp -= 1
                y_tmp += 1

    """ Placing disk """
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

    """ Updating ValidPos and ValidDir """
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

    """ Displaying board """
    def display(self):
 
        # columns
        print('  a b c d e f g h')
        # Looping all columns
        for y in range(1, 9):
 
            # rows
            print(str(y) + " ", end="")
            for x in range(1, 9):
                # Inputting a square status in "grid"
                grid = self.RawBoard[x, y]
 
                # Changing square depending on the status
                if grid == EMPTY: # Empty
                    print('{:^2}'.format('□'), end = '')
                elif grid == LIGHT: # Light
                    print('{:^2}'.format('●'), end = '')
                elif grid == DARK: # Dark
                    print('{:^2}'.format('○'), end = '')
 
            print()
        print()
        
    """ Validating the input address """
    def inputValidation(self, IN):
        # Length check
        if not len(IN) == 2:
            return False
 
        # Checking if the first and second letters in IN are valid
        if IN[0] in IN_ALPHABET:
            if IN[1] in IN_NUMBER:
                return True
 
        return False

    """ Game over check """
    def isGameOver(self):
 
        # Game is over when reaches to 60 turns
        if self.Turns >= MAX_TURNS:
            return True
 
        # Game is not over if there is any open square during own turn
        if self.ValidPos[:, :].any():
            return False
 
        # Game is not over if there is any open square during the other's turn
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):
 
                # Game is not over if there is any open square
                if self.checkValidation(x, y, - self.CurrentColor) != 0:
                    return False
 
        # Game is over when reaching to this point
        return True


app = tkinter.Tk()
app.title('Reversi')
reversi = Board(app)
app.mainloop()

''' Main code '''
# Creating board instance
board = Board()

"""
# For testing
board.RawBoard = np.array([
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1,-1,-1, 1, 1, 1, 1, 2],
    [2, 1, 1,-1,-1,-1, 1,-1, 1, 2],
    [2, 1, 1, 1,-1, 1, 1, 1, 1, 2],
    [2, 1, 1,-1, 1,-1,-1, 0, 1, 2],
    [2, 1,-1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 0,-1,-1,-1,-1, 1, 1, 2],
    [2, 1, 0, 0, 0, 0,-1, 1, 1, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
board.initValidation()
"""

# Displaying the board
board.display()

# Looping turns
while True:
    # Displaying the board
    board.display()
 
    # Showing turns
    if board.CurrentColor == DARK:
        print("Dark's turn: ", end = "")
    else:
        print("Light's turn: ", end = "")
    IN = input()
    print()

    # Input validation
    if board.inputValidation(IN):
        x = IN_ALPHABET.index(IN[0]) + 1
        y = IN_NUMBER.index(IN[1]) + 1
    else:
        print('Please input in the correct format (e.g.: f5)')
        continue

    # Placing a disk
    if not board.place_disk(x, y):
        print('Invalid address')
        continue
    
    # Game over check
    if board.isGameOver():
        board.display()
        print('Game over')
        break

    # Pass
    if not board.ValidPos[:, :].any():
        board.CurrentColor = - board.CurrentColor
        board.initValidation()
        print('Turn passed')
        print()
        continue

# Displaying the result
print()
    
## Number of each color
count_dark = np.count_nonzero(board.RawBoard[:, :] == DARK)
count_light = np.count_nonzero(board.RawBoard[:, :] == LIGHT)
    
print('Dark:  ', count_dark)
print('Light: ', count_light)
 
## Result
dif = count_dark - count_light
if dif > 0:
    print('Dark won the game!')
elif dif < 0:
    print('Light won the game!')
else:
    print('Draw game!')

# Test
# Confirming the contents of RawBoard
# print('RawBoard')
# for y in range(10):
#     for x in range(10):
#         print('{:^3}'.format(board.RawBoard[x, y]), end = '')
#     print()
 
# # Confirming the contents of ValidPos
# print('ValidPos')
# for y in range(10):
#     for x in range(10):
#         print('{:^3}'.format(board.ValidPos[x, y]), end = '')
#     print()
 
# # Confirming the contents of ValidDir
# print('ValidDir')
# for y in range(10):
#     for x in range(10):
#         print('{:^3}'.format(board.ValidDir[x, y]), end = '')
#     print()