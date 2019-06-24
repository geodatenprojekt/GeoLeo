import tkinter as Tk # python 3

from model import Model
from view import View


class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)

    def run(self):
        self.root.title("Output Selection")
        self.root.deiconify()
        self.root.mainloop()
