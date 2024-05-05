import random


class Spot(object):
    def __init__(self):
        self.is_selected = False
        self.is_mine = False
        self.count = 0

    def __str__(self):
        if self.is_selected:
            if self.is_mine:
                return "*"
            else:
                return str(self.count)
        else:
            return " "

    def is_mine(self):
        """Determines whether or not the board spot contains a mine.

        Returns:
            bool:  `True` if and only if the spot has a mine
        """
        return self.is_mine


class Board(object):
    def __init__(self, board_size, num_mines):
        self.board = [[Spot() for _ in range(board_size)] for _ in range(board_size)]
        self.boardSize = board_size
        self.numMines = num_mines
        # selectableSpots is the number of cells without a mine
        # when this is 0, the game is over and the minefield has been cleared
        self.selectableSpots = board_size * board_size - num_mines
        # lay m_numMines mines randomly on the board ...
        # taking care not to lay a mine on a cell that already has a mine
        # change: else case where i is reduced has been removed ...
        # as this causes infinite loops behaviour when the number of mines is relatively large
        i = 0
        while i < num_mines:
            x = random.randint(0, self.boardSize - 1)
            y = random.randint(0, self.boardSize - 1)
            if not self.board[x][y].is_mine:
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


def validate_coordinates_range(x, y, board_size):
    """Validate whether the (x, y) coordinates are in range.

    Args:
        x (int): the 'x' coordinate
        y (int): the 'y' coordinate
        board_size (int): the size of the board

    Returns:
        int, int: validated (x,y) coordinates
    """
    while x < 0 or x >= board_size or y < 0 or y >= board_size:
        print("Invalid coordinates. Please choose coordinates within the board range.")
        x = int(input("x: "))
        y = int(input("y: "))
    return x, y


def validate_unselected(x, y, board):
    """Validate whether the (x, y) coordinates denote an unselected location.

    Args:
        x (int): the 'x' coordinate
        y (int): the 'y' coordinate
        board (Board): board object

    Returns:
        int, int: validated (x,y) coordinates
    """
    while board[x][y].is_selected:
        print("Spot already selected. Please choose an unselected spot.")
        x = int(input("x: "))
        y = int(input("y: "))
    return x, y


def validate_board_width(width):
    """Validate the board width.

    Args:
        width (int): width of the board

    Returns:
        int: validated board width
    """
    while width < 3:
        print("Board width should be at least 3 for a playable game.")
        width = int(input("Choose the width of the board: "))
    return width


def validate_num_mines(num_mines, board_size):
    """Validate the number of mines requested.

    Args:
        num_mines (int): number of mines entered by the player
        board_size (int): size of the board

    Returns:
        int: validated number of mines
    """
    while num_mines >= board_size * board_size:
        print("Number of mines should be less than the total number of spots on the board.")
        num_mines = int(input("Choose the number of mines: "))
    return num_mines


def play_game():
    # Get the board width from user input and validate
    board_size = int(input("Choose the width of the board: "))
    board_size = validate_board_width(board_size)

    # Get the number of mines from user input and validate
    num_mines = int(input("Choose the number of mines: "))
    num_mines = validate_num_mines(num_mines, board_size)

    game_over = False
    winner = False

    board = Board(board_size, num_mines)
    while not game_over:
        print(board)
        print("Make your move:")
        # Get the (x, y) coordinates from user input and validate
        x = int(input("x: "))
        y = int(input("y: "))
        x, y = validate_coordinates_range(x, y, board_size)

        # Validate whether the spot at (x, y) is unselected
        x, y = validate_unselected(x, y, board.board)

        # Make the move
        board.make_move(x, y)
        game_over = board.hit_mine(x, y)
        if board.is_winner() and not game_over:
            game_over = True
            winner = True
    print(board)
    if winner:
        print("Congratulations, You Win!")
    else:
        print("You hit a mine, Game Over!")


if __name__ == "__main__":
    play_game()
