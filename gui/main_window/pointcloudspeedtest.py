import tkinter as Tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import Opengl
from geoleo import pointcloud
from geoleo import util

import numpy as np

class AppOgl(Opengl):

    initialised = 0

    def createData(self):
        self.vao = glGenVertexArrays(1)
        vbos = glGenBuffers(2)
        glBindVertexArray(self.vao)

        # vertices
        vertices = np.array([-1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0], dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, vbos[0])
        glEnableVertexAttribArray(0)  # shader layout location
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, ctypes.c_void_p(0))
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # indices
        indices = np.array([0, 1, 2, 2, 0, 3], dtype=np.int32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbos[1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        self.vertexCount = len(indices)

        glBindVertexArray(0)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDeleteBuffers(2, vbos)

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
            util.getPathRelativeToRoot("/example_data/pointcloud_examples/47078_575411_0011.laz"))
        self.points = pcReader.getPointsWithColors(absolute=False)

        self.vao = glGenVertexArrays(1)
        vbos = glGenBuffers(2)
        glBindVertexArray(self.vao)

        # vertices

        self.dlist = glGenLists(1)
        glNewList(self.dlist, GL_COMPILE)
        glBegin(GL_POINTS)
        for point in self.points:
            glColor3d(point[3] / 65536, point[4] / 65536, point[5] / 65536)
            glVertex3d(point[0], point[2], point[1])
        glEnd()
        glEndList()

        vertices = np.array([0 , -1,  0], dtype=np.int32)
        print(vertices)
        glBindBuffer(GL_ARRAY_BUFFER, vbos[0])
        glEnableVertexAttribArray(0)  # shader layout location
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, ctypes.c_void_p(0))
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        '''
        # indices
       
       
        indices = np.array([0, 0, 0], dtype=np.int32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbos[1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        self.vertexCount = len(indices)
'''
        glBindVertexArray(0)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDeleteBuffers(2, vbos)

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



       #self.vertexArrayObject = GLuint(0)
       # glGenVertexArrays(1, self.vertexArrayObject)
        #glBindVertexArray(self.vertexArrayObject)

        '''
        [[11683 25476  8710]
 [11864 25835  8007]
 [11339 25166  9087]
 '''
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
        #glBindVertexArray(self.vertexArrayObject)
        #glDrawElements(GL_POINTS, 3, GL_INT, 0)
        #glBindVertexArray(0)

        glCallList(self.dlist)

        #glBindVertexArray(self.vertexArrayObject)

        #glDrawArrays(GL_POINTS, 0, 3)  # This line works
        #glDrawElements(GL_POINTS, 3, GL_INT, 0)
        #glBindVertexArray(0)


    def initgl(self):
        self.set_background(0,0,0)
        #self.set_background(173 / 255, 203 / 255, 255 / 255)
        self.set_eyepoint(10000)
        #GL_MATRIX_MODE
        glPointSize(2)
        self.fovy = 60.0

        self.near = 0.1
        self.far = 999999.0

        self.yspin = 0
        self.xspin = 0

        #self.autospin = 0.1

        #self.do_AutoSpin()

        #self.createData()

        self.init_pointcloud()

        self.initialised = 1

        #self.do_AutoSpin()
        pass

    def redraw(self, *args, **named):
        if(self.initialised):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.yspin += 1

            glBindVertexArray(self.vao)
            self.vertexCount = 0
            #glDrawArrays(GL_POINTS, 0, 3)  # This line works
            # glDrawElements(GL_POINTS, self.vertexCount, GL_UNSIGNED_INT, ctypes.c_void_p(0))
            glBindVertexArray(0)
            #self.draw_cordsystem()
            self.draw_pointcloud()

            glBegin(GL_POINTS)
            glColor3f(0, 1, 0)
            glVertex3fv((0, -2, 0))
            glEnd()

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