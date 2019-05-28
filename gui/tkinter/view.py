import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

points = ((0, 0, 0), (1, 1, 1))
width, height = 1920, 1080  # window size

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()


def draw_point(x, y, z, cx, cy, cz):
    #glPointSize(5.0)

    #glVertex3f(x, y, z)
    #glVertex3i(x, y, z)
    glColor3f(cx, cy, cz)
    glVertex3d(x, y, z)
    #glVertex2i(x, height - y)


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glOrtho(left,right,bottom,top,zNear,zFar):pass
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glLoadIdentity()


def draw():  # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    refresh2d(width, height)  # set mode to 2d

    #glColor3f(1, 1, 1)  # set color to blue

    glPointSize(1.0)
    glScale(0.01, 0.01, 0.01)
    glBegin(GL_POINTS)

    #draw_point(0, 0, 0)
    #draw_point(100, 100, 0)
    #draw_point(-100, -100, 0)



    xmax = 100
    xmin = -100
    ymax = 100
    ymin = -100

    # 0 0
    # 1 1
    # ....
    # 11000 11000

    max = 11000

    points = []
    for i in range(0, 1000000):
        points.append([random.randint(-max, max), random.randint(-max, max), random.randint(-max, max), random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255])

    calc = max / 100

    for x in points:
        x[0] /= calc
        x[1] /= calc
        x[2] /= calc


    for x in points:
        draw_point(x[0], x[1], x[2], x[3], x[4], x[5])

    glEnd()
    glFlush()
    #draw_rect(10, 10, 200, 100)  # rect at (10, 10) with width 200, height 100

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("Geodatenprojekt")
glutDisplayFunc(draw)
#glutIdleFunc(draw)
glutMainLoop()