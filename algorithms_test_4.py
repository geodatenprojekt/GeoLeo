from geoleo import algorithms
from geoleo import cadaster
from geoleo.pointcloud import PointCloudFileIO
import geoleo.cadaster_reader as CadReader
import os

cad = cadaster.Cadaster()
cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")

def printPoint(point):
    print("Point at ({}, {})".format(point.x, point.y))

def printAllPoints(building):
    for point in building.coordinates:
        printPoint(point)

print("Found buildings: {}".format(len(cad.buildings)))

buildingsCombined = algorithms.combineBuildingsToGroups(cad.buildings)

print("Found building groups: {}".format(len(buildingsCombined)))

filesList = list()
[filesList.append("example_data/pointcloud_examples/"+x) if x.endswith(".las") else x for x in os.listdir("example_data/pointcloud_examples")]

preProcessed = algorithms.preProcessLasFiles(filesList)


ret = algorithms.getLasFilesForBuildings(buildingsCombined, filesList, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))

i = 0
for building, buildingInfo in ret.items():
    hasPointsInPointCloud = True in buildingInfo[0]
    if(not hasPointsInPointCloud):
        continue
    paths = buildingInfo[1]
    pcr = PointCloudFileIO(paths[0])
    pcr.mergePointClouds(paths[1:], "joined_testing_cut.las")
    del(pcr)
    pcr = PointCloudFileIO("joined_testing_cut.las")
    algorithms.cutBuildingFromPointcloud(pcr, building, "joined_after_cut_{}.las".format(i))
    i += 1

# uniquePoints = {}
# buildingGroups = []
# i = 0
# for building in cad.buildings:
#     for point in building.coordinates:
#         if(point in uniquePoints and uniquePoints[point] != i):
#             otherBuildingIndex = uniquePoints[point]
#             otherBuilding = cad.buildings[otherBuildingIndex]
#             print("Building({}) and Building({}) have a point in common: Point at ({}, {}, {})".format(i, otherBuildingIndex, point.x, point.y, point.z))
#             found = False
#             for buildingGroup in buildingGroups:
#                 if(otherBuilding in buildingGroup):
#                     if(not building in buildingGroup):
#                         buildingGroup.append(building)
#                         found = True
#             if(found == False):
#                 buildingGroups.append([building])
#         else:
#             uniquePoints[point] = i
#     i += 1
# print("Found building groups: {}".format(len(buildingGroups)))
# countGroups = 0
# for buildingGroup in buildingGroups:
#     if(len(buildingGroup) > 1):
#         print("Found building group with more than 1 building")
#         countGroups += 1
# print("Real building groups count: {}".format(countGroups))
