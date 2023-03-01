from MineField import MineField
import UI_tkinter

if __name__ == '__main__':
    Field = MineField(10, 10, 5)
    UI = UI_tkinter.UI(Field)
    UI.root.mainloop()

