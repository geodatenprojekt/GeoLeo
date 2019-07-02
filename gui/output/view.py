
from tkinter import filedialog
import tkinter as Tk # python 3
import subprocess

from gui.output.side_panel import SidePanel


class View:
    def __init__(self, root, model, contr):
        self.frame = Tk.Frame(root)
        self.frame.grid(row=0, column=0, sticky='news')
        self.model = model
        self.controller = contr

        self.model.outPath = Tk.StringVar()
        self.model.outPath.set("No Path")
        
        self.out_label = Tk.Label(self.frame, textvariable=self.model.outPath)
        self.out_label.pack(side="top", fill=Tk.BOTH)
        self.sidepanel = SidePanel(self.frame)

        self.sidepanel.out_but.config(command=lambda: self.setOut())
        self.sidepanel.cont_but.config(command=lambda: self.cont())

    def setOut(self):
        self.model.outPath.set(filedialog.askdirectory())

    def cont(self):
        print("press")
        self.model.cutPC()