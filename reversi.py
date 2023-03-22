""" Library """
import numpy as np
import tkinter as tk
import tkinter.messagebox as mbox
import sys
 
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

# AI status
AI_STAT = False

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
        self.strColor = {
            DARK : "DARK",
            LIGHT : "LIGHT"
        }

        # Set all the squares as empty
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
 
        # Setting walls
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL
 
        # Turns
        self.Turns = 0
 
        # Current color
        self.CurrentColor = DARK
    
        # Postion where disk can be placed and direction for flipping
        self.ValidPos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.ValidDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
 
        # Initializing ValidPos and ValidDir
        returnVal = self.initValidation(self.RawBoard, self.ValidPos, self.ValidDir, self.CurrentColor)
        self.RawBoard = returnVal[0]
        self.ValidPos = returnVal[1]
        self.ValidDir = returnVal[2]
        self.CurrentColor = returnVal[3]

        # Creating widgets
        self.createWidgets()

        # Setting events
        self.setEvents()

        # Initializing reversi
        self.initReversi()
        # self.RawBoard = np.array([
        #     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        #     [2, 1, 1,-1,-1, 1, 1, 1, 1, 2],
        #     [2, 1, 1,-1,-1,-1, 1,-1, 1, 2],
        #     [2, 1, 1, 1,-1, 1, 1, 1, 1, 2],
        #     [2, 1, 1,-1, 1,-1,-1, 0, 1, 2],
        #     [2, 1,-1, 1, 1, 1, 1, 1, 1, 2],
        #     [2, 1, 0,-1,-1,-1,-1, 1, 1, 2],
        #     [2, 1, 0, 0, 0, 0,-1, 1, 1, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
        # for y in range(10):
        #     for x in range(10):
        #         # print(self.RawBoard[x, y])
        #         if self.RawBoard[x, y] != 2:
        #             if self.RawBoard[x, y] != 0:
        #                 self.drawDisk(x-1, y-1, self.RawBoard[x, y])
        # self.initValidation()
    
        # Set values to all the squares
        # Values are used for AI to calculate where to put disks
        self.valuePoints = np.array([
            [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
            [0, 30,-12,  0, -1, -1,  0,-12, 30,  0],
            [0,-12,-15, -3, -3, -3, -3,-15,-12,  0],
            [0,  0, -3,  0, -1, -1,  0, -3,  0,  0],
            [0, -1, -3, -1, -1, -1, -1, -3, -1,  0],
            [0, -1, -3, -1, -1, -1, -1, -3, -1,  0],
            [0,  0, -3,  0, -1, -1,  0, -3,  0,  0],
            [0,-12,-15, -3, -3, -3, -3,-15,-12,  0],
            [0, 30,-12,  0, -1, -1,  0,-12, 30,  0],
            [0,  0,  0,  0,  0,  0,  0,  0,  0,  0]])
 
    ''' Evaluate disk state '''
    def EvaluateDiskStates(self, cpRawBoard, putDiskColor):
            lightScore = 0
            darkScore = 0
            for y in range(10):
                for x in range(10):
                    score = self.valuePoints[x, y]
                    if cpRawBoard[x, y] == LIGHT:
                        lightScore += score
                    elif cpRawBoard[x, y] == DARK:
                        darkScore += score
            if putDiskColor == LIGHT:
                return lightScore - darkScore
            return darkScore - lightScore

    def SearchNegaAlphaStone(self, cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, depth):
            # // 探索したストーン
            resultStoneIndex = None

            # // 置くことが可能なストーンを全て調べる
            alpha = -sys.maxsize + 1 #// MinValueを反転するとintの範囲を超えてしまうため、+1する
            beta = sys.maxsiz
            canPutStonesIndex = GetAllCanPutStonesIndex(stoneStates, putStoneState)
            for putStoneIndex in canPutStonesIndex:
                # // 次の階層の状態を調べる
                putStoneStates = GetPutStoneState(stoneStates, putStoneState, putStoneIndex.X, putStoneIndex.Z);
                score = -1 * self.GetNegaAlphaScore(putStoneStates, cpValidPos, cpValidDir, -cpCurrentColor, depth - 1, -beta, -alpha, False);

                # // 最大スコアの場合、スコアと該当インデックスを保持
                if alpha < score:
                    alpha = score
                    resultStoneIndex = putStoneIndex
            return resultStoneIndex

    def GetNegaAlphaScore(self, cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, depth, alpha, beta, isPrevPassed = False):
        # // 葉ノードで評価関数を実行
        if depth == 0:
            return self.EvaluateDiskStates(cpRawBoard, cpCurrentColor)
        # // 置くことが可能なストーンを全て調べる
        maxScore = -sys.maxsize
        # for y, putDiskCol in enumerate(cpValidPos):
        for y in range(10):
            # for x, putDiskRow in enumerate(putDiskCol):
            for x in range(10):
                # // 次の階層の状態を調べる
                resultValue = self.place_disk(cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, x, y)
                cpRawBoard = resultValue[0]
                cpValidPos = resultValue[1]
                cpValidDir = resultValue[2]
                cpCurrentColor = resultValue[3]
                score = -1 * self.GetNegaAlphaScore(cpRawBoard, cpValidPos, cpValidDir, -cpCurrentColor, depth - 1, -beta, -alpha, False)
                # // NegaMax値が探索範囲の上限より上の場合は枝狩り
                if score >= beta:
                    return score

                # // alpha値、maxScoreを更新
                alpha = max(alpha, score)
                maxScore = max(maxScore, score)

            # // 見つからなかった場合
            if maxScore == -sys.maxsize:
                # // ２回連続パスの場合、評価関数を実行
                if isPrevPassed:
                    return self.EvaluateDiskStates(cpRawBoard, cpCurrentColor);
                # // ストーン状態はそのままで、次の階層の状態を調べる
                return -1 * self.GetNegaAlphaScore(cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, depth - 1, -beta, -alpha, True);
        return maxScore

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
        # Showing initial message
        message = "This is " + self.strColor[self.CurrentColor] + "'s turn"
        self.message_label = tk.Message(self.master, text=message, font=("Arial", 14), fg="white", width=CANVAS_SIZE, anchor="w")
        self.message_label.pack()

        # Creating canvas
        self.canvas = tk.Canvas(
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
            self.RawBoard[x+1][y+1] = self.drawDisk(x, y, DARK)

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
            self.RawBoard[x+1][y+1] = self.drawDisk(x, y, LIGHT)

        # self.initValidation()
        returnVal = self.initValidation(self.RawBoard, self.ValidPos, self.ValidDir, self.CurrentColor)
        self.RawBoard = returnVal[0]
        self.ValidPos = returnVal[1]
        self.ValidDir = returnVal[2]
        self.CurrentColor = returnVal[3]

    def drawDisk(self, x, y, store_color):
        ''' Drawing a disk (circle) '''
        color = self.color[store_color]

        # Draws disk only when AI status is False
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
        return store_color

    def showPopup(self, input):
        # Getting window position
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        x1 = self.master.winfo_rootx()
        y1 = self.master.winfo_rooty()
        x2 = x1 + w
        y2 = y1 + h

        # Defining popup
        popup = tk.Toplevel(self.master)
        popup.title("")
        pw = 200
        ph = 30
        popup.wm_attributes("-topmost", True)
        popup.focus_force()
        popup.grab_set()
        popup.geometry(str(pw) + "x" + str(ph))

        # Showing popup in the middle of the window
        x = (x1 + x2) / 2 - pw / 2
        y = (y1 + y2) / 2 - ph / 2
        popup.geometry("+%d+%d" % (x, y))
        message = tk.Label(popup, text=input, width=CANVAS_SIZE)
        message.pack()
        
        # Closing the popup in 1 second
        popup.after(1500, popup.destroy)
            
        
    def click(self, event):
        ''' Operation when the board is clicked '''
        # if self.CurrentColor != DARK:
            # Does nothing during COM's turn
            # return
        AI_STAT = False

        # Calculating the clicked position
        x = event.x // self.square_size + 1
        y = event.y // self.square_size + 1

        # Placing a disk
        returnValue = self.place_disk(self.RawBoard, self.ValidPos, self.ValidDir, self.CurrentColor, x, y)
        self.RawBoard = returnValue[0]
        self.ValidPos = returnValue[1]
        self.ValidDir = returnValue[2]
        self.CurrentColor = returnValue[3]
        if not returnValue[4]:
        # if not self.place_disk(x, y):
            self.showPopup('Invalid square')

        # Game over check
        elif self.isGameOver():
            # # Displaying the result
                
            ## Number of each color
            count_dark = np.count_nonzero(self.RawBoard[:, :] == DARK)
            count_light = np.count_nonzero(self.RawBoard[:, :] == LIGHT)
                
            dark_result = 'Dark:  ' + str(count_dark)
            light_result = 'Light: ' + str(count_light)
            
            ## Result
            dif = count_dark - count_light
            if dif > 0:
                result_msg = 'Dark won the game!'
            elif dif < 0:
                result_msg = 'Light won the game!'
            else:
                result_msg = 'Draw game!'

            # Getting window position
            w = self.master.winfo_width()
            h = self.master.winfo_height()
            x1 = self.master.winfo_rootx()
            y1 = self.master.winfo_rooty()
            x2 = x1 + w
            y2 = y1 + h

            popup = tk.Toplevel(self.master)
            popup.title("Result")
            pw = 220
            ph = 200
            popup.wm_attributes("-topmost", True)
            popup.focus_force()
            popup.grab_set()
            popup.geometry(str(pw) + "x" + str(ph))

            # Showing popup in the middle of the window
            x = (x1 + x2) / 2 - pw / 2
            y = (y1 + y2) / 2 - ph / 2
            popup.geometry("+%d+%d" % (x, y))
            message = tk.Label(popup, text=dark_result, width=CANVAS_SIZE)
            message.pack()
            message = tk.Label(popup, text=light_result, width=CANVAS_SIZE)
            message.pack()
            message = tk.Label(popup, text=" ", width=CANVAS_SIZE)
            message.pack()
            message = tk.Label(popup, text=result_msg, font=("Arial", 18), width=CANVAS_SIZE)
            message.pack()
            message = tk.Label(popup, text=" ", width=CANVAS_SIZE)
            message.pack()
            def button_click():
                self.master.destroy()
            button = tk.Button(popup, text="Close", command=button_click)
            button.pack()

        # Pass
        elif not self.ValidPos[:, :].any():
            self.CurrentColor = - self.CurrentColor
            message = "This is " + self.strColor[self.CurrentColor] + "'s turn"
            self.message_label.config(text=message)
            # self.initValidation()
            returnVal = self.initValidation(self.RawBoard, self.ValidPos, self.ValidDir, self.CurrentColor)
            self.RawBoard = returnVal[0]
            self.ValidPos = returnVal[1]
            self.ValidDir = returnVal[2]
            self.CurrentColor = returnVal[3]
            self.showPopup(self.strColor[self.CurrentColor] + "'s turn passed")
        
        # print(self.strColor[self.CurrentColor] + str(self.EvaluateDiskStates()))
        cpRawBoard = self.RawBoard
        cpValidPos = self.ValidPos
        self.GetNegaMaxScore(cpRawBoard, cpValidPos, self.CurrentColor, 3, False)

    """ Checking which direction disks can flip """
    def checkValidation(self, cpRawBoard, x, y, color):
        # Stores direction
        dir = 0
 
        # Invalid when disk already exists
        if(cpRawBoard[x, y] != EMPTY):
        # if(self.RawBoard[x, y] != EMPTY):
            return dir
 
        ## Left
        if(cpRawBoard[x - 1, y] == - color): #Checking if the other color exists
            x_tmp = x - 2
            y_tmp = y
 
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | LEFT
 
        ## Upper left
        if(cpRawBoard[x - 1, y - 1] == - color): #Checking if the other color exists
            x_tmp = x - 2
            y_tmp = y - 2
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_LEFT
 
        ## Upper
        if(cpRawBoard[x, y - 1] == - color): #Checking if the other color exists
            x_tmp = x
            y_tmp = y - 2
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                y_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER
 
        ## Upper right
        if(cpRawBoard[x + 1, y - 1] == - color): #Checking if the other color exists
            x_tmp = x + 2
            y_tmp = y - 2
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp -= 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_RIGHT
 
        ## Right
        if(cpRawBoard[x + 1, y] == - color): #Checking if the other color exists
            x_tmp = x + 2
            y_tmp = y
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | RIGHT
 
        ## Lower right
        if(cpRawBoard[x + 1, y + 1] == - color): #Checking if the other color exists
            x_tmp = x + 2
            y_tmp = y + 2
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_RIGHT
 
        ## Lower
        if(cpRawBoard[x, y + 1] == - color): #Checking if the other color exists
            x_tmp = x
            y_tmp = y + 2
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                y_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER
 
        ## Lower left
        if(cpRawBoard[x - 1, y + 1] == - color): #Checking if the other color exists
            x_tmp = x - 2
            y_tmp = y + 2
            
            # Loops while the other color continues
            while cpRawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp += 1
            
            # Update dir if self color sandwitches the other color
            if cpRawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_LEFT
 
        return dir
    
    """ Applying changes on the board by placing disks """
    def flipDisks(self, cpRawBoard, cpValidDir, cpCurrentColor, x, y):
        # Placing disk
        cpRawBoard[x, y] = self.drawDisk(x-1, y-1, cpCurrentColor)
 
        # Flipping disks
        # Inputting dir in (y, x) in ValidDir
        dir = cpValidDir[x, y]
 
        ## LEFT
        if dir & LEFT: 
            x_tmp = x - 1
 
            # Loops until hitting other color
            while cpRawBoard[x_tmp, y] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x_tmp][y] = self.drawDisk(x_tmp-1, y-1, cpCurrentColor) #GUI version
 
                # Next loop to the LEFT
                x_tmp -= 1
 
        ## UPPER LEFT
        if dir & UPPER_LEFT: 
            x_tmp = x - 1
            y_tmp = y - 1
 
            # Loops until hitting other color
            while cpRawBoard[x_tmp, y_tmp] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x_tmp][y_tmp] = self.drawDisk(x_tmp-1, y_tmp-1, cpCurrentColor) #GUI version
                
                # Next loop to the UPPER LEFT
                x_tmp -= 1
                y_tmp -= 1
 
        ## UPPER
        if dir & UPPER: 
            y_tmp = y - 1
 
            # Loops until hitting other color
            while cpRawBoard[x, y_tmp] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x][y_tmp] = self.drawDisk(x-1, y_tmp-1, cpCurrentColor) #GUI version
 
                # Next loop to the UPPER
                y_tmp -= 1
 
        ## UPPER RIGHT
        if dir & UPPER_RIGHT: 
            x_tmp = x + 1
            y_tmp = y - 1
 
            # Loops until hitting other color
            while cpRawBoard[x_tmp, y_tmp] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x_tmp][y_tmp] = self.drawDisk(x_tmp-1, y_tmp-1, cpCurrentColor) #GUI version
 
                # Next loop to the UPPER RIGHT
                x_tmp += 1
                y_tmp -= 1
 
        ## RIGHT
        if dir & RIGHT: 
            x_tmp = x + 1
 
            # Loops until hitting other color
            while cpRawBoard[x_tmp, y] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x_tmp][y] = self.drawDisk(x_tmp-1, y-1, cpCurrentColor) #GUI version
                
                # Next loop to the RIGHT
                x_tmp += 1
 
        ## LOWER RIGHT
        if dir & LOWER_RIGHT: 
            x_tmp = x + 1
            y_tmp = y + 1
 
            # Loops until hitting other color
            while cpRawBoard[x_tmp, y_tmp] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x_tmp][y_tmp] = self.drawDisk(x_tmp-1, y_tmp-1, cpCurrentColor) #GUI version
 
                # Next loop to the LOWER RIGHT
                x_tmp += 1
                y_tmp += 1
 
        ## LOWER
        if dir & LOWER: 
            y_tmp = y + 1
 
            # Loops until hitting other color
            while cpRawBoard[x, y_tmp] == - cpCurrentColor:
 
                # Changing color
                cpRawBoard[x][y_tmp] = self.drawDisk(x-1, y_tmp-1, cpCurrentColor) #GUI version
 
                # Next loop to the LOWER
                y_tmp += 1
 
        ## LOWER LEFT
        if dir & LOWER_LEFT: 
            x_tmp = x - 1
            y_tmp = y + 1
 
            # Loops until hitting other color
            while cpRawBoard[x_tmp, y_tmp] == - cpCurrentColor:
                
                # Changing color
                cpRawBoard[x_tmp][y_tmp] = self.drawDisk(x_tmp-1, y_tmp-1, cpCurrentColor) #GUI version
 
                # Next loop to the LOWER LEFT
                x_tmp -= 1
                y_tmp += 1

        return cpRawBoard, cpValidDir, cpCurrentColor

    """ Placing disk """
    def place_disk(self, cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, x, y):
 
        # Validating square position
        if x < 1 or BOARD_SIZE < x:
            return cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, False
        if y < 1 or BOARD_SIZE < y:
            return cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, False
        if cpValidPos[x, y] == 0:
            return cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, False
        # Flipping disk
        returnValue = self.flipDisks(cpRawBoard, cpValidDir, cpCurrentColor, x, y)
        cpRawBoard = returnValue[0]
        cpValidDir = returnValue[1]
        cpCurrentColor = returnValue[2]
 
        # Next turn
        self.Turns += 1
 
        # Switching color
        cpCurrentColor = - cpCurrentColor
        
        # Updating ValidPos and ValidDir
        returnVal = self.initValidation(cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor)
        cpRawBoard = returnVal[0]
        cpValidPos = returnVal[1]
        cpValidDir = returnVal[2]
        cpCurrentColor = returnVal[3]

        message = "This is " + self.strColor[cpCurrentColor] + "'s turn"
        self.message_label.config(text=message)
 
        return cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor, True

    """ Updating ValidPos and ValidDir """
    def initValidation(self, cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor):
 
        # Initializing ValidPos (initialized to False for all)
        cpValidPos[:, :] = False
 
        # Loops in all squares besides WALL
        for x in range(1, BOARD_SIZE + 1):
            for y in range(1, BOARD_SIZE + 1):
 
                # Running checkValidation function
                dir = self.checkValidation(cpRawBoard, x, y, cpCurrentColor)
 
                # Inputting dir to ValidDir in each square
                cpValidDir[x, y] = dir
 
                # Input True into ValidPos if dir is not 0
                if dir != 0:
                    cpValidPos[x, y] = True
        return cpRawBoard, cpValidPos, cpValidDir, cpCurrentColor

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
                if self.checkValidation(self.RawBoard, x, y, - self.CurrentColor) != 0:
                    return False
 
        # Game is over when reaching to this point
        return True


''' Main code '''
app = tk.Tk()
app.title('Reversi')
reversi = Board(app)
app.mainloop()
