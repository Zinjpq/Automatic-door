from tkinter import Tk
from src.Components.AllBar import MainWindow
import pretty_errors

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
