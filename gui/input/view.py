
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

        self.model.lasPath = Tk.StringVar()
        self.model.lasPath.set("No Path")

        self.model.gmlPath = Tk.StringVar()
        self.model.gmlPath.set("No Path")
        
        self.lasLabel = Tk.Label(self.frame, textvariable=self.model.lasPath)
        self.lasLabel.pack(side="top", fill=Tk.BOTH)
        self.gmlLabel = Tk.Label(self.frame, textvariable=self.model.gmlPath)
        self.gmlLabel.pack(side="top", fill=Tk.BOTH)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidepanel = SidePanel(root)

        self.sidepanel.lasBut.bind("<Button>", self.setLas)
        self.sidepanel.gmlButton.bind("<Button>", self.setGml)
        self.sidepanel.contBut.bind("<Button>", self.cont)

    def choosePath(self):
        return filedialog.askdirectory()

    def setLas(self, event):
        self.model.lasPath.set(self.choosePath())

    def setGml(self, event):
        self.model.gmlPath.set(self.choosePath())
		
    def cont(self, event):
        pass
