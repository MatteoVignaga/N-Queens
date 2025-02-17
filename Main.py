import random
import time
from math import floor

import pygame
from pygame import Vector2
from win32api import mouse_event

#board will be nxn, queens will be an n sized list
n = 10
square_size = 600/n
max_steps = 1000
colors = {
    "GRAY": (200, 200, 200),
    "GREEN": (0, 100, 0),
    "BLACK": (70, 70, 70)
}

def generate_queens():
    return [Vector2(i, random.randint(0, n - 1)) for i in range(n)]


def place_queens(queens, board):
    for queen in queens:
        board[floor(queen.y)][floor(queen.x)] = 1


def reset():
    board = [[0 for _ in range(n)] for _ in range(n)]
    queens = generate_queens()
    place_queens(queens, board)
    return board, queens


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
    board_size = (600, 600)
    grid = pygame.Rect(0, 0, board_size[0], board_size[1])
    grid.center = (int(display.get_width() / 2), int(display.get_height() / 2))
    pygame.draw.rect(display, colors["BLACK"], grid, 3)

    for i in range(len(board)):
        for ii in range (len(board[i])):
            square = pygame.Rect(0, 0, square_size, square_size)
            square.topleft = (int(grid.topleft[0] + square_size*ii), int(grid.topleft[1] + square_size*i))
            if board[i][ii] == 1: pygame.draw.rect(display, colors["GREEN"], square)
            pygame.draw.rect(display, colors["BLACK"], square, 1)



def min_conflicts(max_steps, board, queens):
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
        board[int(old_pos.y)][int(old_pos.x)] = 0
        queen.y = new_pos.y
        queen.x = new_pos.x
        board[int(new_pos.y)][int(new_pos.x)] = 1

        #show board at each step
        display.fill(colors["GRAY"])
        show_board(board)
        pygame.display.flip()
        time.sleep(0.1)
    return None


def draw_start_button(button_rect):
    pygame.draw.rect(display, colors["BLACK"], button_rect, 3, 3)
    font = pygame.font.Font(None, 30)
    text = font.render("start", True, colors["BLACK"])
    display.blit(text, (button_rect.x + 25, button_rect.y + 10))


def draw_reset_button(button_rect):
    pygame.draw.rect(display, colors["BLACK"], button_rect, 3, 3)
    font = pygame.font.Font(None, 30)
    text = font.render("reset", True, colors["BLACK"])
    display.blit(text, (button_rect.x + 25, button_rect.y + 10))


def main():
    display.fill(colors["GRAY"])
    running = True
    clock = pygame.time.Clock()

    # empty board
    board = [[0 for _ in range(n)] for _ in range(n)]
    # generate queens in random spots: place one queen per column at a random height
    queens = generate_queens()
    # place the queens on the board
    place_queens(queens, board)

    #start button
    start_button_rect = pygame.Rect(20, 20, 100, 40)
    reset_button_rect = pygame.Rect(20, 80, 100, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    res = min_conflicts(max_steps, board, queens)
                    if res is None: print("The algorithm stopped without being able to solve the CSP.")
                if reset_button_rect.collidepoint(event.pos): board, queens = reset()

        display.fill(colors["GRAY"])
        show_board(board)
        draw_start_button(start_button_rect)
        draw_reset_button(reset_button_rect)
        pygame.display.flip()
        clock.tick(1)

pygame.init()
display = pygame.display.set_mode((900, 700))
main()