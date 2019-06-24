import tkinter as Tk
from OpenGL.GL import *
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
        cad = cadaster.Cadaster(util.getPathRelativeToRoot("/example_data/cadaster_examples/"))


        self.cadlist = glGenLists(1)
        glNewList(self.cadlist, GL_COMPILE)

        glColor3d(1, 0, 0)

        vertices = []

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for building in cad.buildings:
            glBegin(GL_POLYGON)
            for coord in building.coordinates:
                x = self.parser.parse_coords(coord._x, coord._y, coord._z)
                glVertex3d(x[0], x[2], x[1])
                vertices.append((x[0], x[2], x[1]))
            glEnd()
        glEndList()


        #self.cam = np.amax(vertices, axis=0)
        print(np.amax(vertices, axis=0))
        print(np.amin(vertices, axis=0))

    def init_pointcloud(self):
        '''
        47094_575411_0011.las
        47094_575419_0011.las
        47094_575427_0011.las
        '''

        reader = pointcloud.PointCloudFileIO(
            util.getPathRelativeToRoot("/example_data/pointcloud_examples/47094_575419_0011.las"))


        self.cloudlist = glGenLists(1)
        glNewList(self.cloudlist, GL_COMPILE)
        glBegin(GL_POINTS)
        points = reader.getPointsWithColors(absolute=True)

        points_max = np.amax(points, axis=0)
        points_min = np.amin(points, axis=0)

        self.parser = AbsParser(points_min, points_max)
        points = self.parser.parse_list(points)

        eye = self.parser.parse_coords(points_max[0], points_max[1], points_max[2])
        points_med = np.median(points, axis=0)

        print(eye)
        print(np.amax(points, axis=0))
        self.set_eyepoint(eye[2] + max(eye[1], eye[0]))
        self.cam = (points_med[0], points_med[2], points_med[1])

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

        glPointSize(2)

        self.fovy = 40.0
        self.near = 0.1
        self.far = 999999.0

        self.init_pointcloud()
        self.init_cadaster()

        glRotatef(90.0, 1., 0., 0.)
        self.set_centerpoint(self.cam[0], -self.cam[2], 0)

        self.initialised = 1
        pass

    def redraw(self, *args, **named):
        if (self.initialised):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.draw_pointcloud()
            self.draw_cadaster()

            #print(self.xcenter, self.ycenter, self.zcenter, self.distance)

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