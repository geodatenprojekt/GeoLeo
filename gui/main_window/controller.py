import tkinter as Tk # python 3

from gui.main_window.model import Model
from gui.main_window.view import View


class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)

    def run(self):
        self.root.title("Pointcloud view")
        self.root.deiconify()
        self.root.mainloop()
