import tkinter as Tk
from OpenGL.GL import *
from gui.main_window.pyopengltk import Opengl
from geoleo import pointcloud
from geoleo import util
from geoleo import cadaster
from geoleo import file_helper
import numpy as np
import logging
from geoleo import algorithms
from gui.main_window.absolute_parser import AbsParser


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def logState(current, max, precedent=""):
    logger.info("{}{:.2f}%".format(precedent, (current / max) * 100))


def dontPrint(current, max, precedent=""):
    pass


class AppOgl(Opengl):
    initialised = 0

    def __init__(self, model, *args, **kw):
        self.pcPath = model.lasPath.get()
        self.cadPath = model.gmlPath.get()
        self.outputPath = ""

        self.model = model

        self.cloudlist = list()

        self.las_files = list()
        self.cads_list = list()

        self.points = list()
        self.buildings = list()

        super().__init__(*args, **kw)

    def read_las_files(self):
        # ========= GET LAS FILES ==========
        logger.info("Reading LAS files..")
        self.las_files = file_helper.get_all_paths_from_dir(self.pcPath, ".las")
        if not self.las_files or len(self.las_files) < 1:
            laz_files = list()
            laz_files = file_helper.get_all_paths_from_dir(self.pcPath, ".laz")
            if laz_files:
                for laz_file in laz_files:
                    if platform.system() == "Windows":
                        util.unzipLAZFile(laz_file)
                    else:
                        util.unzipLAZFile(laz_file, "lib/laszip")
                las_files = file_helper.get_all_paths_from_dir(self.pcPath, ".las")

        if not self.las_files or len(self.las_files) < 1:
            logger.error("No LAS files found")
            exit()

    def read_cadaster_files(self):
        logger.info("Reading GML files..")
        cad_files = file_helper.get_all_paths_from_dir(self.cadPath, ".gml")
        if len(cad_files) < 1:
            logger.error("No GML files found")
            exit()
        totalBuildings = 0

        for cad_file in cad_files:
            cad = cadaster.Cadaster()
            cad.get_buildings(cad_file)
            if self.model.moveX != 0 or self.model.moveY != 0:
                logger.info("Shifting Cadaster coordinates by ({}, {})".format(self.model.moveX, self.model.moveY))
                algorithms.shiftCadasterCoordinates(cad.buildings, (self.model.moveX, self.model.moveY))
            totalBuildings += len(cad.buildings)
            self.cads_list.append(cad)

        logger.debug("Found buildings: {}".format(totalBuildings))

    def init_view(self):
        logger.info("Pre processing LAS files..")
        preProcessed = algorithms.preProcessLasFiles(self.las_files, callback=logState)

        logger.info("Init Pointcloud View")

        ret = algorithms.getLasFilesForFirstBuilding(self.cads_list[0].buildings, self.las_files, preProcessed[4], maxBounds=(
        preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))

        self.cloudlist = glGenLists(1)
        glNewList(self.cloudlist, GL_COMPILE)
        glBegin(GL_POINTS)

        for building, paths in ret.items() :
            self.buildings.append(building)
            for path in paths:
                reader = pointcloud.PointCloudFileIO(path)
                for point in reader.getPointsWithColors(absolute=True):
                    self.points.append(point)

        points_max = np.amax(self.points, axis=0)
        points_min = np.amin(self.points, axis=0)

        self.parser = AbsParser(points_min, points_max)
        points = self.parser.parse_list(self.points)

        eye = self.parser.parse_coords(points_max[0], points_max[1], points_max[2])
        points_med = np.median(points, axis=0)

        self.set_eyepoint(eye[2] + max(eye[1], eye[0]))
        self.cam = (points_med[0], points_med[2], points_med[1])

        for point in points:
            glColor3d(point[3] / 65536, point[4] / 65536, point[5] / 65536)
            glVertex3d(point[0], point[2], point[1])
        glEnd()
        glEndList()

    def draw_cadaster(self):
        glColor3d(1, 0, 0)
        vertices = []
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for building in self.buildings:
            glBegin(GL_POLYGON)
            for coord in building.coordinates:
                x = self.parser.parse_coords(coord.x, coord.y, coord.z)
                glVertex3d(x[0] + self.model.moveX * 1000, x[2], x[1] + self.model.moveY * 1000)
                vertices.append((x[0] + self.model.moveX * 1000, x[2], x[1] + self.model.moveY * 1000))
            glEnd()

    def draw_pointcloud(self):
        if self.cloudlist:
            glCallList(self.cloudlist)

    def initgl(self):
        if not self.initialised:
            self.set_background(173 / 255, 203 / 255, 255 / 255)

            glPointSize(2)

            self.fovy = 60.0
            self.near = 0.1
            self.far = 999999999.0

            self.read_las_files()
            self.read_cadaster_files()

            self.init_view()

            glRotatef(90.0, 1., 0., 0.)
            self.set_centerpoint(self.cam[0], -self.cam[2], 0)

            self.initialised = 1

    def redraw(self, *args, **named):
        if self.initialised:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.draw_pointcloud()
            self.draw_cadaster()

            glFlush()