from geoleo.pointcloud import PointCloudFileIO
from geoleo import cadaster
import geoleo.cadaster_reader as CadReader
import geoleo.util as util
from shapely.geometry import Point, Polygon
import numpy as np
import os

# pcReader = PointCloudFileIO(util.getPathToFile("example_data/pointcloud_examples/47086_575419_0011.las"))
# low = pcReader.getLowestCoords()
# high = pcReader.getHighestCoords()
# diff = high - low;
# middle = low + diff/2

# print("Higher bounds: {}".format(high))
# print("Lower bounds: {}".format(low))
# print("Middle bounds: {}".format(middle))
# print("Difference bounds: {}".format(diff))

# lowRel = pcReader.getLowestCoords(False)
# highRel = pcReader.getHighestCoords(False)
# diffRel = highRel - lowRel;
# middleRel = lowRel + diffRel/2

# print("Higher bounds (relative): {}".format(highRel))
# print("Lower bounds (relative): {}".format(lowRel))
# print("Middle bounds (relative): {}".format(middleRel))
# print("Difference bounds (relative): {}".format(diffRel))


"""
Hier sieht man, dass im Durchschnitt zwischen den R, G und B Werten nur 20 unterschied ist, das sind automatisch Grautöne!
"""
# variance = 0
# count = 0
# for p in pcReader.getPointsWithColors()[0:20]:
    # print(type(p[3])) -> numpy.float64
    # r = (p[3]/65536)*255
    # g = (p[4]/65536)*255
    # b = (p[5]/65536)*255
    # maxVal = max(r, g, b)
    # minVal = min(r, g, b)
    # diff = maxVal - minVal
    # variance += diff
    # count += 1
    # print(p[3], p[4], p[5])
# print("average variance: {}".format(variance / count))

"""
Test for classifications other than 0
"""
# file = pcReader.getFile()
# points = np.vstack((file.x, file.y, file.z, file.classification, file.red, file.green, file.blue)).transpose()
# hadNonZero = False
# for p in points:
#     if(p[3] != 0):
#         hadNonZero = True
#         print("Found classification of '{}'".format(p[3]))


path = "example_data/pointcloud_examples"
cad = cadaster.Cadaster()
cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")
buildings = {}
buildingsPointclouds = {}
did = False

for lasFile in os.listdir(path):
    if(lasFile.endswith(".laz")):
        continue
    filePath = "{}/{}".format(path, lasFile)

    pcReader = PointCloudFileIO(util.getPathToFile(filePath))
    low = pcReader.getLowestCoords()
    high = pcReader.getHighestCoords()

    eckpunkt1 = (low[0], low[1])
    eckpunkt2 = (high[0], low[1])
    eckpunkt3 = (high[0], high[1])
    eckpunkt4 = (low[0], high[1])

    bounds = Polygon([eckpunkt1, eckpunkt2, eckpunkt3, eckpunkt4])
    print("Polygon: (({:.3f}, {:.3f}), ({:.3f}, {:.3f}), ({:.3f}, {:.3f}), ({:.3f}, {:.3f}))".format(eckpunkt1[0], eckpunkt1[1], eckpunkt2[0], eckpunkt2[1], eckpunkt3[0], eckpunkt3[1], eckpunkt4[0], eckpunkt4[1]))


    for building in cad.buildings:#(470958.666, 5754256.334, 131.36)
        # if(building.coordinates[0].x == 470958.666 and building.coordinates[0].y == 5754256.334 and building.coordinates[0].z == 131.36):
        if(building.coordinates[0].x <= 470780.00 or building.coordinates[0].x >= 471980.00 or building.coordinates[0].y <= 5753950.000 or building.coordinates[0].y >= 5755390.000):
            continue
        # else:
        #     continue
        i = 0

        buildingHad = False
        for buildingPoint in building.coordinates:
            point = Point(buildingPoint.x, buildingPoint.y)
            if(not building in buildings):
                buildings[building] = []
            if(not building in buildingsPointclouds):
                buildingsPointclouds[building] = []

            if(bounds.contains(point)):
                print("Pointcloud contains point [{} {}]".format(buildingPoint.x, buildingPoint.y))
                if(len(buildings[building]) == i):
                    buildings[building].append(True)
                else:
                    buildings[building][i] = True
                if(not filePath in buildingsPointclouds[building]):
                    buildingsPointclouds[building].append(filePath)
            else:
                print("Pointcloud does not contain point [{} {}]".format(buildingPoint.x, buildingPoint.y))
                if(len(buildings[building]) == i):
                    buildings[building].append(False)
            i += 1

print("Buildings containing a point in the pointcloud:")
for building, points in buildings.items():
    if(not True in points):
        continue
    print("Building points count: {}, points count {}".format(len(building.coordinates), len(points)))
    i = 0
    for p in building.coordinates:
        isInString = ""
        if(points[i] == True):
            isInString = " => Is inside bounds"
        print("Point: ({}, {}, {}){}".format(p.x, p.y, p.z, isInString))
        i += 1
    if(len(buildingsPointclouds[building]) != 0):
        print("Building is in following pointclouds:")
        for path in buildingsPointclouds[building]:
            print(path)

#points = pcReader.getPoints()
#print("\n")
#[print(x) for x in points[0:20]]
