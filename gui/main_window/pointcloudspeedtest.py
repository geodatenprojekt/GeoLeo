import tkinter as Tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import Opengl
from geoleo import pointcloud
from geoleo import util
from geoleo import cadaster
import numpy as np
from gui.main_window.absolute_parser import AbsParser

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

    def init_cadaster(self):
        cad = cadaster.Cadaster("../../example_data/cadaster_examples")

        self.cadlist = glGenLists(1)
        glNewList(self.cadlist, GL_COMPILE)

        glColor3d(1, 0, 0)
        for building in cad.buildings:
            glBegin(GL_POLYGON)
            for coord in building.coordinates:
                x = self.parser.parse_coords(coord._x, coord._y, coord._z)
                glVertex3d(x[0], x[1], x[2])
                self.cam = x
            glEnd()
        glEndList()

    def init_pointcloud(self):
        reader = pointcloud.PointCloudFileIO(
            util.getPathRelativeToRoot("/example_data/pointcloud_examples/47078_575419_0011.laz"))

        self.cloudlist = glGenLists(1)
        glNewList(self.cloudlist, GL_COMPILE)
        glBegin(GL_POINTS)
        points = reader.getPointsWithColors(absolute=True)

        max = np.amax(points, axis=0)
        min = np.amin(points, axis=0)

        self.parser = AbsParser(min, max)
        points = self.parser.parse_list(points)

        for point in points:
            glColor3d(point[3] / 65536, point[4] / 65536, point[5] / 65536)
            glVertex3d(point[0], point[2], point[1])
        glEnd()
        glEndList()

    def draw_cadaster(self):
        glCallList(self.cadlist)

    def draw_pointcloud(self):
        glCallList(self.cloudlist)

    def initgl(self):
        self.set_background(173 / 255, 203 / 255, 255 / 255)
        self.set_eyepoint(5)

        glPointSize(2)

        self.fovy = 60.0
        self.near = 0.1
        self.far = 999999.0

        self.init_pointcloud()
        self.init_cadaster()

        print(self.cam)
        self.set_centerpoint(self.cam[0], self.cam[1], self.cam[2])

        self.initialised = 1
        pass

    def redraw(self, *args, **named):
        if (self.initialised):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

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