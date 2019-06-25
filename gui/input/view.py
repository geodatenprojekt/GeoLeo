from tkinter import filedialog
import tkinter as Tk # python 3

from gui.input.side_panel import SidePanel

class View:
    def __init__(self, root, model, contr):
        self.frame = Tk.Frame(root)
        self.frame.grid(row=0, column=0, sticky='news')
        self.model = model
        self.root = root
        self.controller = contr

        self.model.lasPath = Tk.StringVar()
        self.model.lasPath.set("No Path")

        self.model.gmlPath = Tk.StringVar()
        self.model.gmlPath.set("No Path")
        
        self.las_label = Tk.Label(self.frame, textvariable=self.model.lasPath)
        self.las_label.grid(row=0, column=0)
        self.las_but = Tk.Button(self.frame, text="Choose Las")
        self.las_but.grid(row=0, column=1, sticky="ew")

        self.gml_label = Tk.Label(self.frame, textvariable=self.model.gmlPath)
        self.gml_label.grid(row=1, column=0)
        self.gml_but = Tk.Button(self.frame, text="Choose Gml")
        self.gml_but.grid(row=1, column=1, sticky="ew")

        self.cont_but = Tk.Button(self.frame, text="Continue")
        self.cont_but.grid(row=2, column=0, rowspan=2, columnspan=2, sticky="ew")

        self.las_but.config(command=lambda: self.set_las()) 
        self.gml_but.config(command=lambda: self.set_gml())
        self.cont_but.config(command=lambda: self.cont())

    def choose_path(self):
        return filedialog.askdirectory()

    def set_las(self):
        self.model.lasPath.set(self.choose_path())
        print(self.model.lasPath)

    def set_gml(self):
        self.model.gmlPath.set(self.choose_path())
        print(self.model.gmlPath)
		
    def cont(self):
        self.controller.raise_main()