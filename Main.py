import random
import string
import time

import pygame
from pygame import Vector2

from BacktrackingSearch import BacktrackingSearch
from utils import *

#board will be nxn, queens will be an n sized list
#queens are represented as a couple (x,y) representing their coordinates

max_steps = 1000

#queens are represented by x-column and y-row coordinates
def generate_queens():
    return [Vector2(i, random.randint(0, n - 1)) for i in range(n)]


def reset():
    board = [[0 for _ in range(n)] for _ in range(n)]
    constraints_board = [[0 for _ in range(n)] for _ in range(n)]
    queens = generate_queens()
    place_queens(queens, board)
    for queen in queens:
        lock_cells(constraints_board, queen)
    return board, constraints_board, queens


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


def min_conflicts(max_steps, board, constraints_board):
    # generate queens in random spots: place one queen per column at a random height
    queens = generate_queens()
    # place the queens on the board
    place_queens(queens, board)
    for queen in queens:
        lock_cells(constraints_board, queen)
    time.sleep(0.1)

    #solve
    for i in range(max_steps):
        #goal check
        conflicted = update_conflicted(queens, board)
        if len(conflicted) == 0: return board

        #select a queen whose position causes a conflict
        queen = random.choice(conflicted)

        #select the position for this queen that minimizes conflicts
        new_pos = choose_new_position(queen, board)

        #move the queen to that position
        old_pos = queen
        unlock_cells(constraints_board, old_pos)
        board[int(old_pos.y)][int(old_pos.x)] = 0
        queen.y = new_pos.y
        queen.x = new_pos.x
        board[int(new_pos.y)][int(new_pos.x)] = 1
        lock_cells(constraints_board, new_pos)

        #show board at each step
        display.fill(colors["GRAY"])
        draw_board(board, constraints_board, display)
        pygame.display.flip()
        time.sleep(0.1)
    return None


def draw_start_button(button_rect, label: string):
    pygame.draw.rect(display, colors["BLACK"], button_rect, 3, 3)
    font = pygame.font.Font(None, 25)
    text = font.render(label, True, colors["BLACK"])
    display.blit(text, (button_rect.x + 10, button_rect.y + 10))


def draw_reset_button(button_rect):
    pygame.draw.rect(display, colors["BLACK"], button_rect, 3, 3)
    font = pygame.font.Font(None, 25)
    text = font.render("reset", True, colors["BLACK"])
    display.blit(text, (button_rect.x + 25, button_rect.y + 10))


def main():
    display.fill(colors["GRAY"])
    running = True
    clock = pygame.time.Clock()

    # empty board
    board = [[0 for _ in range(n)] for _ in range(n)] #board to place queens on
    constraints_board = [[0 for _ in range(n)] for _ in range(n)] #board to show locked cells

    #start button
    start_minconflicts_button_rect = pygame.Rect(20, 50, 200, 40)
    start_backtracking_search_button_rect = pygame.Rect(20, 110, 200, 40)
    reset_button_rect = pygame.Rect(20, 170, 200, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_minconflicts_button_rect.collidepoint(event.pos):
                    res = min_conflicts(max_steps, board, constraints_board)
                    if res is None: print("The algorithm stopped without being able to solve the CSP.")
                if start_backtracking_search_button_rect.collidepoint(event.pos):
                    algorithm = BacktrackingSearch(board, constraints_board, n, display)
                    res = algorithm.solve()
                    if not res: print("The algorithm stopped without being able to solve the CSP.")
                if reset_button_rect.collidepoint(event.pos): board, constraints_board, queens = reset()

        display.fill(colors["GRAY"])
        draw_board(board, constraints_board, display)
        draw_start_button(start_minconflicts_button_rect, "minconflicts")
        draw_start_button(start_backtracking_search_button_rect, "backtracking search")
        #draw_reset_button(reset_button_rect)
        pygame.display.flip()
        clock.tick(1)

pygame.init()
display = pygame.display.set_mode((900, 700))
main()