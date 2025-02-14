import unittest
import Main

from pygame import Vector2

from Main import count_same_column_queens, count_same_diagonal_queens, count_same_antidiagonal_queens, count_conflicts, \
    count_same_row_queens, update_conflicted


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.queen = Vector2(2,2)

    def tearDown(self):
        self.board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

    def test_count_same_row_queens(self):
        count = count_same_row_queens(self.queen, self.board)
        self.assertEqual(count, 0)

        self.board[2][3] = 1
        count = count_same_row_queens(self.queen, self.board)
        self.assertEqual(count, 1)

        self.board[2][4] = 1
        count = count_same_row_queens(self.queen, self.board)
        self.assertEqual(count, 2)

    def test_count_same_column_queens(self):
        count = count_same_column_queens(self.queen, self.board)
        self.assertEqual(count, 0)

        self.board[4][2] = 1
        count = count_same_column_queens(self.queen, self.board)
        self.assertEqual(count, 1)

        self.board[3][2] = 1
        count = count_same_column_queens(self.queen, self.board)
        self.assertEqual(count, 2)

    def test_count_same_diagonal_queens(self):
        count = count_same_diagonal_queens(self.queen, self.board)
        self.assertEqual(count, 0)

        self.board[4][4] = 1
        count = count_same_diagonal_queens(self.queen, self.board)
        self.assertEqual(count, 1)

        self.board[3][3] = 1
        count = count_same_diagonal_queens(self.queen, self.board)
        self.assertEqual(count, 2)

    def test_count_same_antidiagonal_queens(self):
        count = count_same_antidiagonal_queens(self.queen, self.board)
        self.assertEqual(count, 0)

        self.board[4][0] = 1
        count = count_same_antidiagonal_queens(self.queen, self.board)
        self.assertEqual(count, 1)

        self.board[3][1] = 1
        count = count_same_antidiagonal_queens(self.queen, self.board)
        self.assertEqual(count, 2)

    def test_count_conflicts(self):
        board = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        count = count_conflicts(self.queen, board)
        self.assertEqual(count, 8)

    def test_update_conflicted(self):
        board = [
            [0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        queens = [Vector2(1,1), Vector2(3,3), Vector2(0,4)]
        conflicted = update_conflicted(queens, board)
        self.assertEqual(len(conflicted), 2)
        self.assertIn(Vector2(1,1), conflicted)
        self.assertIn(Vector2(3,3), conflicted)



if __name__ == '__main__':
    unittest.main()
