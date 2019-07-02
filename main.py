from geoleo import cmdargs
from geoleo import cadaster
from geoleo import pointcloud
from geoleo import algorithms
from geoleo import file_helper
from geoleo import algorithms
from geoleo import util
from geoleo.pointcloud import PointCloudFileIO
import os
import logging
import platform

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def logState(current, max, precedent=""):
    logger.info("{}{:.2f}%".format(precedent, (current / max) * 100))

def dontPrint(current, max, precedent=""):
    pass

#========= GET PARAMETERS =====================
cmd = cmdargs.Parameters()

cadPath = cmd.getCadasterPath()
pcPath = cmd.getPointCloudPath()
outputPath = cmd.getOutputPath()
xOffset = cmd.getXOffset()
yOffset = cmd.getYOffset()


#for testing
if cadPath is None:
    cadPath = "example_data/cadaster_examples"
    logger.info("Using default path Cadasters: {}".format(cadPath))
if pcPath is None:
    pcPath = "example_data/pointcloud_examples"
    logger.info("Using default path for Pointclouds: {}".format(pcPath))
if outputPath is None:
    outputPath = "output"
    logger.info("Using default output path: {}".format(outputPath))


if(not os.path.isdir(outputPath)):
    os.makedirs(outputPath)
    logger.info("Created output directory")

#========= GET LAS FILES ==========
las_files = list()
logger.info("Reading LAS files..")
las_files = file_helper.get_all_paths_from_dir(pcPath, ".las")
if len(las_files) < 1:
    laz_files = list()
    laz_files = file_helper.get_all_paths_from_dir(pcPath, ".laz")
    for laz_file in laz_files:
        if platform.system() == "Windows":
            util.unzipLAZFile(laz_file)
        else:
            util.unzipLAZFile(laz_file, "lib/laszip")
    las_files = file_helper.get_all_paths_from_dir(pcPath, ".las")

if len(las_files) < 1:
  logger.error("No LAS files found")
  exit()

#========= GET CADASTER ========================
cads_list = []
logger.info("Reading GML files..")
cad_files = file_helper.get_all_paths_from_dir(cadPath, ".gml")
if len(cad_files) < 1:
  logger.error("No GML files found")
  exit()
totalBuildings = 0

for cad_file in cad_files:
    cad = cadaster.Cadaster()
    cad.get_buildings(cad_file)
    if(xOffset != 0 or yOffset != 0):
        logger.info("Shifting Cadaster coordinates by ({}, {})".format(xOffset, yOffset))
        algorithms.shiftCadasterCoordinates(cad.buildings, (xOffset, yOffset))
    totalBuildings += len(cad.buildings)
    cads_list.append(cad)

logger.debug("Found buildings: {}".format(totalBuildings))

#========= PRE PROCESS ======================================
logger.info("Pre processing LAS files..")
preProcessed = algorithms.preProcessLasFiles(las_files, callback=dontPrint)



# logger.info("Pre processing GML files..")
max = len(cads_list)
current = 0
logger.info("Pre processing GML files.. {:.2f}%".format((current / max) * 100))
for cad in cads_list:
    algorithms.preProcessBuildingList(cad.buildings, pointLeeway=0.1, callback=dontPrint)
    current += 1
    logger.info("Pre processing GML files.. {:.2f}%".format((current / max) * 100))

logger.info("Combining buildings parts to whole buildings..")
buildingsCombinedAll = []
totalAfterCombine = 0
current = 0
logger.info("Combining buildings parts to whole buildings.. {:.2f}%".format((current / max) * 100))
for cad in cads_list:
    buildingsCombined = algorithms.combineBuildingsToGroups(cad.buildings)
    buildingsCombinedAll.append(buildingsCombined)
    totalAfterCombine += len(buildingsCombined)
    current += 1
    logger.info("Combining buildings parts to whole buildings.. {:.2f}%".format((current / max) * 100))

logger.debug("Count after combine: {}".format(totalAfterCombine))

#========= CUT OUT PROCESS ==================================
# logger.info("Getting LAS files for buildings..")
groupedByPointcloudsAll = []
totalBuildingsToBeProcessed = 0
current = 0
logger.info("Getting LAS files for buildings.. {:.2f}%".format((current / max) * 100))
for buildingsCombined in buildingsCombinedAll:
    ret = algorithms.getLasFilesForBuildings(buildingsCombined, las_files, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]), callback=dontPrint)
    groupedByPointclouds = algorithms.groupBuildingsByPointclouds(ret)
    groupedByPointcloudsAll.append(groupedByPointclouds)
    for pointcloudPath, group in groupedByPointclouds.items():
        totalBuildingsToBeProcessed += len(group)

    # totalGroups += len(groupedByPointclouds)
    current += 1
    logger.info("Getting LAS files for buildings.. {:.2f}%".format((current / max) * 100))

if len(groupedByPointcloudsAll) < 1:
  logger.error("No building found in pointclouds")
  exit()

buildingCount = 0
for groupedByPointclouds in groupedByPointcloudsAll:
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
            pointsList.append(pcr.getPoints())
            pointsWriteableList.append(pcr.file.points)
            bounds = []
            bounds.append(pcr.getHighestCoords())
            bounds.append(pcr.getLowestCoords())
            boundsList.append(bounds)

        for building in group:
            algorithms.cutBuildingFromPointcloud(pointsList, pointsWriteableList, boundsList, pcrs[0].file.header, building, outputPath)
            buildingCount += 1
            logger.info("Building Cut Progress: {:.2f}%".format((buildingCount / totalBuildingsToBeProcessed) * 100))

logger.info("Cut Progress finished")
