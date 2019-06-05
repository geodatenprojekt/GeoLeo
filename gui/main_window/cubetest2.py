import tkinter as Tk
from OpenGL import GL, GLU
from pyopengltk import Opengl

class AppOgl(Opengl):

    def draw_cordsystem(self):
        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(1, 0, 0)
        GL.glVertex3fv((0, 0, 0))
        GL.glVertex3fv((1, 0, 0))

        GL.glColor3f(0, 1, 0)
        GL.glVertex3fv((0, 0, 0))
        GL.glVertex3fv((0, 1, 0))

        GL.glColor3f(0, 0, 1)
        GL.glVertex3fv((0, 0, 0))
        GL.glVertex3fv((0, 0, 1))
        GL.glEnd()

    def initgl(self):
        self.set_background(0, 0, 0)
        self.set_eyepoint(10)
        #self.do_AutoSpin()

        pass

    def redraw(self, *args, **named):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.draw_cordsystem()


        GL.glFlush()


if __name__ == '__main__':
    root = Tk.Tk()
    app = AppOgl(root, width=600, height=600)
    app.pack(fill=Tk.BOTH, expand=Tk.YES)
    sidebar = Tk.Frame(root)
    sidebar.pack(side="top", fill=Tk.BOTH)
    but1 = Tk.Button(sidebar, text="start")
    but1.pack(side="top", fill=Tk.BOTH)
    but2 = Tk.Button(sidebar, text="stop")
    but2.pack(side="top", fill=Tk.BOTH)
    root.mainloop()