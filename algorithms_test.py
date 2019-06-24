from geoleo import algorithms
from geoleo import cadaster
from geoleo.pointcloud import PointCloudFileIO
import geoleo.cadaster_reader as CadReader
import os


filesList = list()
[filesList.append("example_data/pointcloud_examples/"+x) if x.endswith(".las") else x for x in os.listdir("example_data/pointcloud_examples")]

preProcessed = algorithms.preProcessLasFiles(filesList)

cadasterPaths = list()
[cadasterPaths.append("example_data/cadaster_examples/"+x) if x.endswith(".gml") else x for x in os.listdir("example_data/cadaster_examples")]

allPaths = []

for cadPath in cadasterPaths:

    cad = cadaster.Cadaster()
    # cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")
    cad.buildings = CadReader.getBuildings(cadPath)

    # preProcessed = algorithms.preProcessLasFiles(filesList)
    # for path in filesList:
    #     pass
        #print("\nPath:  {}".format(path))
        #print("Local lowest:  {}".format(preProcessed[4][path][0]))
        #print("Local highest: {}".format(preProcessed[4][path][1]))

    # print("\n\nGlobal lowest:  ({}, {})".format(preProcessed[0], preProcessed[1]))
    # print("Global highest: ({}, {})".format(preProcessed[2], preProcessed[3]))



    ret = algorithms.getLasFilesForBuildings(cad.buildings, filesList, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))
    i = 1
    buildingsCountInside = 0
    uniquePaths = []
    for building, buildingInfo in ret.items():
        hasPointsInPointCloud = True in buildingInfo[0]
        #print("Building ({}){}".format(i, ":" if hasPointsInPointCloud else " - Not inside bounds"))
        i += 1
        if(not hasPointsInPointCloud):
            continue
        else:
            buildingsCountInside += 1

        for j in range(len(building.coordinates)):
            pass
            #print("\tPoint ({:.3f}, {:.3f}) is {}".format(building.coordinates[j].x, building.coordinates[j].y, "inside" if buildingInfo[0][j] == True else "not inside"))
        for path in buildingInfo[1]:
            #print("\tPath to pointcloud: '{}'".format(path))
            if(not path in uniquePaths):
                uniquePaths.append(path)
            if(not path in allPaths):
                allPaths.append(path)

    # paths = ["example_data/pointcloud_examples/47102_575411_0011.las", "example_data/pointcloud_examples/47102_575419_0011.las"]

    print("Buildings count: {}".format(len(ret)))
    print("Buildings count inside pointcloud: {}".format(buildingsCountInside))
    print("Unique pointcloud files needed: {}\n\n".format(len(uniquePaths)))
    # print("Paths:")
    # pcr = PointCloudFileIO(uniquePaths[0])
    # pcrs = []
    # for path in uniquePaths:
    #     print("\t'{}'".format(path))
    #     if(not path in allPaths):
    #         allPaths.append(path)
        # pcr = PointCloudFileIO(path)
        # pcrs.append(pcr)
print("Paths:")
for path in allPaths:
    print("\t'{}'".format(path))

    # pcr.mergePointClouds(uniquePaths, "joined_3.las")
    #
    # pcr2 = PointCloudFileIO("joined_3.las")
    # print("old max: {}".format(pcr.header.max))
    # print("old min: {}".format(pcr.header.min))
    # print("")
    # print("new max: {}".format(pcr2.header.max))
    # print("new min: {}".format(pcr2.header.min))
