import tkinter as Tk # python 3
from tkinter import ttk

class SidePanel():
    def __init__(self, root):
        self.sb = Tk.Frame(root)
        self.sb.pack(side="top", fill=Tk.BOTH, expand=Tk.YES)
        
        self.sbt = Tk.Frame(self.sb)
        self.sbt.pack(side="top", fill=Tk.BOTH, expand=Tk.NO, pady = 2)
        self.scal_label = Tk.Label(self.sbt, text="Step Length:")
        self.scal_label.pack(side="top", fill=Tk.BOTH)
        self.step_entry = Tk.Entry(self.sbt)
        self.step_entry.delete(0, Tk.END)
        self.step_entry.insert(0, "1")
        self.step_entry.pack(side="top", fill=Tk.BOTH, expand=Tk.NO)

        self.sidebar = Tk.Frame(self.sb)
        self.sidebar.pack(side="top", fill=Tk.X)
        self.left_but = Tk.Button(self.sidebar, text="←")
        self.left_but.pack(side="left", fill=Tk.BOTH)
        self.right_but = Tk.Button(self.sidebar, text="→")
        self.right_but.pack(side="right", fill=Tk.BOTH)
        self.up_but = Tk.Button(self.sidebar, text="↑")
        self.up_but.pack(side="top", fill=Tk.BOTH)
        self.down_but = Tk.Button(self.sidebar, text="↓")
        self.down_but.pack(side="top", fill=Tk.BOTH)

        self.sepf = Tk.Frame(self.sb)
        self.sepf.pack(side="top", fill=Tk.X, pady=2)
        self.sep = ttk.Separator(self.sepf, orient=Tk.HORIZONTAL)
        self.sep.pack(side="bottom", fill=Tk.BOTH)

        """Scale Frame"""
        self.sbf = Tk.Frame(self.sb)
        self.sbf.pack(side="top", fill=Tk.BOTH, expand=Tk.YES)
        self.scalLabel = Tk.Label(self.sbf, text="Scale Factor:")
        self.scalLabel.pack(side="top", fill=Tk.BOTH)
        self.entry = Tk.Entry(self.sbf)
        self.entry.insert(Tk.END, "1")
        self.entry.pack(side="top", fill=Tk.BOTH, expand=Tk.NO)
        self.sup_but = Tk.Button(self.sbf, text="Scale Up")
        self.sup_but.pack(side="top", fill=Tk.BOTH)
        
        self.sdown_but = Tk.Button(self.sbf, text="Scale Down")
        self.sdown_but.pack(side="top", fill=Tk.BOTH)

        self.cont_but = Tk.Button(self.sbf, text="Cut Pointcloud")
        self.cont_but.pack(side="bottom", fill=Tk.BOTH)