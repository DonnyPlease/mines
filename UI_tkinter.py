import tkinter
import tkinter.ttk
import MineField
from PIL import Image, ImageTk
import PIL
import time


class UI:
    # Set parameters for size of one grid edge
    _row_size = 25
    _col_size = 25

    def __init__(self, Field):
        self.root = tkinter.Tk()
        self.root.title('Minesweeper')
        self.root.resizable(False, False)

        self.logo = (PIL.Image.open("logo.png"))
        self.logo = self.logo.resize((18, 18), PIL.Image.ANTIALIAS)
        self.logo = PIL.ImageTk.PhotoImage(self.logo)
        self.root.iconphoto(False, self.logo)

        # MENU
        self._menubar = None
        self._game_menu = None
        self._settings = None
        self._help_menu = None
        self._set_up_menu()

        # Assign MineField instance to a class variable and assing the important parameters
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

        # Set up the canvas of the upper bar
        self._canvas_info = tkinter.Canvas(self.root, width=self._width_of_canvas, height=40)
        self._canvas_info.grid(column=0, row=0)
        self.timer_text = self._canvas_info.create_text(80, 20, text="Mines to find: "+str(self.Field.number_of_mines),
                                                        fill="black",
                                                        font='Helvetica 14 bold')

        # Images of tiles
        self.unrevealed_image = None
        self.flagged_image = None
        self.mine_lose_image = None
        self.mine_win_image = None
        self._import_images()

        #self.start_timer(0)

        # self.num_of_cols = tkinter.IntVar(value=self._number_of_columns)
        # self.num_of_rows = tkinter.IntVar(value=self._number_of_rows)
        # self.num_of_mines = tkinter.IntVar(value=self._number_of_mines)


        self.draw()

    def start_timer(self, secs):
        self._canvas_info.itemconfig(self.timer_text, text=f"{secs:02}")
        self._canvas_info.after(1000, self.start_timer, secs + 1)

    def _set_up_menu(self):
        self._menubar = tkinter.Menu(self.root, background='green', tearoff=0)

        self._game_menu = tkinter.Menu(self._menubar, tearoff=0)
        self._game_menu.add_command(label="Reset", command=lambda: self.reset(False), accelerator="F5")
        self._game_menu.add_separator()
        self._game_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        self._menubar.add_cascade(label="Game", menu=self._game_menu)

        self._settings = tkinter.Menu(self._menubar, tearoff=0)
        self._settings.add_command(label="Default settings", command=lambda: self.reset(True))
        self._settings.add_command(label="Customize", command=lambda: self._ask_params())
        self._menubar.add_cascade(label="Options", menu=self._settings)

        self._help_menu = tkinter.Menu(self._menubar, tearoff=0)
        self._help_menu.add_command(label="Rules")
        self._help_menu.add_command(label="About...")
        self._menubar.add_cascade(label="Help", menu=self._help_menu)

        self.root.config(menu=self._menubar)

        # Keyboard shortcuts
        self.root.bind_all("<Control-q>", lambda event: self.root.quit())
        self.root.bind_all("<F5>", lambda event: self.reset(False))

    def _import_images(self):
        size = self._col_size - 1

        unrevealed_img = (Image.open("tile_square2.png"))
        resized_unrevealed_img = unrevealed_img.resize((size, size), Image.ANTIALIAS)
        self.unrevealed_image = ImageTk.PhotoImage(resized_unrevealed_img)

        flagged_img = (Image.open("tile_square_flagged.png"))
        resized_flagged_img = flagged_img.resize((size, size), Image.ANTIALIAS)
        self.flagged_image = ImageTk.PhotoImage(resized_flagged_img)

        mine_lose_img = (Image.open("mine_lose.png"))
        resized_mine_lose_img = mine_lose_img.resize((size, size), Image.ANTIALIAS)
        self.mine_lose_image = ImageTk.PhotoImage(resized_mine_lose_img)

        mine_win_img = (Image.open("mine_win.png"))
        resized_mine_win_img = mine_win_img.resize((size, size), Image.ANTIALIAS)
        self.mine_win_image = ImageTk.PhotoImage(resized_mine_win_img)

    def set_canvas(self):
        self._width_of_canvas = self._number_of_columns * self._col_size + 1
        self._height_of_canvas = self._number_of_rows * self._row_size + 1
        self._canvas_field.config(width=self._width_of_canvas, height=self._height_of_canvas)

    def reset(self, default=True, new_params=None):
        if default:
            self._number_of_rows = 10
            self._number_of_columns = 10
            self._number_of_mines = 10

        if new_params is None:
            new_params = [self._number_of_columns, self._number_of_rows, self._number_of_mines]

        if not default:
            self._number_of_rows = new_params[1]
            self._number_of_columns = new_params[0]
            self._number_of_mines = new_params[2]

        del self.Field
        self.Field = MineField.MineField(self._number_of_columns, self._number_of_rows, self._number_of_mines)

        self.set_canvas()

        self.draw()

    def reveal(self, event):
        if self.Field.boom or self.Field.check_win(): return

        col = (event.x - 1) // self._row_size
        row = (event.y - 1) // self._col_size

        if self.Field.field[col][row].is_flagged: return

        self.Field.reveal(col=col, row=row)
        self.draw()

    def toggle_flag(self, event):
        if self.Field.boom or self.Field.check_win(): return

        col = (event.x - 1) // self._row_size
        row = (event.y - 1) // self._col_size

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

        # self._canvas_info.create_text(80, 20, text="Mines to find: " + str(self.Field.number_of_mines), fill="black",
        #                               font='Helvetica 14 bold')

    def _draw_grid(self):
        sizeX = self._width_of_canvas
        sizeY = self._height_of_canvas
        for i in range(self._number_of_rows + 1):
            self._canvas_field.create_line(0, i * self._col_size + 1, sizeX + 1, i * self._col_size + 1,
                                           fill='#636363', width=1)
        for j in range(self._number_of_columns + 1):
            self._canvas_field.create_line(j * self._row_size + 1, 0, j * self._row_size + 1, sizeY + 1,
                                           fill='#636363', width=1)

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
                    self._canvas_field.create_rectangle(col * self._row_size + 1, row * self._col_size + 1,
                                                        col * self._row_size + self._row_size + 1,
                                                        row * self._col_size + self._col_size + 1,
                                                        outline=color, fill=color, width=1)
                    if self.Field.field[col][row].is_mine:
                        if not self.Field.boom:
                            self._canvas_field.create_image(col * self._row_size + 2, row * self._col_size + 2,
                                                            anchor="nw",
                                                            image=self.mine_win_image)
                        else:
                            self._canvas_field.create_image(col * self._row_size + 2, row * self._col_size + 2,
                                                            anchor="nw",
                                                            image=self.mine_lose_image)
                        continue

                if self.Field.field[col][row].is_revealed:
                    number = self.Field.field[col][row].number
                    if number > 0:
                        if number == 1:
                            color = "black"
                        elif number == 2:
                            color = "blue"
                        elif number == 3:
                            color = "green"
                        elif number > 3:
                            color = "red"

                        self._canvas_field.create_text(col * self._row_size + 14, row * self._col_size + 14,
                                                       text=str(number), fill=color,
                                                       font='Helvetica 12 bold')

    def draw(self):
        self._canvas_field.delete('all')
        self.draw_info()
        self._draw_insides()
        self._draw_grid()
        self.root.update()

    def _ask_params(self):
        param_window = tkinter.Toplevel(self.root)
        param_window.title("Customize")
        param_window.iconphoto(False, self.logo)

        param_window.resizable(False, False)

        # sets the geometry of toplevel
        # param_window.geometry("200x200")

        # param_window.attributes('-toolwindow', True)
        # set maximum window size value
        height = 115
        width = 155

        # get screen width and height
        screen_width = param_window.winfo_screenwidth()
        screen_height = param_window.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        param_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # A Label widget to show in toplevel
        title = tkinter.Label(param_window, text="CUSTOMIZE THE GAME")
        cols_label = tkinter.Label(param_window, text="Number of columns:")
        rows_label = tkinter.Label(param_window, text="Number of rows:")
        mines_label = tkinter.Label(param_window, text="Number of mines:")

        num_of_cols = tkinter.IntVar(value=self._number_of_columns)
        num_of_rows = tkinter.IntVar(value=self._number_of_rows)
        num_of_mines = tkinter.IntVar(value=self._number_of_mines)

        cols_spin = tkinter.Spinbox(param_window, from_=1, to=999, width=3, textvariable=num_of_cols)
        rows_spin = tkinter.Spinbox(param_window, from_=1, to=999, width=3, textvariable=num_of_rows)
        mines_spin = tkinter.Spinbox(param_window, from_=1, to=999, width=3, textvariable=num_of_mines)

        title.grid(column=0, row=0, columnspan=2)
        cols_label.grid(column=0, row=1, sticky='e')
        rows_label.grid(column=0, row=2, sticky='e')
        mines_label.grid(column=0, row=3, sticky='e')

        cols_spin.grid(column=1, row=1, sticky='w')
        rows_spin.grid(column=1, row=2, sticky='w')
        mines_spin.grid(column=1, row=3, sticky='w')

        ButtonSet = tkinter.ttk.Button(param_window, text="Set",
                                       command=lambda: [self.reset(False, [int(cols_spin.get()),
                                                                           int(rows_spin.get()),
                                                                           int(mines_spin.get())]),
                                                        param_window.destroy()
                                                        ])
        ButtonSet.grid(column=0, row=4, columnspan=2)  # Update button


