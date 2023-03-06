import MineField
import UI_tkinter


def main() -> int:
    Field = MineField.MineField(8, 8, 4)
    UI = UI_tkinter.UI(Field)
    UI.root.mainloop()


if __name__ == '__main__':
    main()
