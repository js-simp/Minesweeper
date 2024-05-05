"""Module containing the `Board` class.
"""

import random
from spot import Spot


class Board:
    def __init__(self, board_size, num_mines):
        self.board = [[Spot() for _ in range(board_size)] for _ in range(board_size)]
        self.boardSize = board_size
        self.numMines = num_mines
        # selectableSpots is the number of cells without a mine
        # when this is 0, the game is over and the minefield has been cleared
        self.selectableSpots = board_size * board_size - num_mines
        # lay num_mines mines randomly on the board ...
        # taking care not to lay a mine on a cell that already has a mine
        i = 0
        while i < num_mines:
            x = random.randint(0, self.boardSize - 1)
            y = random.randint(0, self.boardSize - 1)
            # Check if the spot is not already a mine
            if not self.board[x][y].is_mine:
                # Add a mine and update neighboring spots
                self.add_mine(x, y)
                i += 1

    def __str__(self):
        """Returns a string representation of the board.

        Returns:
            str:  string representation of the board
        """
        return_string = self._generate_column_headings()
        divider = self._generate_divider()

        for y in range(self.boardSize):
            return_string += str(y)
            for x in range(self.boardSize):
                return_string += " | " + str(self.board[x][y])
            return_string += " |" + divider

        return return_string

    def _generate_divider(self):
        """Generates a string representing the divider between rows.

        Returns:
            str:  the divider between rows
        """
        divider = "\n---"
        for i in range(self.boardSize):
            divider += "----"
        divider += "\n"
        return divider

    def _generate_column_headings(self):
        """Generates a string representing the column headings.

        Returns:
            str:  string representation of the column headings
        """
        column_headings = " "
        divider = self._generate_divider()
        for i in range(self.boardSize):
            column_headings += " | " + str(i)
        column_headings += divider
        return column_headings

    def add_mine(self, x, y):
        """
        Add a mine to the board at the specified coordinate and update neighboring cells.

        Args:
            x (int): The x-component of the coordinate.
            y (int): The y-component of the coordinate.

        Returns:
            None
        """

        # Set the value of the spot at (x, y) to indicate a mine
        self.board[x][y].count = -1
        self.board[x][y].is_mine = True

        # Get coordinates of neighboring cells around (x, y)
        nearby_coords = self.nearby_coords_of(x, y)

        # Increment the value of neighboring cells that are not mines
        for nx, ny in nearby_coords:
            if not self.board[nx][ny].is_mine:
                self.board[nx][ny].count += 1

    def make_move(self, x, y):
        """Step on the cell at the requested component and reveal whether the player is still alive.

        Args:
            x (int): The 'x' coordinate.
            y (int): The 'y' coordinate.

        Returns:
            bool: True if and only if (x, y) did not have a mine.
        """
        # Select the cell
        self.board[x][y].is_selected = True
        self.selectableSpots -= 1

        # If the cell is a mine, return false
        if self.board[x][y].count == -1:
            return False

        # If the cell has no neighboring mines, recursively visit neighboring cells
        if self.board[x][y].count == 0:
            # Get neighboring coordinates
            nearby_coords = self.nearby_coords_of(x, y)
            # Visit each neighboring cell
            for nx, ny in nearby_coords:
                # Visit the cell only if it's within the board boundaries and not already selected
                if 0 <= nx < self.boardSize and 0 <= ny < self.boardSize and not self.board[nx][ny].is_selected:
                    self.make_move(nx, ny)

            # If the cell is not a mine and not empty, return true
            return True
        else:
            return True

    def hit_mine(self, x, y):
        """
        reveals whether a particular location holds a mine
        :param x: the x-component of the location
        :param y: the y-component of the location
        :return: True if and only if (x,y) is a mine
        """
        return self.board[x][y].count == -1

    def is_winner(self):
        """
        reveals whether the player has won
        :return: True if and only if the player has won
        """
        return self.selectableSpots == 0

    def nearby_coords_of(self, x, y):
        """Gives the list of all valid nearby coordinates.

        Args:
            x (int): The 'x' coordinate
            y (int): The 'y' coordinate

        Returns:
            list(tuple): List of coordinates adjacent to or diagonally next to
            the given coordinate that are also on the board.
        """
        nearby_coords = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (dx, dy) != (0, 0) and 0 <= nx < self.boardSize and 0 <= ny < self.boardSize:
                    nearby_coords.append((nx, ny))
        return nearby_coords


if __name__ == "__main__":
    pass
