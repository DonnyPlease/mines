import tkinter
import tkinter.ttk


class UI:
    def __init__(self, Field):
        self.root = tkinter.Tk()
        self.root.title('Mines')
        self.root.geometry()
        self.style = tkinter.ttk.Style(self.root)
        self.style.theme_use('clam')

        self.Field = Field