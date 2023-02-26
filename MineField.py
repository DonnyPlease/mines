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

            self._num_of_mines = 0
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
            return self._num_of_mines

        @number.setter
        def number(self, value):
            self._num_of_mines = value

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

    def __init__(self, number_of_columns: int, number_of_rows: int, mines=None):
        """Constructor for a class that carries oll the information about the current field of mines.
        If a player decides to change the size of the board, it might be best to delete current instance
        and initialize a new one by calling the constructor. """

        self._num_of_columns = number_of_columns
        """Number of columns of the field of mines. """

        self._num_of_rows = number_of_rows
        """Number of rows of the field of mines. Can change, if the player decides to change the size of the board."""

        self._mines = mines
        """List of mines. Each mine is a list of two integers - columns and row of the mine"""

        # Initialize field of mines based on number of columns and rows that are parameters of the constructor.
        self.field = []
        for row in range(number_of_rows):
            new_row = []
            for col in range(number_of_columns):
                new_row.append(self.Square(col=col, row=row))
            self.field.append(new_row)

        # Set squares as mines the parameter 'mines' is
        if self._mines is None:
            self._mines = []
        for mine in self._mines:
            col = mine[0]
            row = mine[1]
            self.field[col][row].is_mine = True
            self._increment_neighbors(col, row)

    def _increment_neighbors(self, col, row):
        """
        Is called only in the constructor of this class. It increments attribute '_num_of_mines' of all neighboring
        squares.

        :param col: Column (x axis) of the mine, neighbors of which we want to increment.
        :param row: Row (y axis) of the mine, neighbors of which we want to increment.
        :return:
        """
        for c in range(max(col - 1, 0), min(col + 1, self._num_of_columns - 1)):
            for r in range(max(row - 1, 0), min(row + 1, self._num_of_rows - 1)):
                self.field[c][r].number += 1

    def flag(self, col: int, row: int):
        self.field[col][row].is_flagged = True

    def unflag(self, col: int, row: int):
        self.field[col][row].is_flagged = False

    def boom(self):
        # TO DO: implement this function.
        """Game over."""
        pass

    def reveal(self, col: int, row: int):
        """This function represents a click on the square - reveals the square. If the square contains a mine,
        it is triggered by calling 'boom()'. If no neighbor is a mine (_num_of_mines == 0), the function calls itself
        with parameters of all the neighbors."""
        if not self.field[col][row].is_revealed:
            return

        if self.field[col][row].is_mine:
            self.boom()

        self.field[col][row].is_revealed = True

        if self.field[col][row].number == 0:
            for c in range(max(col - 1, 0), min(col + 1, self._num_of_columns - 1) + 1):
                for r in range(max(row - 1, 0), min(row + 1, self._num_of_rows - 1) + 1):
                    self.reveal(c, r)
