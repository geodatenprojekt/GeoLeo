from geoleo.pointcloud import PointCloudFileIO
from geoleo import cadaster
import geoleo.cadaster_reader as CadReader
import geoleo.util as util
from shapely.geometry import Point, Polygon
import numpy as np
import os

"""
Return:
buildingsFound = {building1: ((True, True, True, True, ...), (pathToFile1, pathToFile2, ...)), building2: [...]}
"""
def getLasFilesForBuildings(buildings, filePathList, skipLazFiles=False):
    for lasFile in filePathList:
        if(not skipLazFiles and lasFile.endswith(".laz")):
            continue

        # filePath = "{}/{}".format(lasFolderPath, lasFile)

        pcReader = PointCloudFileIO(util.getPathToFile(lasFile))
        low = pcReader.getLowestCoords()
        high = pcReader.getHighestCoords()

        eckpunkt1 = (low[0], low[1])
        eckpunkt2 = (high[0], low[1])
        eckpunkt3 = (high[0], high[1])
        eckpunkt4 = (low[0], high[1])

        bounds = Polygon([eckpunkt1, eckpunkt2, eckpunkt3, eckpunkt4])
        print("Polygon: (({:.3f}, {:.3f}), ({:.3f}, {:.3f}), ({:.3f}, {:.3f}), ({:.3f}, {:.3f}))".format(eckpunkt1[0], eckpunkt1[1], eckpunkt2[0], eckpunkt2[1], eckpunkt3[0], eckpunkt3[1], eckpunkt4[0], eckpunkt4[1]))

        buildingsFound = {}

        for building in buildings:#(470958.666, 5754256.334, 131.36)
            if(building.coordinates[0].x <= 470780.00 or building.coordinates[0].x >= 471980.00 or building.coordinates[0].y <= 5753950.000 or building.coordinates[0].y >= 5755390.000):
                continue

            pointsFound = []
            pathsFound = []

            for buildingPoint in building.coordinates:
                point = Point(buildingPoint.x, buildingPoint.y)

                if(bounds.contains(point)):
                    print("Pointcloud contains point [{} {}]".format(buildingPoint.x, buildingPoint.y))
                    pointsFound.append(True)
                    if(not filePath in pathsFound):
                        pathsFound.append(lasFile)
                else:
                    print("Pointcloud does not contain point [{} {}]".format(buildingPoint.x, buildingPoint.y))
                    pointsFound.append(False)

            buildingFound[building] = (pointsFound, pathsFound)

        return buildingsFound

cad = cadaster.Cadaster()
cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")

filesList = list()
[filesList.append(x) if x.endswith(".las") else x for x in os.listdir("example_data/pointcloud_examples")]

ret = getLasFilesForBuildings(cad.buildings, filesList)
print(ret)


    # print("Buildings containing a point in the pointcloud:")
    # for building, points in buildings.items():
    #     if(not True in points):
    #         continue
    #     print("Building points count: {}, points count {}".format(len(building.coordinates), len(points)))
    #     i = 0
    #     for p in building.coordinates:
    #         isInString = ""
    #         if(points[i] == True):
    #             isInString = " => Is inside bounds"
    #         print("Point: ({}, {}, {}){}".format(p.x, p.y, p.z, isInString))
    #         i += 1
    #     if(len(buildingsPointclouds[building]) != 0):
    #         print("Building is in following pointclouds:")
    #         for path in buildingsPointclouds[building]:
    #             print(path)
