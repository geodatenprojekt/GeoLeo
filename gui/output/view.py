
from tkinter import filedialog
import tkinter as Tk # python 3

from gui.output.side_panel import SidePanel


class View:
    def __init__(self, root, model):
        self.frame = Tk.Frame(root)
        self.model = model

        self.model.out_path = Tk.StringVar()
        self.model.out_path.set("No Path")
        
        self.out_label = Tk.Label(self.frame, textvariable=self.model.outPath)
        self.out_label.pack(side="top", fill=Tk.BOTH)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidepanel = SidePanel(root)

        self.sidepanel.out_but.config(command=lambda: self.setOut())
        self.sidepanel.cont_but.config(command=lambda: self.cont)

    def setOut(self):
        self.model.out_path.set(filedialog.askdirectory())

    def cont(self):
        pass