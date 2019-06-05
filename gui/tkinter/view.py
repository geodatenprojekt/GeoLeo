import random
from geoleo import pointcloud
from geoleo import cadaster
import geoleo.cadaster_reader as CadReader
from geoleo import util

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

points = ((0, 0, 0), (1, 1, 1))
width, height = 1300, 600  # window size

def draw_cordsystem():
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


def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()


def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINE)
    glColor3f(0, 1, 0)
    glVertex3fv((x1, y1, 0))
    glVertex3fv((x2, y2, 0))
    glEnd()

def draw_point(x, y, z, cr, cg, cb):
    glColor3d(cr,cg,cb)
    glVertex3d(x, y, z)


def refresh2d(width, height):
    #glViewport(0, 0, width, height)
    #glMatrixMode(GL_MODELVIEW)
    #glLoadIdentity()
    #glOrtho(left,right,bottom,top,zNear,zFar):pass
    #glOrtho(0.0, width, 0.0, height, 0, 1000)

    #gluPerspective(fovy, aspect, zNear, zFar)

    #glm::vec3 eye(3.0f, 3.0f, 3.0f);		// Hannes Ansicht: (1.0f, 10.0f, 5.0f)
    #glm::vec3 center(0.0f, 0.0f, 0.0f);
    #glm::vec3 up(0.0f, 1.0f, 0.0f);


    #gluLookAt(vehicleX, vehicleY + 20, vehicleZ, vehicleX, vehicleY, vehicleZ, 0.0, 0.0, 1.0); ---> this is what i need :)

    gluPerspective(90.0, width / height , 0.1, 20000)
    gluLookAt(0,1,0, 0,0,0, 0, 0, 1)
    #glLoadIdentity()


def cadaster():
    cad = cadaster.Cadaster()
    cad.buildings = CadReader.getBuildings("/example_data/cadaster_examples/LoD1_468_5751_1_NW.gml")


def init():
    pass

def redraw():
    pass

def draw():  # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    refresh2d(width, height)  # set mode to 2d

    draw_cordsystem()

    glPointSize(2)
    #glScale(0.05, 0.05, 0.05)
    glBegin(GL_POINTS)

    pcReader = pointcloud.PointCloudFileIO(util.getPathRelativeToRoot("/example_data/pointcloud_examples/47078_575419_0011.laz"))

    points = pcReader.getPointsWithColors(absolute=False)

    max = np.amax(points, axis=0)
    min = np.amin(points, axis=0)

    print(max[0])
    print(max[1])
    print(max[2])

    print(min[0])
    print(min[1])
    print(min[2])

    hundred = 1
    xmax = max[0] / hundred
    ymax = max[1] / hundred
    zmax = max[2] / hundred

    xmin = min[0] / hundred
    ymin = min[1] / hundred
    zmin = min[2] / hundred

    print(xmax)
    print(ymax)
    print(zmax)

    '''for point in points:
        point[0] /= xmax
        point[1] /= ymax
        point[2] /= zmax
    '''
    print(points[0])

    print(np.amax(points, axis=0))
    print(np.amin(points, axis=0))

    for point in points:
        #print(point[0], point[1], point[2])
        draw_point(point[0], point[1], point[2], point[3] / 65536, point[4] / 65536, point[5] / 65536)

    #draw_line(0, 0, 0, 5)
    #draw_line(5, 5, 0, 0)

    glEnd()
    glFlush()
    #draw_rect(0, 0, 1, 1)  # rect at (10, 10) with width 200, height 100

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("Geodatenprojekt")
glutDisplayFunc(draw)
#glutIdleFunc(draw)
glutMainLoop()