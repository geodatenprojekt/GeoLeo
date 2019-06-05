try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3


class SidePanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame(root)
        self.frame2.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.outBut = Tk.Button(self.frame2, text="Choose Output")
        self.outBut.pack(side="top", fill=Tk.BOTH)

        self.contBut = Tk.Button(self.frame2, text="Continue")
        self.contBut.pack(side="top", fill=Tk.BOTH)