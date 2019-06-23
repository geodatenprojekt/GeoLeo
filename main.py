from geoleo import cmdargs
from geoleo import cadaster
from geoleo import pointcloud
from geoleo import algorithms
from geoleo import file_helper
from geoleo import algorithms
from geoleo import util
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def logState(current, max, precedent=""):
    logger.info("{}{:.2f}%".format(precedent, (current / max) * 100))

#========= GET PARAMETERS =====================
cmd = cmdargs.Parameters()

cadPath = cmd.getCadasterPath()
pcPath = cmd.getPointCloudPath()
outputPath = cmd.getOutputPath()
xOffset = cmd.getXOffset()
yOffset = cmd.getYOffset()

#for testing
if cadPath is None:
    cadPath = "example_data/cadaster_examples_test"
if pcPath is None:
    pcPath = "example_data/pointcloud_examples"
if outputPath is None:
    outputPath = "output"

#========= GET LAS FILES ==========
las_files = list()
logger.info("Reading LAS files..")
las_files = file_helper.get_all_paths_from_dir(pcPath, ".las")

#========= GET CADASTER ========================
cad = cadaster.Cadaster()
cad_files = file_helper.get_all_paths_from_dir(cadPath, ".gml")
logger.info("Reading GML files..")
#i = 0
#for file_name in file_names:
#    if i < 6:
#        cad.get_buildings(file_name)
#    i += 1
cad.get_buildings(cad_files[0])
cad.get_buildings(cad_files[1])
cad.get_buildings(cad_files[2])
#cad.get_buildings(cad_files[3])
#cad.get_buildings(cad_files[4])
#cad.get_buildings(cad_files[5])

logger.debug("Found buildings: {}".format(len(cad.buildings)))

#========= PRE PROCESS ======================================
logger.info("Pre processing LAS files..")
preProcessed = algorithms.preProcessLasFiles(las_files, callback=logState)

logger.info("Pre processing GML files..")
algorithms.preProcessBuildingList(cad.buildings, pointLeeway=0.1, callback=logState)

logger.info("Combining buildings parts to whole buildings..")
buildingsCombined = algorithms.combineBuildingsToGroups(cad.buildings)
logger.debug("Count after combine: {}".format(len(buildingsCombined)))

#========= CUT OUT PROCESS ==================================
logger.info("Getting LAS files for buildings..")
ret = algorithms.getLasFilesForBuildings(buildingsCombined, las_files, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]), callback=logState)
groupedByPointclouds = algorithms.groupBuildingsByPointclouds(ret)

logger.debug("==========CHECK LISTS===========")
if len(las_files) < 1:
    logger.debug("LAS_FILES EMPTY")
else:
    logger.debug("LAS_FILES[0]: {}".format(las_files[0]))
if len(cad_files) < 1:
    logger.debug("CAD_FILES EMPTY")
else:
    logger.debug("CAD_FILES[0]: {}".format(cad_files[0]))
if len(buildingsCombined) < 1:
    logger.debug("BUILDINGSCOMBINED EMPTY")
else:
    logger.debug("BUILDINGSCOMBINED[0].COORDINATES[0].X: {}".format(buildingsCombined[0].coordinates[0].x))
if len(preProcessed) < 1:
    logger.debug("PREPROCESSED EMPTY")
else:
    logger.debug("PREPROCESSED[0]: {}".format(preProcessed[0]))
if len(ret) < 1:
    logger.debug("RET EMPTY")
else:
    logger.debug("RET[0]: {}".format(ret[0]))
if len(groupedByPointclouds) < 1:
    logger.debug("GROUPEDBYPOINTCLOUDS EMPTY")
else:
    logger.debug("GROUPEDBYPOINTCLOUDS[0]: {}".format(groupedByPointclouds[0]))

for concattedPath, group in groupedByPointclouds.items():
    paths = util.getPointcloudsFromConcated(concattedPath)
    if paths == None:
        logger.warning("Pointcloud files where too small, building ignored")
        continue
    pcrs = []
    pointsList = []
    pointsWriteableList = []
    boundsList = []

    for path in paths:
        pcr = PointCloudFileIO(path)
        pcrs.append(pcr)
        pointsWriteableList.append(pcr.file.points)
        bounds = []
        bounds.append(pcr.getHighestCoords())
        bounds.append(pcr.getLowestCoords())
        boundsList.append(bounds)

    for building in group:
        algorithms.cutBuildingFromPointcloud(pointsList, pointsWriteableList, boundsList, pcrs[0].file.header, building,outputPath)
        buildingCount += 1
        logger.debug("Building Count: {}".format(buildingCount))


