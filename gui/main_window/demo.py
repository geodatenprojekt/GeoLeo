from __future__ import print_function

"""
Demo entry point for Tkinter Window with OpenGL
"""

import sys, math, time

if sys.version_info[0] < 3:
    from Tkinter import Tk, YES, BOTH
else:
    import tkinter as Tk
    from tkinter import ttk
from OpenGL import GL, GLU
from pyopengltk import OpenGLFrame


class AppOgl(OpenGLFrame):

    def initgl(self):
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glPointSize(4.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(-5, 5, -5, 5)
        self.start = time.time()
        self.nframes = 0

    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBegin(GL.GL_POINTS)
        npt = 500
        for i in range(npt):
            x = -5.0 + i * 10.0 / npt
            y = math.sin(x + time.time()) * 5 / 2
            GL.glVertex2f(x, y)
        GL.glEnd()
        GL.glFlush()
        self.nframes += 1
        tm = time.time() - self.start
        print("fps", self.nframes / tm, end="\r")


if __name__ == '__main__':
    root = Tk.Tk()
    """ opengl frame"""
    app = AppOgl(root, width=1024, height=720)
    app.pack(side="left", fill=Tk.BOTH, expand=Tk.YES)
    app.animate = 1
    app.after(100, app.printContext)

    """Direction (side) Frame"""
    sb = Tk.Frame(root)
    sb.pack(side="top", fill=Tk.BOTH, expand=Tk.YES)

    sbt = Tk.Frame(sb)
    sbt.pack(side="top", fill=Tk.BOTH, expand=Tk.NO, pady=2)
    scalLabel1 = Tk.Label(sbt, text="Step Length:")
    scalLabel1.pack(side="top", fill=Tk.BOTH)
    entry1 = Tk.Entry(sbt)
    entry1.delete(0, Tk.END)
    entry1.insert(0, "1")
    entry1.pack(side="top", fill=Tk.BOTH, expand=Tk.NO)

    sidebar = Tk.Frame(sb)
    sidebar.pack(side="top", fill=Tk.X)
    left_but = Tk.Button(sidebar, text="←")
    left_but.pack(side="left", fill=Tk.BOTH)
    right_but = Tk.Button(sidebar, text="→")
    right_but.pack(side="right", fill=Tk.BOTH)
    up_but = Tk.Button(sidebar, text="↑")
    up_but.pack(side="top", fill=Tk.BOTH)
    down_but = Tk.Button(sidebar, text="↓")
    down_but.pack(side="top", fill=Tk.BOTH)

    sepf = Tk.Frame(sb)
    sepf.pack(side="top", fill=Tk.X, pady=2)
    sep = ttk.Separator(sepf, orient=Tk.HORIZONTAL)
    sep.pack(side="bottom", fill=Tk.BOTH)

    """Scale Frame"""
    sbf = Tk.Frame(sb)
    sbf.pack(side="top", fill=Tk.BOTH, expand=Tk.YES)
    scalLabel = Tk.Label(sbf, text="Scale Factor:")
    scalLabel.pack(side="top", fill=Tk.BOTH)
    entry = Tk.Entry(sbf)
    entry.insert(Tk.END, "1")
    entry.pack(side="top", fill=Tk.BOTH, expand=Tk.NO)
    sup_but = Tk.Button(sbf, text="Scale Up")
    sup_but.pack(side="top", fill=Tk.BOTH)

    sdown_but = Tk.Button(sbf, text="Scale Down")
    sdown_but.pack(side="top", fill=Tk.BOTH)

    cont_but = Tk.Button(sbf, text="Cut Pointcloud")
    cont_but.pack(side="bottom", fill=Tk.BOTH)
    root.mainloop()
