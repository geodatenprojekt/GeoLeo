import sys, math, time
import tkinter as Tk
from tkinter import ttk
from OpenGL import GL, GLU
from pyopengltk import OpenGLFrame

class AppOgl(OpenGLFrame):

    def initgl(self):
        GL.glViewport( 0, 0, self.width, self.height)
        GL.glClearColor(1.0,1.0,1.0,0.0)
        GL.glColor3f(0.0,0.0, 0.0)
        GL.glPointSize(4.0)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(-5,5,-5,5)
        self.start = time.time()
        self.nframes = 0
    

    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBegin(GL.GL_POINTS)
        npt = 500
        for i in range(npt):
            x = -5.0 + i*10.0/npt 
            y = math.sin(x+ time.time())*5/2
            GL.glVertex2f( x, y )
        GL.glEnd()
        GL.glFlush()
        self.nframes+=1
        tm = time.time() - self.start
        print("fps",self.nframes / tm, end="\r" )