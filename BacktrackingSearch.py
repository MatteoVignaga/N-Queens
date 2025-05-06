import heapq
import time
from utils import *


class BacktrackingSearch:

    def __init__(self, board, constraints_board, n, display):
        self.n = n
        self.board = board
        self.constraints_board = constraints_board
        self.display = display


    def solve(self):
        return self.backtrack(self.board, self.constraints_board, 0)


    def backtrack(self, board, constraints_board, counter):
        # did we place all the queens?
        if counter == self.n: return True

        available_cells = self.generate_available_cells()

        while len(available_cells) > 0:
            _, next_cell = heapq.heappop(available_cells)
            next_cell = Vector2(next_cell[0], next_cell[1])

            # constraint propagation
            place_queens([next_cell], self.board)
            lock_cells(self.constraints_board, next_cell)
            counter += 1

            # show board at each step
            self.display.fill(colors["GRAY"])
            draw_board(board, constraints_board, self.display)
            pygame.display.flip()
            time.sleep(0.001)

            res = self.backtrack(self.board, self.constraints_board, counter)
            if res: return res

            # undo constraint propagation
            board[floor(next_cell.y)][floor(next_cell.x)] = 0
            unlock_cells(self.constraints_board, next_cell)
            counter -= 1

            # show board at each step
            self.display.fill(colors["GRAY"])
            draw_board(board, constraints_board, self.display)
            pygame.display.flip()
            time.sleep(0.001)

        return False


    def generate_available_cells(self):
        # available cells is a max heap that contains each available cell
        # ordered by how many cells would be available after placing a queen
        # there, following the least constraining value heuristic.
        # PS: standard heapq is a minheap, so we negate the count
        # to adjust the behavior to act as a max heap
        heap = []
        for i in range(self.n):
            for ii in range(self.n):
                if self.board[i][ii] == 0 and self.constraints_board[i][ii] == 0:
                    cell = Vector2(ii, i)
                    priority = self.count_remaining_cells(cell)
                    cell = (ii, i) #convert to tuple for the heap
                    heapq.heappush(heap, (-priority, cell))
        return heap


    def count_remaining_cells(self, cell):
        # setup: act like you're placing the queen there, locking all the other cells
        lock_cells(self.constraints_board, cell)

        # count the remaining available cells
        count = 0
        for i in range(self.n):
            for ii in range(self.n):
                if self.constraints_board[i][ii] == 0: count+=1

        # teardown: unlock the cells like no queen was ever placed
        unlock_cells(self.constraints_board, cell)

        return count

