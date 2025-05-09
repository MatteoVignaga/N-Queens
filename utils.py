from math import floor

import pygame
import random
from pygame import Vector2

# board will be nxn, queens will be an n sized list
# queens are represented as a 2D vector (x,y) representing their coordinates
n = 30                              # board size
square_size = 600/n                 # single cell size
max_steps = 1000                    # iteration limit for MinConflicts
delay = 0.001                         # time delay for each step of algorithms
colors = {
    "GRAY": (200, 200, 200),        # background color
    "GREEN": (0, 100, 0),           # queen position color
    "BLACK": (70, 70, 70),          # border color
    "LOCK GRAY": (180, 180, 180)    # constraints visualization color
}

def reset(display):
    board = [[0 for _ in range(n)] for _ in range(n)]
    constraints_board = [[0 for _ in range(n)] for _ in range(n)]
    draw_board(board, constraints_board, display)
    return board, constraints_board

# queens are represented by x-column and y-row coordinates
def generate_queens():
    return [Vector2(i, random.randint(0, n - 1)) for i in range(n)]

#board is printed row by row!
def place_queens(queens, board):
    for queen in queens:
        board[floor(queen.y)][floor(queen.x)] = 1


def lock_same_row(constraints_board, queen):
    row_index = int(queen.y)
    for col_index in range(len(constraints_board[row_index])):
        constraints_board[row_index][col_index] -= 1


def lock_same_column(constraints_board, queen):
    col_index = int(queen.x)
    for row_index in range(len(constraints_board)):
        constraints_board[row_index][col_index] -= 1


def lock_same_diagonal_and_antidiagonal(constraints_board, queen):
    for r in range(len(constraints_board)):
        for c in range(len(constraints_board)):
            if (r - c == queen.y - queen.x) or (r + c == queen.y + queen.x):
                constraints_board[r][c] -= 1


def lock_cells(constraints_board, queen):
    lock_same_row(constraints_board, queen)
    lock_same_column(constraints_board, queen)
    lock_same_diagonal_and_antidiagonal(constraints_board, queen)


def unlock_same_row(constraints_board, queen):
    row_index = int(queen.y)
    for col_index in range(len(constraints_board[row_index])):
        constraints_board[row_index][col_index] += 1


def unlock_same_column(constraints_board, queen):
    col_index = int(queen.x)
    for row_index in range(len(constraints_board)):
        constraints_board[row_index][col_index] += 1


def unlock_same_diagonal_and_antidiagonal(constraints_board, queen):
    for r in range(len(constraints_board)):
        for c in range(len(constraints_board)):
            if (r - c == queen.y - queen.x) or (r + c == queen.y + queen.x):
                constraints_board[r][c] += 1


def unlock_cells(constraints_board, queen):
    unlock_same_row(constraints_board, queen)
    unlock_same_column(constraints_board, queen)
    unlock_same_diagonal_and_antidiagonal(constraints_board, queen)


def draw_board(board, constraints_board, display):
    board_size = (600, 600)
    grid = pygame.Rect(0, 0, board_size[0], board_size[1])
    grid.center = (int(display.get_width() / 2) + 100, int(display.get_height() / 2))

    for i in range(len(board)):
        for ii in range (len(board[i])):
            square = pygame.Rect(0, 0, square_size, square_size)
            square.topleft = (int(grid.topleft[0] + square_size*ii), int(grid.topleft[1] + square_size*i))
            if board[i][ii] == 1:
                pygame.draw.rect(display, colors["GREEN"], square)
            elif constraints_board[i][ii] < 0:
                pygame.draw.rect(display, colors["LOCK GRAY"], square)
            pygame.draw.rect(display, colors["BLACK"], square, 1)

    pygame.draw.rect(display, colors["BLACK"], grid, 3)
