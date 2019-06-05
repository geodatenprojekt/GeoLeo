import sys, math, time

import tkinter as Tk
from OpenGL import GL, GLU
from pyopengltk import OpenGLFrame
from pyopengltk import Opengl

class AppOgl(OpenGLFrame):

    eye = [1, 0, 0]
    center = (0, 0, 0)
    up = (0, 1, 0)

    def keyup(self, e):
        print('up', e.char)
        if(e.char == '+'):
            self.eye[0] = self.eye[0] - 1
            self.redraw()
        if (e.char == '-'):
            self.eye[0] = self.eye[0] + 1
            self.redraw()

    def keydown(self, e):
        print('down', e.char)


    def draw_cube(self):
        GL.glBegin(GL.GL_QUADS)

        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glVertex3f(1.0, 1.0, -1.0)
        GL.glVertex3f(-1.0, 1.0, -1.0)
        GL.glVertex3f(-1.0, 1.0, 1.0)
        GL.glVertex3f(1.0, 1.0, 1.0)

        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glVertex3f(1.0, -1.0, 1.0)
        GL.glVertex3f(-1.0, -1.0, 1.0)
        GL.glVertex3f(-1.0, -1.0, -1.0)
        GL.glVertex3f(1.0, -1.0, -1.0)

        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glVertex3f(1.0, 1.0, 1.0)
        GL.glVertex3f(-1.0, 1.0, 1.0)
        GL.glVertex3f(-1.0, -1.0, 1.0)
        GL.glVertex3f(1.0, -1.0, 1.0)

        GL.glColor3f(1.0, 1.0, 0.0)
        GL.glVertex3f(1.0, -1.0, -1.0)
        GL.glVertex3f(-1.0, -1.0, -1.0)
        GL.glVertex3f(-1.0, 1.0, -1.0)
        GL.glVertex3f(1.0, 1.0, -1.0)

        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex3f(-1.0, 1.0, 1.0)
        GL.glVertex3f(-1.0, 1.0, -1.0)
        GL.glVertex3f(-1.0, -1.0, -1.0)
        GL.glVertex3f(-1.0, -1.0, 1.0)

        GL.glColor3f(1.0, 0.0, 1.0)
        GL.glVertex3f(1.0, 1.0, -1.0)
        GL.glVertex3f(1.0, 1.0, 1.0)
        GL.glVertex3f(1.0, -1.0, 1.0)
        GL.glVertex3f(1.0, -1.0, -1.0)

        GL.glEnd()

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
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glPointSize(4.0)
        GL.glMatrixMode(GL.GL_PROJECTION)

        # GLU.gluOrtho2D(-5, 5, -5, 5)
        GL.glLoadIdentity()
        GLU.gluPerspective(90.0, self.width / self.height, 0.1, 20000)


    def updateCamera(self):
        GLU.gluLookAt(self.eye[0], self.eye[1], self.eye[2],
                      self.center[0], self.center[1], self.center[2],
                      self.up[0], self.up[1], self.up[2])

    def redraw(self):
        print("REDRAW", self.eye)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.updateCamera()

        self.draw_cube()
        self.draw_cordsystem()

        GL.glFlush()



if __name__ == '__main__':
    root = Tk.Tk()
    app = Opengl(root, width=600, height=600)
    app.pack(fill=Tk.BOTH, expand=Tk.YES)
    sidebar = Tk.Frame(root)
    sidebar.pack(side="top", fill=Tk.BOTH)
    but1 = Tk.Button(sidebar, text="start")
    but1.pack(side="top", fill=Tk.BOTH)
    but2 = Tk.Button(sidebar, text="stop")
    but2.pack(side="top", fill=Tk.BOTH)
    root.mainloop()
'''
if __name__ == '__main__':
    root = Tk.Tk()
    app = AppOgl(root, width=600, height=600)
    app.bind("<KeyPress>", app.keydown)
    app.bind("<KeyRelease>", app.keyup)
    app.focus_set()
    app.pack(fill=Tk.BOTH, expand=Tk.YES)
    sidebar = Tk.Frame(root)
    sidebar.pack(side="top", fill=Tk.BOTH)
    but1 = Tk.Button(sidebar, text="start")
    but1.pack(side="top", fill=Tk.BOTH)
    but2 = Tk.Button(sidebar, text="stop")
    but2.pack(side="top", fill=Tk.BOTH)
    root.mainloop()
'''