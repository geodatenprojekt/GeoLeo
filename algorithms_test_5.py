from geoleo import algorithms
from geoleo import cadaster
from geoleo.pointcloud import PointCloudFileIO
import geoleo.cadaster_reader as CadReader
import geoleo.util as util
import os

#==========GET LAS FILES & PRE PROCESS=====================
filesList = list()
[filesList.append("example_data/pointcloud_examples/"+x) if x.endswith(".las") else x for x in os.listdir("example_data/pointcloud_examples")]

print("Pre processing las files..")
preProcessed = algorithms.preProcessLasFiles(filesList)
#==========================================================

cadasterPaths = list()
[cadasterPaths.append("example_data/cadaster_examples/"+x) if x.endswith(".gml") else x for x in os.listdir("example_data/cadaster_examples")]

i = 0
max = len(cadasterPaths)

for cadasterPath in cadasterPaths:

    cad = cadaster.Cadaster()
    cad.buildings = CadReader.getBuildings(cadasterPath)

    # firstBuildingDict = algorithms.getLasFilesForFirstBuilding(cad.buildings, filesList, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))
    #
    # if(firstBuildingDict != None):
    #     print("Found building:")
    #     for key, value in firstBuildingDict.items():
    #         util.printBuildingPoints(key)
    #         for lasFile in value:
    #             print("\tLas File: {}".format(lasFile))
    #             pcr = PointCloudFileIO(lasFile)
    #             print("Points count in pointcloud: {}".format(len(pcr.file.get_x())))



    print("Found buildings: {}".format(len(cad.buildings)))

    print("Pre processing gml files..")
    algorithms.preProcessBuildingList(cad.buildings, pointLeeway=0.1)

    print("\n\n\n")

    print("Combining buildings parts to whole buildings..")
    buildingsCombined = algorithms.combineBuildingsToGroups(cad.buildings)
    # buildingsCombined = cad.buildings

    print("Count after combine: {}".format(len(buildingsCombined)))

    #==========SIMPLE CUT OUT PROCESS=====================
    print("Getting las files for building...")
    ret = algorithms.getLasFilesForBuildings(buildingsCombined, filesList, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))

    groupedByPointclouds = algorithms.groupBuildingsByPointclouds(ret)

    for concattedPaths, group in groupedByPointclouds.items():
        print("Paths:\n{}".format("\n\t".join(util.getPointcloudsFromConcated(concattedPaths))))
        print("Buildings count: {}".format(len(group)))


    #
    # for building, buildingInfo in ret.items():
    #     hasPointsInPointCloud = True in buildingInfo[0]
    #     if(not hasPointsInPointCloud):
    #         continue
    #     paths = buildingInfo[1]
    #     pcr = PointCloudFileIO(paths[0])
    #     if(len(paths) > 1):
    #         pcr.mergePointClouds(paths[1:], "temp.las")
    #         del(pcr)
    #         pcr = PointCloudFileIO("temp.las")
    #     algorithms.cutBuildingFromPointcloud(pcr, building, "cut_with")
    # #==========================================================
    # i += 1
    # util.printProgressToConsole(i, max, "Cadaster List: ")




# countGroups = 0
# for buildingGroup in buildingsCombined:
#     if(len(buildingGroup) > 1):
#         print("Found building group with more than 1 building")
#         countGroups += 1
# print("Real building groups count: {}".format(countGroups))

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
