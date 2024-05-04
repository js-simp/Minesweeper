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

    def test_makeMove_no_mine_hit_center(self):
        """Test whether the `makeMove` function returns True when a mine has not been hit
        and it clears all locations around a cell that has no mines in neighbouring cells.
        """

        # Create a board with a mine at (0,0) and select a cell near the center
        board = boardClass(5, 0)
        board.addMine(0, 0)
        # Assert that makeMove returns True when the mine has not been hit
        self.assertTrue(board.makeMove(2, 2))
        board.makeMove(2, 2)

        # Assert that makeMove returns True and clears locations around a cell with no neighboring mines
        self.assertTrue(board.board[2][2].selected)
        self.assertTrue(board.board[0][2].selected)
        self.assertTrue(board.board[0][3].selected)
        self.assertTrue(board.board[0][4].selected)
        self.assertTrue(board.board[1][2].selected)
        self.assertTrue(board.board[1][3].selected)
        self.assertTrue(board.board[1][4].selected)
        self.assertTrue(board.board[2][0].selected)
        self.assertTrue(board.board[2][1].selected)
        self.assertTrue(board.board[2][3].selected)
        self.assertTrue(board.board[2][4].selected)
        self.assertTrue(board.board[3][0].selected)
        self.assertTrue(board.board[3][1].selected)
        self.assertTrue(board.board[3][2].selected)
        self.assertTrue(board.board[3][3].selected)
        self.assertTrue(board.board[3][4].selected)
        self.assertTrue(board.board[4][0].selected)
        self.assertTrue(board.board[4][1].selected)
        self.assertTrue(board.board[4][2].selected)
        self.assertTrue(board.board[4][3].selected)
        self.assertTrue(board.board[4][4].selected)

    def test_makeMove_no_mine_hit_edge(self):
        """Test whether the `makeMove` function works for a mine-free location
        at the edge of the board.
        """

        # Create a board with a mine at (2,2) and select a cell at the edge of the board
        board = boardClass(5, 0)
        board.addMine(2, 2)
        # Assert that makeMove returns True when the mine has not been hit
        self.assertTrue(board.makeMove(0, 2))
        board.makeMove(0, 2)

        # Assert that makeMove returns True and clears locations around a cell with no neighboring mines
        self.assertTrue(board.board[0][2].selected)
        self.assertTrue(board.board[0][0].selected)
        self.assertTrue(board.board[0][1].selected)
        self.assertTrue(board.board[0][3].selected)
        self.assertTrue(board.board[0][4].selected)
        self.assertTrue(board.board[1][0].selected)
        self.assertTrue(board.board[1][4].selected)
        self.assertTrue(board.board[2][0].selected)
        self.assertTrue(board.board[2][4].selected)
        self.assertTrue(board.board[3][0].selected)
        self.assertTrue(board.board[3][4].selected)
        self.assertTrue(board.board[4][0].selected)
        self.assertTrue(board.board[4][1].selected)
        self.assertTrue(board.board[4][2].selected)
        self.assertTrue(board.board[4][3].selected)
        self.assertTrue(board.board[4][4].selected)

    def test_str_empty_board(self):
        # Create a test board (no mines)
        board = boardClass(5, 0)

        # Define the expected output for an empty board
        expected_output = "  | 0 | 1 | 2 | 3 | 4\n" \
                          "-----------------------\n" \
                          "0 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "1 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "2 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "3 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "4 |  |  |  |  |  |\n" \
                          "-----------------------\n"

        # Assert that __str__ can draw an empty board
        self.assertEqual(str(board), expected_output)

    def test_str_after_selection(self):
        # Create a test board with no mines, make a move on an empty cell
        board = boardClass(5, 0)
        board.makeMove(2, 2)

        expected_output = "  | 0 | 1 | 2 | 3 | 4\n" \
                          "-----------------------\n" \
                          "0 | 0 | 0 | 0 | 0 | 0 |\n" \
                          "-----------------------\n" \
                          "1 | 0 | 0 | 0 | 0 | 0 |\n" \
                          "-----------------------\n" \
                          "2 | 0 | 0 | 0 | 0 | 0 |\n" \
                          "-----------------------\n" \
                          "3 | 0 | 0 | 0 | 0 | 0 |\n" \
                          "-----------------------\n" \
                          "4 | 0 | 0 | 0 | 0 | 0 |\n" \
                          "-----------------------\n"

        # Assert that __str__ can draw a board after a non-mine has been selected
        self.assertEqual(str(board), expected_output)

    def test_str_after_mine_hit(self):
        """Test whether the __str__ function can draw a board after a mine has been hit.
        """

        # Create a test board with a mine, then make a move on the mine
        board = boardClass(5, 0)
        board.addMine(2, 2)
        board.makeMove(2, 2)

        expected_output = "  | 0 | 1 | 2 | 3 | 4\n" \
                          "-----------------------\n" \
                          "0 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "1 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "2 |  |  | * |  |  |\n" \
                          "-----------------------\n" \
                          "3 |  |  |  |  |  |\n" \
                          "-----------------------\n" \
                          "4 |  |  |  |  |  |\n" \
                          "-----------------------\n"

        # Assert that __str__ can draw a board after a mine has been selected
        self.assertEqual(str(board), expected_output)


if __name__ == '__main__':
    unittest.main()
