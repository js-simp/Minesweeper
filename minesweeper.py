import random

# criticism: the prefix board is redundant
class boardSpot(object):
    # criticism: these three class variables are redundant
    value = 0
    selected = False
    mine = False
    def __init__(self):
        self.selected = False
    def __str__(self):
        # criticism: value is a poor uninformative variable name
        return str(boardSpot.value)
    def isMine(self):
        """
        Determines whether or not the board spot contains a mine
        :return: True if and only if the spot has a mine
        """
        # criticism: -1 is a magic number
        # criticism: this function should be written more compactly in any case
        if boardSpot.value == -1:
            return True
        return False
# criticism: the suffix Class is redundant
class boardClass(object):
    # criticism: the convention of using prefix m_ to indicate method parameters is no longer used
    def __init__(self, m_boardSize, m_numMines):
        self.board = [[boardSpot() for i in range(m_boardSize)] for j in range(m_boardSize)]
        self.boardSize = m_boardSize
        self.numMines = m_numMines
        # selectableSpots is the number of cells without a mine
        # when this is 0, the game is over and the mine field has been cleared
        self.selectableSpots = m_boardSize * m_boardSize - m_numMines
        # lay m_numMines mines randomly on the board ...
        # taking care not to lay a mine on a cell that already has a mine
        # change: else case where i is reduced has been removed ...
        # as this causes infinite loops behaviour when the number of mines is relatively large
        i=0
        while i < m_numMines:
            x = random.randint(0, self.boardSize-1)
            y = random.randint(0, self.boardSize-1)
            if not self.board[x][y].mine:
                self.addMine(x, y)
                i += 1
    def __str__(self):
        # make divider be 3 -s plus 4 -s for each cell
        # with a new line both before and after the divider
        # make returnString be a row labelling each column followed by a divider
        returnString = " "
        divider = "\n---"

        for i in range(0, self.boardSize):
            returnString += " | " + str(i)
            divider += "----"
        divider += "\n"
        returnString += divider
        # for each row of the table, add onto the return string ...
        # the number of the row and a representation for each cell (then right edge and divider)
        # which is * for a selected cell with a mine, blank for an unselected cell
        # and otherwise (selected cell without mine) the number of neighbours with mines
        # change: -1 has been replaced with * as it is more visually attractive
        # criticism: displaying the cell should be the responsibility of boardSpot
        for y in range(0, self.boardSize):
            returnString += str(y)
            for x in range(0, self.boardSize):
                if self.board[x][y].mine and self.board[x][y].selected:
                    returnString += " |" + " *"
                elif self.board[x][y].selected:
                    returnString += " | " + str(self.board[x][y].value)
                else:
                    returnString += " | "
            returnString += " |"
            returnString += divider
        return returnString
    def addMine(self, x, y):
        """
        add a mine to the board at the requested coordinate
        :param x: the x-component of the coordinate
        :param y: the y-component of the coordinate
        :return: no value is returned"""
        self.board[x][y].value = -1
        self.board[x][y].mine = True
        # examine cells to the left, middle and right, relative to (x,y)
        for i in range(x-1, x+2):
            # make sure cell is not too far to the left or right
            if i >= 0 and i < self.boardSize:
                # if the three cells above (x,y) are on the board and not mines, increment their value
                if y-1 >= 0 and not self.board[i][y-1].mine:
                     self.board[i][y-1].value += 1
        # if the three cells below (x,y) are on the board and not mines, increment their value
                if y+1 < self.boardSize and not self.board[i][y+1].mine:
                    self.board[i][y+1].value += 1
                # if cell to the left of (x,y) is on the board and not a mine, increment its value
        if x-1 >= 0 and not self.board[x-1][y].mine:
            self.board[x-1][y].value += 1
                # if cell to the of (x,y) right is on the board and not a mine, increment its value
        if x+1 < self.boardSize and not self.board[x+1][y].mine:
            self.board[x+1][y].value += 1
    def makeMove(self, x, y):
        """
        step on the cell at the requested component and reveal whether the player is still alive
        :param x: the x-component of the component
        :param y: the y-component of the coordinate
        :return: True if and only if (x,y) did not have a mine
        """
        # select the cell and return false if a mine has been stepped on (all other paths return True)
        self.board[x][y].selected = True
        self.selectableSpots -= 1
        if self.board[x][y].value == -1:
            return False
        # if there are no mines around (x,y)
        if self.board[x][y].value == 0:
            # examine cells to the left, centre and right of (x,y)
            for i in range(x-1, x+2):
                # make sure cell is not too far to the left or right
                if i >= 0 and i < self.boardSize:
                    # if the three cells above (x,y) are on the board and not selected, visit them
                    if y-1 >= 0 and not self.board[i][y-1].selected:
                        self.makeMove(i, y-1)
                    # if the three cells below (x,y) are on the board and not selected, visit them
                    if y+1 < self.boardSize and not self.board[i][y+1].selected:
                        self.makeMove(i, y+1)
                # if the cell to the left of (x,y) is on the board and not selected, visit it
            if x-1 >= 0 and not self.board[x-1][y].selected:
                self.makeMove(x-1, y)
                # if the cell to the right of (x,y) is on the board and not selected, visit it
            if x+1 < self.boardSize and not self.board[x+1][y].selected:
                self.makeMove(x+1, y)
        # only False case is when value is -1 and that was detailed above
            return True
        else:
            return True
    def hitMine(self, x, y):
        """
        reveals whether a particular location holds a mine
        :param x: the x-component of the location
        :param y: the y-component of the location
        :return: True if and only if (x,y) is a mine
        """
        return self.board[x][y].value == -1
    def isWinner(self):
        """
        reveals whether the player has won
        :return: True if and only if the player has won
        """
        return self.selectableSpots == 0
    def nearby_coords_of(self, x, y):
        """
        gives the list of all valid nearby coordinates
        :param x: the x component of the coordinate
        :param y: the y component of the coordinate
        :return: the list of coordinates adjacent to or diagonally next to the given coordinate that
        are also on the board
        suitable tests for board of width at least 3 would be:
        self.assertEqual ( board.nearby_coords_of(1,1) ,
        [(0,0), (0, 1), (0, 2), (1, 0), (1, 2), (2,0), (2,1), (2, 2) ] )
        self.assertEqual ( board.nearby_coords_of(0,0) ,
        [(0,1), (1,0), (1,1)] )
        """
        pass

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
        board (boardClass): board object

    Returns:
        int, int: validated (x,y) coordinates
    """
    while board[x][y].selected:
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


def playGame():
    # Get the board width from user input and validate
    board_size = int(input("Choose the width of the board: "))
    board_size = validate_board_width(board_size)

    # Get the number of mines from user input and validate
    num_mines = int(input("Choose the number of mines: "))
    num_mines = validate_num_mines(num_mines, board_size)

    game_over = False
    winner = False

    board = boardClass(board_size, num_mines)
    while not game_over:
        print(board)
        print("Make your move:")
        # Get the (x, y) coordinates from user input and validate
        x = int(input("x: "))
        y = int(input("y: "))
        x, y = validate_coordinates_range(x, y, board_size)

        # Validate whether the spot at (x, y) is unselected
        x, y = validate_unselected(x, y, board.board)

        #Make the move
        board.makeMove(x, y)
        game_over = board.hitMine(x, y)
        if board.isWinner() and game_over == False:
            game_over = True
            winner = True
    print(board)
    if winner:
        print("Congratulations, You Win!")
    else:
        print("You hit a mine, Game Over!")
if __name__ == "__main__":
    playGame()