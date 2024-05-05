"""The primary module of the minesweeper game. This module is responsible
for starting the game
"""

from board import Board


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
