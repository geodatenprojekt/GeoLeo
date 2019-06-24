import tkinter as Tk # python 3


class SidePanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame(root)
        self.frame2.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.out_but = Tk.Button(self.frame2, text="Choose Output")
        self.out_but.pack(side="top", fill=Tk.BOTH)

        self.cont_but = Tk.Button(self.frame2, text="Continue")
        self.cont_but.pack(side="top", fill=Tk.BOTH)