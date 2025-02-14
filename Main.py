import random
import time
from math import floor
from pygame import Vector2

#board will be nxn, queens will be an n sized list
n = 10

def main():
    #empty board
    board = [[0 for _ in range(n)] for _ in range(n)]
    show_board(board)

    #generate queens in random spots: place one queen per column at a random height
    queens = [Vector2(i, random.randint(0,n-1)) for i in range(n)]
    print(queens)

    #place the queens on the board
    for queen in queens:
        board[floor(queen.y)][floor(queen.x)] = 1
        show_board(board)

    #start algorithm
    res = min_conflicts(500, board, queens)
    if res is None: print("Non è stato possibile risolvere il CSP con questi steps")


def count_same_row_queens(queen, board):
    count = 0
    for cell in board[int(queen.y)]:
        if cell == 1: count += 1
    return count - 1 #don't count input queen


def count_same_column_queens(queen, board):
    count = 0
    for row in board:
        if row[int(queen.x)] == 1: count += 1
    return count - 1 #don't count input queen


def count_same_diagonal_queens(queen, board):
    count = 0
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 1 and (r - c == queen.y - queen.x):
                count += 1
    return count - 1 #don't count input queen


def count_same_antidiagonal_queens(queen, board):
    count = 0
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 1 and (r + c == queen.y + queen.x):
                count += 1
    return count - 1 #don't count input queen


def count_conflicts(queen, board):
    same_row = count_same_row_queens(queen, board)
    same_column = count_same_column_queens(queen, board) #might not be needed considering the heuristic
    same_diagonal = count_same_diagonal_queens(queen, board)
    same_antidiagonal = count_same_antidiagonal_queens(queen, board)
    return same_row + same_column + same_diagonal + same_antidiagonal


def update_conflicted(queens, board):
    return [queen for queen in queens if count_conflicts(queen, board) > 0]


def choose_new_position(queen, board):
    conflicts = {}
    min = None
    for i in range(len(board)):
        pos = (queen.x, i)
        amount_of_conflicts = count_conflicts(Vector2(pos[0], pos[1]), board)
        conflicts[pos] = amount_of_conflicts

        if min is None or conflicts[pos] < conflicts[min]:
            min = pos
    return Vector2(min[0], min[1])


def show_board(board):
    for row in board:
        print(row)
    print()


def min_conflicts(max_steps, board, queens):
    for i in range(max_steps):
        #goal check
        conflicted = update_conflicted(queens, board)
        if len(conflicted) == 0: return board

        #select a queen whose position causes a conflict
        queen = conflicted[random.randint(0, len(conflicted)-1)]

        #select the position for this queen that minimizes conflicts
        new_pos = choose_new_position(queen, board)

        #move the queen to that position
        old_pos = queen
        board[int(old_pos.y)][int(old_pos.x)] = 0
        queen.y = new_pos.y
        queen.x = new_pos.x
        board[int(new_pos.y)][int(new_pos.x)] = 1

        #show board at each step
        show_board(board)
        #time.sleep(1)
    return None

main()