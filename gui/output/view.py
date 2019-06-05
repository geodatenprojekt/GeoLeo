
try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    from tkinter import filedialog
    import tkinter as Tk # python 3

from side_panel import SidePanel


class View:
    def __init__(self, root, model):
        self.frame = Tk.Frame(root)
        self.model = model

        self.model.outPath = Tk.StringVar()
        self.model.outPath.set("No Path")
        
        self.outLabel = Tk.Label(self.frame, textvariable=self.model.outPath)
        self.outLabel.pack(side="top", fill=Tk.BOTH)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidepanel = SidePanel(root)

        self.sidepanel.outBut.bind("<Button>", self.setOut)
        self.sidepanel.contBut.bind("<Button>", self.cont)

    def setOut(self, event):
        self.model.outPath.set(filedialog.askdirectory())

    def cont(self, event):
        pass