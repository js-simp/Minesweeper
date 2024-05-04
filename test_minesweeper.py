import unittest
from minesweeper import boardClass

class TestMinesweeper(unittest.TestCase):
    def test_addMine(self):
        """Test whether the `addMine` function adds a mine in the specified place
        and increases the value stored at every neighbouring cell.
        """
        # Create a test board without any mines
        board = boardClass(5, 0)

        # Add a mine at position (2, 2)
        board.addMine(2, 2)

        # Assert that the value at (2, 2) is -1 (mine)
        self.assertEqual(board.board[2][2].value, -1)

        # Assert that the values of neighboring cells are incremented by 1
        self.assertEqual(board.board[1][1].value, 1)
        self.assertEqual(board.board[1][2].value, 1)
        self.assertEqual(board.board[1][3].value, 1)
        self.assertEqual(board.board[2][1].value, 1)
        self.assertEqual(board.board[2][3].value, 1)
        self.assertEqual(board.board[3][1].value, 1)
        self.assertEqual(board.board[3][2].value, 1)
        self.assertEqual(board.board[3][3].value, 1)

    def test_makeMove_mine_hit(self):
        """Test whether the `makeMove` function returns false when a mine is hit.
        """

        # Create test board and add a mine at position (2, 2)
        board = boardClass(5, 0)
        board.addMine(2, 2)

        # Assert that makeMove returns False when hitting a mine
        self.assertFalse(board.makeMove(2, 2))

if __name__ == '__main__':
    unittest.main()
