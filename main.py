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
logger.setLevel(logging.DEBUG)

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
if pcPath is None:
    pcPath = "example_data/pointcloud_examples"
if outputPath is None:
    outputPath = "output"

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

#========= GET CADASTER ========================
cads_list = []
cad_files = file_helper.get_all_paths_from_dir(cadPath, ".gml")
logger.info("Reading GML files..")
#i = 0
#for file_name in file_names:
#    if i < 6:
#        cad.get_buildings(file_name)
#    i += 1
totalBuildings = 0
for cad_file in cad_files:
    cad = cadaster.Cadaster()
    cad.get_buildings(cad_file)
    totalBuildings += len(cad.buildings)
    cads_list.append(cad)
# cad.get_buildings(cad_files[0])
#cad.get_buildings(cad_files[1])
#cad.get_buildings(cad_files[2])
#cad.get_buildings(cad_files[3])
#cad.get_buildings(cad_files[4])
#cad.get_buildings(cad_files[5])

logger.debug("Found buildings: {}".format(totalBuildings))

#========= PRE PROCESS ======================================
logger.info("Pre processing LAS files..")
preProcessed = algorithms.preProcessLasFiles(las_files, callback=logState)



logger.info("Pre processing GML files..")
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
logger.info("Getting LAS files for buildings..")
groupedByPointcloudsAll = []
totalGroups = 0
current = 0
logger.info("Getting LAS files for buildings.. {:.2f}%".format((current / max) * 100))
for buildingsCombined in buildingsCombinedAll:
    ret = algorithms.getLasFilesForBuildings(buildingsCombined, las_files, preProcessed[4], maxBounds=(preProcessed[0], preProcessed[1], preProcessed[2], preProcessed[3]), callback=dontPrint)
    groupedByPointclouds = algorithms.groupBuildingsByPointclouds(ret)
    groupedByPointcloudsAll.append(groupedByPointclouds)
    totalGroups += len(groupedByPointclouds)
    current += 1
    logger.info("Getting LAS files for buildings.. {:.2f}%".format((current / max) * 100))

# logger.debug("==========CHECK LISTS===========")
# if len(las_files) < 1:
#     logger.debug("LAS_FILES EMPTY")
# else:
#     logger.debug("LAS_FILES[0]: {}".format(las_files[0]))
# if len(cad_files) < 1:
#     logger.debug("CAD_FILES EMPTY")
# else:
#     logger.debug("CAD_FILES[0]: {}".format(cad_files[0]))
# if len(buildingsCombined) < 1:
#     logger.debug("BUILDINGSCOMBINED EMPTY")
# else:
#     logger.debug("BUILDINGSCOMBINED[0].COORDINATES[0].X: {}".format(buildingsCombined[0].coordinates[0].x))
# if len(preProcessed) < 1:
#     logger.debug("PREPROCESSED EMPTY")
# else:
#     logger.debug("PREPROCESSED[0]: {}".format(preProcessed[0]))
# if len(ret) < 1:
#     logger.debug("RET EMPTY")
# else:
#     pass
#     logger.debug("RET[0]: {}".format(ret[0])) # Auf Dictionaries kann man nicht mit Indizes zugreifen
# if len(groupedByPointclouds) < 1:
#     logger.debug("GROUPEDBYPOINTCLOUDS EMPTY")
# else:
#     pass
#     logger.debug("GROUPEDBYPOINTCLOUDS[0]: {}".format(groupedByPointclouds[0])) # Auf Dictionaries kann man nicht mit Indizes zugreifen

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
            logger.info("Building Cut Progress: {:.2f}%".format((buildingCount / totalAfterCombine) * 100))
