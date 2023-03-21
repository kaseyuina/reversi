# Reversi Program
This program is a Reversi game written in Python. It is created using the Tkinter module for the GUI.

## [How to Play]
Reversi is a two-player game where the players take turns placing disks on the board. The objective is to have the majority of disks of your color at the end of the game.

When a player places a disk on the board, they must place it adjacent to an opponent's disk, and the opponent's disks between the newly placed disk and any other disks of the player's color must be flipped over to the player's color.

The game ends when there are no more valid moves left, or the board is filled. The player with the most disks of their color on the board at the end of the game wins.

## [Installation and Usage]
To use this program, you must have Python 3.x installed on your computer.

Clone or download the repository from GitHub.

Run the program using the following command:
    python reversi.py

## [Features]
The game is played on an 8x8 board.
The program uses numpy for the board representation and validation.
The GUI is created using Tkinter.
The program supports undo functionality, where the player can undo their last move.
The program detects the end of the game and announces the winner.
The program provides a message label to indicate the current player's turn.

## [Future Improvements]
The program can be improved by implementing an AI player using algorithms such as the minimax algorithm.

## [Code Overview]
The program consists of a single class Board, which contains all the necessary functions and variables to play the game. The functions are responsible for initializing the board, drawing the board on the GUI, validating moves, flipping disks, detecting the end of the game, and more.

The Board class uses numpy for the board representation and validation. The GUI is created using Tkinter. The program uses object-oriented programming principles to organize the code and simplify the implementation.

## [Author]
The program is created by Tsutomu Nakajima.
