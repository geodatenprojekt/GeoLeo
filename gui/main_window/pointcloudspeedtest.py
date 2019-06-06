import tkinter as Tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import Opengl
from geoleo import pointcloud
from geoleo import util

class AppOgl(Opengl):

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
        self.points = pcReader.getPointsWithColors(absolute=False)

        self.vertexPositions = glGenBuffers(1)
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
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw_pointcloud(self):
        glBindVertexArray(self.vertexPositions)
        glDrawElements(GL_POINTS, 3, GL_UNSIGNED_SHORT, 0)
        glBindVertexArray(0)


    def initgl(self):
        self.set_background(173 / 255, 203 / 255, 255 / 255)
        self.set_eyepoint(20000)
        #GL_MATRIX_MODE
        glPointSize(2)
        self.fovy = 60.0

        self.near = 0.1
        self.far = 40000.0

        self.yspin = 0
        self.xspin = 0

        self.autospin = 0.1

        self.do_AutoSpin()

        self.init_pointcloud()

        #self.do_AutoSpin()
        pass

    def redraw(self, *args, **named):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.yspin += 1
        print(self.yspin)

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