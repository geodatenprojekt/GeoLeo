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
def getLasFilesForBuildings(buildings, filePathList, maxBounds=None):
    buildingsFound = {}

    for building in buildings:
        if(maxBounds != None and building.coordinates[0].x <= maxBounds[0] or building.coordinates[0].x >= maxBounds[2] or building.coordinates[0].y <= maxBounds[1] or building.coordinates[0].y >= maxBounds[3]):
            continue

        points = []
        paths = []

        for p in building.coordinates:
            points.append(False)

        buildingsFound[building] = (points, paths)

    for lasFile in filePathList:
        if(not lasFile.endswith(".las") and not lasFile.endswith(".laz")):
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

        for building in buildings:#(470958.666, 5754256.334, 131.36)
            if(maxBounds != None and building.coordinates[0].x <= maxBounds[0] or building.coordinates[0].x >= maxBounds[2] or building.coordinates[0].y <= maxBounds[1] or building.coordinates[0].y >= maxBounds[3]):
                continue

            i = 0
            for buildingPoint in building.coordinates:
                point = Point(buildingPoint.x, buildingPoint.y)

                if(bounds.contains(point)):
                    print("Pointcloud contains point [{} {}]".format(buildingPoint.x, buildingPoint.y))
                    buildingsFound[building][0][i] = True
                    if(not lasFile in buildingsFound[building][1]):
                        buildingsFound[building][1].append(lasFile)
                else:
                    print("Pointcloud does not contain point [{} {}]".format(buildingPoint.x, buildingPoint.y))
                i += 1

    return buildingsFound

"""
return = [globalLowestX, globalLowestY, globalHighestX, globalHighestY, {lasFile: (lowestCoords, highestCoords), lasFile2: (...), ...}]
"""
def preProcessLasFiles(filePathList):
    firstFile = filePathList[0]
    firstFileReader = PointCloudFileIO(util.getPathToFile(firstFile))

    low = firstFileReader.getLowestCoords()
    high = firstFileReader.getHighestCoords()

    globalLowestX = low[0]
    globalLowestY = low[1]
    globalHighestX = high[0]
    globalHighestY = high[1]

    coordsForPaths = {}

    for lasFile in filePathList:
        lasFileReader = PointCloudFileIO(util.getPathToFile(lasFile))

        lowestCoords = lasFileReader.getLowestCoords()
        highestCoords = lasFileReader.getHighestCoords()

        if(lowestCoords[0] < globalLowestX):
            globalLowestX = lowestCoords[0]
        if(lowestCoords[1] < globalLowestY):
            globalLowestY = lowestCoords[1]

        if(highestCoords[0] > globalHighestX):
            globalHighestX = highestCoords[0]
        if(highestCoords[1] > globalHighestY):
            globalHighestY = highestCoords[1]

        coordsForPaths[lasFile] = (lowestCoords, highestCoords)

    return [globalLowestX, globalLowestY, globalHighestX, globalHighestY, coordsForPaths]
