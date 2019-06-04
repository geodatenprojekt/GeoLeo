from geoleo import algorithms
from geoleo import cadaster
import geoleo.cadaster_reader as CadReader
import os

cad = cadaster.Cadaster()
cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")

filesList = list()
[filesList.append("example_data/pointcloud_examples/"+x) if x.endswith(".las") else x for x in os.listdir("example_data/pointcloud_examples")]



preProcessed = algorithms.preProcessLasFiles(filesList)
for path in filesList:
    print("\nPath:  {}".format(path))
    print("Local lowest:  {}".format(preProcessed[4][path][0]))
    print("Local highest: {}".format(preProcessed[4][path][1]))

print("\n\nGlobal lowest:  ({}, {})".format(preProcessed[0], preProcessed[1]))
print("Global highest: ({}, {})".format(preProcessed[2], preProcessed[3]))



ret = algorithms.getLasFilesForBuildings(cad.buildings, filesList, maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))
i = 1
buildingsCountInside = 0
uniquePaths = []
for building, buildingInfo in ret.items():
    hasPointsInPointCloud = True in buildingInfo[0]
    print("Building ({}){}".format(i, ":" if hasPointsInPointCloud else " - Not inside bounds"))
    i += 1
    if(not hasPointsInPointCloud):
        continue
    else:
        buildingsCountInside += 1
    for j in range(len(building.coordinates)):
        print("\tPoint ({:.3f}, {:.3f}) is {}".format(building.coordinates[j].x, building.coordinates[j].y, "inside" if buildingInfo[0][j] == True else "not inside"))
    for path in buildingInfo[1]:
        print("\tPath to pointcloud: '{}'".format(path))
        if(not path in uniquePaths):
            uniquePaths.append(path)

print("Buildings count: {}".format(len(ret)))
print("Buildings count inside pointcloud: {}".format(buildingsCountInside))
print("Unqie pointcloud files needed: {}".format(len(uniquePaths)))
print("Paths:")
for path in uniquePaths:
    print("\t'{}'".format(path))
