
from tkinter import filedialog
import tkinter as Tk

from gui.main_window.side_panel import SidePanel
from gui.main_window.openglframe import AppOgl

from OpenGL import GL, GLU
from gui.main_window.pyopengltk import OpenGLFrame

from gui.main_window.side_panel import SidePanel


class View:
    def __init__(self, root, model):
        self.frame = Tk.Frame(root)
        self.model = model

        self.opengl = AppOgl(root, width=1024, height=720)
        self.opengl.pack(side="left", fill=Tk.BOTH)
        
        self.opengl.animate=1

        self.sidepanel = SidePanel(root);

        self.sidepanel.up_but.config(command=lambda: self.move_up())
        self.sidepanel.down_but.config(command=lambda: self.move_down())
        self.sidepanel.left_but.config(command=lambda: self.move_left())
        self.sidepanel.right_but.config(command=lambda: self.move_right())

        self.sidepanel.sup_but.config(command=lambda: self.scale_up())
        self.sidepanel.sdown_but.config(command=lambda: self.scale_down())

        self.sidepanel.cont_but.config(command=lambda: self.cont())

    def getFloatFromEntry(self, entr):
        try:
            return float(entr.get())
        except:
            pass

    def move_left(self):
        try:
            self.model.moveInXDirection(self.getFloatFromEntry(self.sidepanel.step_entry)*(-1.0))
            print("X ",self.model.moveX)
        except:
            pass

    def move_right(self):
        try:
            self.model.moveInXDirection(self.getFloatFromEntry(self.sidepanel.step_entry))
            print("X ",self.model.moveX)
        except:
            pass

    def move_up(self):
        try:
            self.model.moveInYDirection(self.getFloatFromEntry(self.sidepanel.step_entry)*(-1.0))
            print("Y ", self.model.moveY)
        except:
            pass

    def move_down(self):
        try:
            self.model.moveInYDirection(self.getFloatFromEntry(self.sidepanel.step_entry))
            print("Y ", self.model.moveY)
        except:
            pass

    def scale_up(self):
        try:
            self.model.scaleSize(self.getFloatFromEntry(self.sidepanel.entry))
            print("Scale ",self.model.scaleFactor)
        except:
            pass
    
    def scale_down(self):
        try:
            self.model.scaleSize(self.getFloatFromEntry(self.sidepanel.entry))
            print("Scale ",self.model.scaleFactor)
        except:
            pass

    def cont(self):
        pass