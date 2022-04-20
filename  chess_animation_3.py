from decimal import Clamped
import enum
from signal import pause
import sys
from re import T
import turtle
from unittest import expectedFailure
import time


"""
This code generates the path required for a knight's tour
around a chessboard with user-specified dimensions
Written by Sophie Li, 2017
http://blog.justsophie.com/algorithm-for-knights-tour-in-python/
"""


# set up the screen display of the board
size = 5
window = turtle.Screen()
window.title("Knights tour. SIT215. Group 13")
window.setup(width=800, height=800)  # (0,0) is in the centre
window.tracer(0)
chessboard = turtle.Turtle()
# draw board background
chessboard.penup()  # to not draw a line
chessboard.goto(-(size*50), (size*50))
a = 0  # for alternating row colours
b = 0  # for alternating column colours
for i in range(size):
    if (b == 0):
        a = 1
    else:
        a = 0
    for j in range(size):
        chessboard.penup()
        chessboard.goto(j*100-400, i*100*(-1)+400)
        chessboard.pendown()
        if (a == 0):
            chessboard.fillcolor('grey')
            a = 1
        else:
            chessboard.fillcolor('white')
            a = 0
        chessboard.begin_fill()
        for k in range(4):
            chessboard.forward(100)
            chessboard.right(90)
        chessboard.end_fill()
    if (b == 0):
        b = 1
    else:
        b = 0

# create an array of turtles for each cell visited
board_squares = []
for i in range(size*size):
    board_squares.append(turtle.Turtle())
visited = []
# create a placeholder for the move number
text_turtle = turtle.Turtle()

# draw the visited cell number on the screen


def visited_text(turtle, x_y_path, color, i):
    turtle.color(color)
    text_turtle.write(i, align='center', font=('Arial', 20, 'normal'))
    window.update()

# displays the moves on the chess board display


def visited_cell(turtle, x_y_path, color, i):
    visited_text(turtle, x_y_path, "red", i)
    # change sleep time to change animation speed
    time.sleep(0.2)
    turtle.penup()  # to not draw a line
    turtle.color(color)
    # turtle.shape("square")
    turtle.shapesize(stretch_wid=5, stretch_len=5)  # 20 pixels is default
    turtle.goto(x_y_path[0], x_y_path[1])
    text_turtle.goto(x_y_path[0], x_y_path[1])


# translates the size*size array into coordinates of the chessboard on the screen
def map_coords(x_y_path):
    # x from 0 to 7
    # height from -350 to 350
    # create coordinate system for board
    rescale = []
    value = 0

    for i in range(1):
        if (x_y_path[0] == 0):
            value = -350
        elif (x_y_path[0] == 1):
            value = -250
        elif (x_y_path[0] == 2):
            value = -150
        elif (x_y_path[0] == 3):
            value = -50
        elif (x_y_path[0] == 4):
            value = 50
        elif (x_y_path[0] == 5):
            value = 150
        elif (x_y_path[0] == 6):
            value = 250
        elif (x_y_path[0] == 7):
            value = 350
        rescale.append(value)
    for i in range(1):
        if (x_y_path[1] == 0):
            value = 350
        elif (x_y_path[1] == 1):
            value = 250
        elif (x_y_path[1] == 2):
            value = 150
        elif (x_y_path[1] == 3):
            value = 50
        elif (x_y_path[1] == 4):
            value = -50
        elif (x_y_path[1] == 5):
            value = -150
        elif (x_y_path[1] == 6):
            value = -250
        elif (x_y_path[1] == 7):
            value = -350
        rescale.append(value)
    return rescale


''''
state space search
'''


class KnightsTour:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.board = []  # empty array for the board
        self.generate_board()

    def generate_board(self):
        """
        Creates a nested list to represent the game board
        each element of list is a list of same size
        """
        for i in range(self.h):  # for every height row
            # append a elements the length of a column
            self.board.append([0]*self.w)

    def print_board(self):
        """"
        Prints the move numbers of the solved chess board
        """
        print("  ")
        print("------")
        for elem in self.board:
            print(elem)  # column-wise OR row-wise???
        print("------")
        print("  ")

    def animate(self):
        """"
        Shows the animation of moves on the screen
        """
        for i in range(size*size):
            visited_cell(board_squares[i], map_coords(
                path[i]), "red", i)

    def generate_legal_moves(self, cur_pos):
        """
        Generates a list of legal moves for the knight to take next
        Checks each move is allowed according to valid move of a knight
        """
        possible_pos = []  # array of options
        move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                        (2, 1), (2, -1), (-2, 1), (-2, -1)]  # x,y coordinates for moves

        for move in move_offsets:  # try each possible of the 8 moves for the knight
            # add the element in first position of tupple
            new_x = cur_pos[0] + move[0]
            # add the element of second position of tupple
            new_y = cur_pos[1] + move[1]

            if (new_x >= self.h):  # check if going wrong height direction
                continue
            elif (new_x < 0):  # check if horizontally out of bounds of board
                continue
            elif(new_y >= self.w):  # check if going wrong width direction
                continue
            elif (new_y < 0):  # check if vertically out of bounds of board
                continue
            else:
                # if check pass then append to array of options
                possible_pos.append((new_x, new_y))
        return possible_pos

    def sort_lonely_neighbours(self, to_visit, wand):
        """
        It is more efficient to visit the lonely neighbors first,
        since these are at the edges of the chessboard and cannot
        be reached easily if done later in the traversal
        This is the warnsdorffs_heuristic which can be turned on/off
        """
        neighbour_list = self.generate_legal_moves(to_visit)
        empty_neighbours = []

        # add a neighbour if the cell is empty (hasnt been visited)
        for neighbour in neighbour_list:
            np_value = self.board[neighbour[0]][neighbour[1]]
            if np_value == 0:
                empty_neighbours.append(neighbour)

        # assign a score for the value of the move
        scores = []
        for empty in empty_neighbours:
            score = [empty, 0]
            # returns array of possible positions as offsets
            moves = self.generate_legal_moves(empty)
            for m in moves:
                # check the array of arrays against the array of moves by their index
                # if this position is blank (0) then make it the next move
                if self.board[m[0]][m[1]] == 0:
                    score[1] += 1
            scores.append(score)

        # this activates warnsdorffs_heuristic for greatly improved pathfinding speed
        if (wand == 1):
            # sort the moves in ascending order of closeness
            scores_sort = sorted(scores, key=lambda s: s[1])
            # return the list of moves, sorted by closeness
            sorted_neighbours = [s[0] for s in scores_sort]
        else:
            sorted_neighbours = empty_neighbours

        return sorted_neighbours

    def tour(self, n, path, to_visit, wand):
        """
        Recursive definition of knights tour. Inputs are as follows:
        n = current depth of search tree
        path = current path taken
        to_visit = node to visit
        """
        self.board[to_visit[0]][to_visit[1]
                                ] = n  # generate number of moves based on board size
        path.append(to_visit)  # first move is the coordinate passed in

        print("Visiting: ", to_visit)
        for i in range(size*size):
            visited.append(to_visit)

        if n == self.w * self.h:
            t1 = time.time()
            runtime = t1-t0
            self.print_board()
            print("N = ", size)
            print("Total Runtime: ", round(runtime, 2), "seconds")
            print("Path taken:\n", path)
            self.animate()
            wait = input("Press Enter to continue.")
            print("Done!")
            # sys.exit(1)

        else:
            sorted_neighbours = self.sort_lonely_neighbours(to_visit, wand)
            for neighbour in sorted_neighbours:  # start with the first move option
                # continue recursivelly calling function
                self.tour(n+1, path, neighbour, wand)

            # starting position is passed in through function
            self.board[to_visit[0]][to_visit[1]] = 0
            try:
                path.pop()  # retun up tree if at a dead end
                print("Going back to: ", path[-1])
            except IndexError:
                print("No path found")
                # sys.exit(1)


# execute the state space algorithm
kt = KnightsTour(size, size)  # width, height
path = []
t0 = time.time()
# starting depth of search tree, new path, starting coordinates, option to use warnsdorffs_heuristic
kt.tour(1, path, (0, 0), 1)

# todo: change to random starting point?
