import random


class MineField:
    class Square:
        """Class of one square in the field of mines. Each instance (as a part of one particular field) should
        be assigned a different pair of attribute '_col' and '_row', so that no two instances hold information
        about the same square.

        Other properties such as '_is_mine', '_is_flagged, '_is_revealed' and '_num_of_mines' are important for
        maintaining all the features of the game."""

        def __init__(self, col: int, row: int, is_mine=False):
            self._row = row
            self._col = col

            self._number = 0
            """It does not matter that a square that represents a mine has a non-zero number. We will never use
            the number because we first check whether a square is mine and in that case we no more need it. 
            Alternative implementation might consider number 9 as a sign that the particular square represents a mine, 
            but this one should save time as comparison of types bool is faster and we first have to check whether 
            square is a mine anyway."""

            self._is_mine = is_mine
            self._is_flagged = False
            """The flag is supposed to prevent the player to accidentally trigger a potential mine by mis-clicking."""

            self._is_revealed = False

        @property
        def number(self):
            return self._number

        @number.setter
        def number(self, value):
            self._number = value

        @property
        def is_mine(self):
            return self._is_mine

        @is_mine.setter
        def is_mine(self, value: bool):
            self._is_mine = value

        @property
        def is_flagged(self):
            return self._is_flagged

        @is_flagged.setter
        def is_flagged(self, value: bool):
            self._is_flagged = value

        @property
        def is_revealed(self):
            return self._is_revealed

        @is_revealed.setter
        def is_revealed(self, value: bool):
            self._is_revealed = value

    def __init__(self, number_of_columns: int, number_of_rows: int, number_of_mines: int, mines=None):
        """A constructor for a class that carries all the information about the current field of mines.
        If a player decides to change the size of the board, it might be the best to delete current instance
        and initialize a new one by calling the constructor. """

        self._num_of_columns = number_of_columns
        """Number of columns of the field of mines. """

        self._num_of_rows = number_of_rows
        """Number of rows of the field of mines. Can change, if the player decides to change the size of the board."""

        self._num_of_mines = number_of_mines

        self._mines = mines
        """List of mines. Each mine is a list of two integers - columns and row of the mine"""

        self._boom = False
        """Variable telling us whether the game is lost."""

        self._list_of_safe_squares = []
        """This list will contain all the squares that do not contain a mine. If square is revealed, it is also deleted
        from this list and when the list is empty the game is won."""

        # Initialize field of mines based on number of columns and rows that are parameters of the constructor.
        self.field = []
        """This list contains instances of squares of the mine field. It is a two dimensional list (each row is a list).
        """
        for col in range(number_of_columns):
            new_col = []
            for row in range(number_of_rows):
                new_col.append(self.Square(col=col, row=row))
                self._list_of_safe_squares.append([col, row])
            self.field.append(new_col)

        self._generate_mines() # Generate mines, which saves a list of mine coordinates into a list 'self._mines'.

        # Update the field based on where the mines were generated.
        for mine in self._mines:
            col = mine[0]
            row = mine[1]
            self.field[col][row].is_mine = True
            self._list_of_safe_squares.pop(self._list_of_safe_squares.index([col, row]))
            self._increment_neighbors(col, row)

    @property
    def number_of_mines(self):
        return self._num_of_mines

    @property
    def boom(self):
        return self._boom

    @boom.setter
    def boom(self, value: bool):
        self._boom = value

    def _generate_mines(self):
        """Generates list of mines -> self._mines."""
        self._mines = []
        while len(self._mines) < self._num_of_mines:
            x = random.randint(0, self._num_of_columns-1)
            y = random.randint(0, self._num_of_rows-1)
            if [x, y] not in self._mines:  # We do not want duplicate mines.
                self._mines.append([x, y])

    def get_dimensions(self):
        """Function called in UI - get the proportions of the minefield."""
        return self._num_of_columns, self._num_of_rows

    def _increment_neighbors(self, col, row):
        """
        Is called only in the constructor of this class. It increments attribute '_num_of_mines' of all neighboring
        squares.

        :param col: Column (x axis) of the mine, neighbors of which we want to increment.
        :param row: Row (y axis) of the mine, neighbors of which we want to increment.
        :return:
        """
        for c in range(max(col - 1, 0), min(col + 1, self._num_of_columns - 1)+1):
            for r in range(max(row - 1, 0), min(row + 1, self._num_of_rows - 1)+1):
                self.field[c][r].number += 1

    def toggle_flag(self, col: int, row: int):
        """This function makes a square flagged if it is not, and unflagged if it is flagged."""
        if self.field[col][row].is_flagged:
            self.field[col][row].is_flagged = False
            return
        self.field[col][row].is_flagged = True

    def check_win(self):
        """Returns whether the game should end because the player revealed all squares that are not a mine, or not."""
        if len(self._list_of_safe_squares) == 0:
            self.reveal_all()
            return True

        return False

    def reveal_all(self, only_mines=False):
        """Reveals every square, unless the parameter 'only_mines' is specified as 'True'. Then reveals only mines.
        :param only_mines: In case of losing, there is no need to reveal squares that do not contain mine.
        (Default: False)"""
        for mine in self._mines:
            self.field[mine[0]][mine[1]].is_revealed = True
        if only_mines: return

        for square in self._list_of_safe_squares:
            self.field[square[0]][square[1]].is_revealed = True

    def reveal(self, col: int, row: int):
        """This function represents a click on the square - reveals the square. If the square contains a mine,
        it is triggered by calling 'boom()'. If no neighbor is a mine (_num_of_mines == 0), the function calls itself
        with parameters of all the neighbors."""
        if self.field[col][row].is_revealed:
            return

        if self.field[col][row].is_mine:
            self.boom = True  # Game over
            self.reveal_all(only_mines=True)
            return

        # Remove a revealed square from list of unrevealed squares that are not a mine.
        self._list_of_safe_squares.pop(self._list_of_safe_squares.index([col, row]))
        self.field[col][row].is_revealed = True

        # If number is zero, reveal neighbors in recursive manner.
        if self.field[col][row].number == 0:
            for c in range(max(col - 1, 0), min(col + 1, self._num_of_columns - 1) + 1):
                for r in range(max(row - 1, 0), min(row + 1, self._num_of_rows - 1) + 1):
                    self.reveal(c, r)
