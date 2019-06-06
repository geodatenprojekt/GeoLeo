import tkinter as Tk
from OpenGL import GL, GLU
from pyopengltk import Opengl
from geoleo import pointcloud
from geoleo import util

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

    def init_pointcloud(self):
        pcReader = pointcloud.PointCloudFileIO(
            util.getPathRelativeToRoot("/example_data/pointcloud_examples/47078_575419_0011.laz"))
        self.points = pcReader.getPointsWithColors(absolute=False)

    def draw_pointcloud(self):
        GL.glBegin(GL.GL_POINTS)
        print(self.points.__len__())
        for point in self.points:
            GL.glColor3d(point[3] / 65536, point[4] / 65536, point[5] / 65536)
            GL.glVertex3d(point[0], point[2], point[1])
        GL.glEnd()


    def initgl(self):
        self.set_background(173 / 255, 203 / 255, 255 / 255)
        self.set_eyepoint(20000)
        #GL.GL_MATRIX_MODE
        GL.glPointSize(2)
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
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.yspin += 1
        print(self.yspin)

        self.draw_cordsystem()
        self.draw_pointcloud()


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