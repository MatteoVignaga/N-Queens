import time
from utils import *

class MinConflicts:

    def __init__(self, board, constraints_board, n, display, max_steps):
        self.n = n
        self.board = board
        self.constraints_board = constraints_board
        self.display = display
        self.max_steps = max_steps

    def solve(self):
        # generate queens in random spots: place one queen per column at a random height
        queens = generate_queens()
        # place the queens on the board
        place_queens(queens, self.board)
        for queen in queens:
            lock_cells(self.constraints_board, queen)
        time.sleep(0.1)

        #solve
        for i in range(self.max_steps):
            #goal check
            conflicted = self.update_conflicted(queens, self.board)
            if len(conflicted) == 0: return self.board

            #select a queen whose position causes a conflict
            queen = random.choice(conflicted)

            #select the position for this queen that minimizes conflicts
            new_pos = self.choose_new_position(queen, self.board)

            #move the queen to that position
            old_pos = queen
            unlock_cells(self.constraints_board, old_pos)
            self.board[int(old_pos.y)][int(old_pos.x)] = 0
            queen.y = new_pos.y
            queen.x = new_pos.x
            self.board[int(new_pos.y)][int(new_pos.x)] = 1
            lock_cells(self.constraints_board, new_pos)

            #show board at each step
            self.display.fill(colors["GRAY"])
            draw_board(self.board, self.constraints_board, self.display)
            pygame.display.flip()
            time.sleep(0.1)
        return None


    def update_conflicted(self, queens, board):
        return [queen for queen in queens if self.count_conflicts(queen, board) > 0]


    def count_conflicts(self, queen, board):
        same_row = self.count_same_row_queens(queen, board)
        same_column = self.count_same_column_queens(queen, board) #might not be needed considering the heuristic
        same_diagonal = self.count_same_diagonal_queens(queen, board)
        same_antidiagonal = self.count_same_antidiagonal_queens(queen, board)
        return same_row + same_column + same_diagonal + same_antidiagonal


    def count_same_row_queens(self, queen, board):
        count = 0
        for cell in board[int(queen.y)]:
            if cell == 1: count += 1
        return count - 1  # don't count input queen


    def count_same_column_queens(self, queen, board):
        count = 0
        for row in board:
            if row[int(queen.x)] == 1: count += 1
        return count - 1  # don't count input queen


    def count_same_diagonal_queens(self, queen, board):
        count = 0
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 1 and (r - c == queen.y - queen.x):
                    count += 1
        return count - 1  # don't count input queen


    def count_same_antidiagonal_queens(self, queen, board):
        count = 0
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == 1 and (r + c == queen.y + queen.x):
                    count += 1
        return count - 1  # don't count input queen


    def choose_new_position(self, queen, board):
        conflicts = {}
        min = None
        for i in range(len(board)):
            pos = (queen.x, i)
            amount_of_conflicts = self.count_conflicts(Vector2(pos[0], pos[1]), board)
            conflicts[pos] = amount_of_conflicts

            if min is None or conflicts[pos] < conflicts[min]:
                min = pos
        return Vector2(min[0], min[1])