import tkinter
import tkinter.ttk
import MineField
from PIL import Image, ImageTk


class UI:
    # Set parameters for size of one grid edge
    _row_size = 25
    _col_size = 25

    def __init__(self, Field):
        self.root = tkinter.Tk()
        self.root.title('Mines')

        # Menu
        self._menubar = tkinter.Menu(self.root)

        self._game_menu = tkinter.Menu(self._menubar, tearoff=0)
        self._game_menu.add_command(label="Reset", command=self.reset, accelerator="F5")
        self._game_menu.add_separator()
        self._game_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        self._menubar.add_cascade(label="Game", menu=self._game_menu)

        self._settings = tkinter.Menu(self._menubar, tearoff=0)
        self._settings.add_command(label="Default settings")
        self._settings.add_command(label="Customize")
        self._menubar.add_cascade(label="Options", menu=self._settings)

        self._helpmenu = tkinter.Menu(self._menubar, tearoff=0)
        self._helpmenu.add_command(label="Help Index")
        self._helpmenu.add_command(label="About...")
        self._menubar.add_cascade(label="Help", menu=self._helpmenu)

        self.root.config(menu=self._menubar)

        self.root.bind_all("<Control-q>", lambda event: self.root.quit())
        self.root.bind_all("<F5>", lambda event: self.reset())

        self.Field = Field

        self._number_of_columns, self._number_of_rows = self.Field.get_dimensions()
        self._number_of_mines = self.Field.number_of_mines

        # Set up the canvas of the field
        self._width_of_canvas = self._number_of_columns * self._col_size + 1
        self._height_of_canvas = self._number_of_rows * self._row_size + 1
        self._canvas_field = tkinter.Canvas(self.root, width=self._width_of_canvas, height=self._height_of_canvas,
                                            background='white')
        self._canvas_field.grid(column=0, row=1)
        self._canvas_field.bind("<Button-1>", self.reveal)
        self._canvas_field.bind("<Button-3>", self.toggle_flag)

        self._canvas_info = tkinter.Canvas(self.root, width=self._width_of_canvas, height=40)
        self._canvas_info.grid(column=0, row=0)

        self.unrevealed_img = (Image.open("tile_square2.png"))
        self.resized_unrevealed_img = self.unrevealed_img.resize((24, 24), Image.ANTIALIAS)
        self.unrevealed_image = ImageTk.PhotoImage(self.resized_unrevealed_img)

        self.flagged_img = (Image.open("tile_square_flagged.png"))
        self.resized_flagged_img = self.flagged_img.resize((24, 24), Image.ANTIALIAS)
        self.flagged_image = ImageTk.PhotoImage(self.resized_flagged_img)

        self.draw()

    def reset(self):
        del self.Field
        self.Field = MineField.MineField(self._number_of_columns, self._number_of_rows, self._number_of_mines)
        self.draw()

    def reveal(self, event):
        if self.Field.boom or self.Field.check_win(): return
        col = (event.x-1) // self._row_size
        row = (event.y-1) // self._col_size

        if self.Field.field[col][row].is_flagged: return
        self.Field.reveal(col=col, row=row)

        self.draw()

    def toggle_flag(self, event):
        if self.Field.boom or self.Field.check_win(): return
        col = event.x // self._row_size
        row = event.y // self._col_size
        if self.Field.field[col][row].is_revealed: return
        self.Field.toggle_flag(col=col, row=row)
        self.draw()

    def draw_info(self):
        self._canvas_info.delete('all')
        if self.Field.boom:
            self._canvas_info.create_text(80, 20, text="You lost!!", fill="black",
                                          font='Helvetica 14 bold')
            return

        if self.Field.check_win():
            self._canvas_info.create_text(80, 20, text="You Won!!", fill="black",
                                          font='Helvetica 14 bold')
            return

        self._canvas_info.create_text(80, 20, text="Mines to find: " + str(self.Field.number_of_mines), fill="black",
                                      font='Helvetica 14 bold')

    def _draw_grid(self):
        sizeX = self._width_of_canvas
        sizeY = self._height_of_canvas
        for i in range(self._number_of_rows + 1):
            self._canvas_field.create_line(0, i * self._col_size + 1, sizeX + 1, i * self._col_size + 1,
                                           fill='black', width=1)
        for j in range(self._number_of_columns + 1):
            self._canvas_field.create_line(j * self._row_size + 1, 0, j * self._row_size + 1, sizeY + 1,
                                           fill='black', width=1)

    def _draw_insides(self):
        for row in range(self._number_of_rows):
            for col in range(self._number_of_columns):

                if not self.Field.field[col][row].is_revealed:
                    self._canvas_field.create_image(col * self._row_size + 2, row * self._col_size + 2, anchor="nw",
                                                    image=self.unrevealed_image)
                color = 'white'  # Default color

                # First squares are colored, then we write numbers.
                if self.Field.field[col][row].is_flagged:
                    self._canvas_field.create_image(col * self._row_size + 2, row * self._col_size + 2, anchor="nw",
                                                    image=self.flagged_image)

                if self.Field.field[col][row].is_revealed:
                    color = '#A1A1A1'
                    if self.Field.field[col][row].is_mine:
                        if not self.Field.boom:
                            color = 'green'
                        else:
                            color = 'red'

                    self._canvas_field.create_rectangle(col * self._row_size + 1, row * self._col_size + 1,
                                                        col * self._row_size + self._row_size + 1,
                                                        row * self._col_size + self._col_size + 1,
                                                        outline=color, fill=color, width=1)

                number = self.Field.field[col][row].number

                if self.Field.field[col][row].is_mine: continue

                if self.Field.field[col][row].is_revealed:
                    if number > 0:
                        if number == 1:
                            color = "black"
                        elif number == 2:
                            color = "blue"
                        elif number == 3:
                            color = "green"
                        elif number > 3:
                            color = "red"
                        self._canvas_field.create_text(col * self._row_size + 15, row * self._col_size + 15,
                                                       text=str(number), fill=color,
                                                       font='Helvetica 11 bold')

    def draw(self):
        self._canvas_field.delete('all')
        self.draw_info()
        self._draw_insides()
        self._draw_grid()
        self.root.update()
