from geoleo import algorithms
from geoleo import cadaster
from geoleo.pointcloud import PointCloudFileIO
import geoleo.cadaster_reader as CadReader
import geoleo.util as util
import os, sys

# print("Modules:\n{}".format("\n".join(sys.modules)))

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
buildingCount = 0

for cadasterPath in cadasterPaths:

    cad = cadaster.Cadaster()
    cad.buildings = CadReader.getBuildings(cadasterPath)
    print("Found buildings: {}".format(len(cad.buildings)))

    print("Pre processing gml files..")
    algorithms.preProcessBuildingList(cad.buildings, pointLeeway=0.1)

    print("\n\n\n")

    print("Combining buildings parts to whole buildings..")
    buildingsCombined = algorithms.combineBuildingsToGroups(cad.buildings)

    print("Count after combine: {}".format(len(buildingsCombined)))

    #==========SIMPLE CUT OUT PROCESS=====================
    print("Getting las files for building...")
    ret = algorithms.getLasFilesForBuildings(buildingsCombined, filesList, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))

    print("Grouping buildings by pointclouds used...")
    groupedByPointclouds = algorithms.groupBuildingsByPointclouds(ret)
    print("Found groups: {}".format(len(groupedByPointclouds)))

    print("Cutting pointclouds...")
    for concattedPath, group in groupedByPointclouds.items():
        paths = util.getPointcloudsFromConcated(concattedPath)
        if(paths == None):
            print("Pointcloud files where too small, building ignored...")
            continue
        pcrs = []
        pointsList = []
        pointsWritableList = []
        boundsList = []

        for path in paths:
            pcr = PointCloudFileIO(path)
            pcrs.append(pcr)
            pointsList.append(pcr.getPoints())
            pointsWritableList.append(pcr.file.points)
            bounds = []
            bounds.append(pcr.getHighestCoords())
            bounds.append(pcr.getLowestCoords())
            boundsList.append(bounds)

        for building in group:
            algorithms.cutBuildingFromPointcloud(pointsList, pointsWritableList, boundsList, pcrs[0].file.header, building, "cut_with")
            buildingCount += 1
            print("Building Count: {}".format(buildingCount))

print("Cut a total of {} buildings.".format(buildingCount))
print("Runtime specifics:")
util.printTimerResult()


"""
Last test:
Timer 'preProcessLasFiles': 0.784s
Timer 'preProcessBuildingList': 88.786s
Timer 'combineBuildingsToGroups': 0.085s
Timer 'combineBuildingGroup': 1.362s
Timer 'getLasFilesForBuildings': 1.602s
Timer 'groupBuildingsByPointclouds': 1.802s
Timer 'cutBuildingFromPointcloud': 3583.275s

Time without PIP:
Timer 'preProcessLasFiles': 1.060s
Timer 'preProcessBuildingList': 86.851s
Timer 'combineBuildingsToGroups': 0.086s
Timer 'combineBuildingGroup': 1.300s
Timer 'getLasFilesForBuildings': 1.261s
Timer 'groupBuildingsByPointclouds': 1.197s
Timer 'cutBuildingFromPointcloud': 215.203s     <--- That's a difference of 3.368,072‬
"""
