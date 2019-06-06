import tkinter as Tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import Opengl
from geoleo import pointcloud
from geoleo import util

import numpy as np

class AppOgl(Opengl):

    initialised = 0

    def draw_cordsystem(self):
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3fv((0, 0, 0))
        glVertex3fv((1, 0, 0))

        glColor3f(0, 1, 0)
        glVertex3fv((0, 0, 0))
        glVertex3fv((0, 1, 0))

        glColor3f(0, 0, 1)
        glVertex3fv((0, 0, 0))
        glVertex3fv((0, 0, 1))
        glEnd()

    def init_pointcloud(self):
        pcReader = pointcloud.PointCloudFileIO(
            util.getPathRelativeToRoot("/example_data/pointcloud_examples/47078_575419_0011.laz"))
        self.points = pcReader.getPoints(absolute=False)

        '''self.vertexPositions = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexPositions)
        glBufferData(GL_ARRAY_BUFFER, self.points, GL_STATIC_DRAW)

        # Create the index buffer object
        indices = [0, 1, 2]
        indexPositions = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexPositions)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexPositions)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexPositions)

        glEnableVertexAttribArray(0)  # from 'location = 0' in shader
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)'''



        self.vertexArrayObject = GLuint(0)
        glGenVertexArrays(1, self.vertexArrayObject)
        glBindVertexArray(self.vertexArrayObject)

        '''
        [[11683 25476  8710]
 [11864 25835  8007]
 [11339 25166  9087]
 '''
        vertices = np.array([[0, -3, 0], [0, 5, 0]], dtype='int16')

        positionBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, positionBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        colors = np.array([1, 1, 1], dtype="float")

        colorBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colorBuffer)
        glBufferData(GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW)

        indices = np.array([0])
        indexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, indexBuffer)
        glBufferData(GL_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glBindVertexArray(0)
        '''
        vertices = np.array([0,-5,0], dtype='int16')
        print(vertices)
        vertexPositions = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertexPositions)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        # Create the index buffer object
        indices = np.array([0, 1, 2], dtype='uint8')
        indexPositions = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexPositions)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexPositions)
        glBindBuffer(GL_ARRAY_BUFFER, vertexPositions)

        glEnableVertexAttribArray(0)  # from 'location = 0' in shader
        glVertexAttribPointer(0, 3, GL_INT, False, 0, None)

        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        '''

    def draw_pointcloud(self):
        glBindVertexArray(self.vertexArrayObject)
        glDrawElements(GL_LINES, 3, GL_INT, 0)
        glBindVertexArray(0)

        #glBindVertexArray(self.vertexArrayObject)

        #glDrawArrays(GL_POINTS, 0, 3)  # This line works
        #glDrawElements(GL_POINTS, 3, GL_INT, 0)
        #glBindVertexArray(0)


    def initgl(self):
        self.set_background(0,0,0)
        #self.set_background(173 / 255, 203 / 255, 255 / 255)
        self.set_eyepoint(5)
        #GL_MATRIX_MODE
        glPointSize(2)
        self.fovy = 60.0

        self.near = 0.1
        self.far = 40000.0

        self.yspin = 0
        self.xspin = 0

        #self.autospin = 0.1

        #self.do_AutoSpin()

        self.init_pointcloud()

        self.initialised = 1

        #self.do_AutoSpin()
        pass

    def redraw(self, *args, **named):
        if(self.initialised):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.yspin += 1

            self.draw_cordsystem()
            self.draw_pointcloud()


            glFlush()


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