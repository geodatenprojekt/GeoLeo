from geoleo import algorithms
from geoleo import cadaster
from geoleo.pointcloud import PointCloudFileIO
import geoleo.cadaster_reader as CadReader
import os


filesList = list()
[filesList.append("example_data/pointcloud_examples/"+x) if x.endswith(".las") else x for x in os.listdir("example_data/pointcloud_examples")]

preProcessed = algorithms.preProcessLasFiles(filesList)

allPaths = []

cad = cadaster.Cadaster()
cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")



ret = algorithms.getLasFilesForBuildings(cad.buildings, filesList, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]))

for building, buildingInfo in ret.items():
    hasPointsInPointCloud = True in buildingInfo[0]
    if(not hasPointsInPointCloud):
        continue
    paths = buildingInfo[1]
    pcr = PointCloudFileIO(paths[0])
    pcr.mergePointClouds(paths[1:], "joined_testing_cut.las")
    del(pcr)
    pcr = PointCloudFileIO("joined_testing_cut.las")
    algorithms.cutBuildingFromPointcloud(pcr, building, "joined_after_cut.las")
    break
