
import tkinter as Tk # python 3

from gui.input.model import Model
from gui.input.view import View


class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)

    def run(self):
        self.root.title("Input Selection")
        self.root.deiconify()
        self.root.mainloop()
