import tkinter as Tk # python 3
from tkinter import ttk

class SidePanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame(root)
        self.frame2.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.lasBut = Tk.Button(self.frame2, text="Choose Las")
        self.lasBut.pack(side="top", fill=Tk.BOTH)
        self.gmlButton = Tk.Button(self.frame2, text="Choose Gml")
        self.gmlButton.pack(side="top", fill=Tk.BOTH)
        self.contBut = Tk.Button(self.frame2, text="Continue")
        self.contBut.pack(side="top", fill=Tk.BOTH)