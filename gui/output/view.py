
from tkinter import filedialog
import tkinter as Tk # python 3

from gui.output.side_panel import SidePanel


class View:
    def __init__(self, root, model):
        self.frame = Tk.Frame(root)
        self.model = model

        self.model.outPath = Tk.StringVar()
        self.model.outPath.set("No Path")
        
        self.out_label = Tk.Label(self.frame, textvariable=self.model.outPath)
        self.out_label.pack(side="top", fill=Tk.BOTH)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidepanel = SidePanel(root)

        self.cont_but = Tk.Button(self.frame, text="Continue")
        self.cont_but.grid(row=2, column=0, rowspan=2, columnspan=2, sticky="ew")

        self.sidepanel.out_but.config(command=lambda: self.setOut())
        self.cont_but.config(command=lambda: self.cont)

    def setOut(self):
        self.model.outPath.set(filedialog.askdirectory())

    def cont(self):
        pass