"""Module containing the `Spot` class.
"""


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


if __name__ == "__main__":
    pass
