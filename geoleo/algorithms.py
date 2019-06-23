from geoleo.pointcloud import PointCloudFileIO
from geoleo import cadaster
import geoleo.cadaster_reader as CadReader
import geoleo.util as util
from shapely import affinity
from shapely.geometry import Point, Polygon
from shapely.ops import cascaded_union
import numpy as np
import os

"""
Shifts all buildings by a given offset
@param buildings  A list of buildings to be shifted
@param offset  The offset by which the buildings should be shifted
"""
def shiftCadasterCoordinates(buildings, offset):
    for building in buildings:
        for coordinate in building.coordinates:
            coordinate.x += offset[0]
            coordinate.y += offset[1]

"""
Filters all of the PointClouds and searches for the buildings inside them
@param buildings  A list of buildings used for the search
@param filePathList  A list of paths to .las/.laz files
@param lasBoundsDict  A dictionary which holds the bounds for a given .las File
@param maxBounds  Optional: The maximum bounds used to filter the buildings beforehands
@return A dictionary of the form {building1: ((True, True, True, True, ...), (pathToFile1, pathToFile2, ...)), building2: [...]}
"""
def getLasFilesForBuildings(buildings, filePathList, lasBoundsDict, maxBounds=None, callback=util.printProgressToConsole):
    buildingsFound = {}

    count = len(filePathList)
    currentFileIndex = 0

    callback(currentFileIndex, count)

    for building in buildings:
        if(maxBounds != None and building.coordinates[0].x <= maxBounds[0] or building.coordinates[0].x >= maxBounds[2] or building.coordinates[0].y <= maxBounds[1] or building.coordinates[0].y >= maxBounds[3]):
            continue

        points = []
        paths = []

        for p in building.coordinates:
            points.append(False)

        buildingsFound[building] = (points, paths)

    for lasFile in filePathList:
        low = lasBoundsDict[lasFile][0]
        high = lasBoundsDict[lasFile][1]

        for building in buildingsFound.keys():#(470958.666, 5754256.334, 131.36)
            i = 0
            for buildingPoint in building.coordinates:
                if(buildingPoint.x > low[0] and buildingPoint.x < high[0] and buildingPoint.y > low[1] and buildingPoint.y < high[1]):
                    buildingsFound[building][0][i] = True
                    if(not lasFile in buildingsFound[building][1]):
                        buildingsFound[building][1].append(lasFile)
                else:
                    pass
                i += 1

        currentFileIndex += 1
        callback(currentFileIndex, count)

    return buildingsFound

"""
Returns the first found building with the according pointcloud files
@param buildings  A list of buildings used for the search
@param filePathList  A list of paths to .las/.laz files
@param lasBoundsDict  A dictionary which holds the bounds for a given .las File
@param maxBounds  Optional: The maximum bounds used to filter the buildings beforehands
@return If found, a dictionary with ONE entry of the form {building: ((True, True, True, True, ...), (pathToFile1, pathToFile2, ...))}
        If not found, None
"""
def getLasFilesForFirstBuilding(buildings, filePathList, lasBoundsDict, maxBounds=None):
    buildingsFound = {}

    for building in buildings:
        if(maxBounds != None and building.coordinates[0].x <= maxBounds[0] or building.coordinates[0].x >= maxBounds[2] or building.coordinates[0].y <= maxBounds[1] or building.coordinates[0].y >= maxBounds[3]):
            continue

        points = []
        paths = []

        for p in building.coordinates:
            points.append(False)

        buildingsFound[building] = (points, paths)

    for building in buildingsFound.keys():
        for lasFile in filePathList:
            low = lasBoundsDict[lasFile][0]
            high = lasBoundsDict[lasFile][1]

            i = 0
            for buildingPoint in building.coordinates:
                if(buildingPoint.x > low[0] and buildingPoint.x < high[0] and buildingPoint.y > low[1] and buildingPoint.y < high[1]):
                    # print("Found point({})".format(i))
                    buildingsFound[building][0][i] = True
                    if(not lasFile in buildingsFound[building][1]):
                        buildingsFound[building][1].append(lasFile)
                else:
                    pass
                i += 1


        if(not False in buildingsFound[building][0]): #One building was inside one or more pointclouds entirely
            return {building: buildingsFound[building][1]}

    return None

"""
Returns multiple buildings, for each cadaster one building, if one was found
"""

"""
Processes the list of .las files before any other algorithm is performed. Grabs globally lowest/highest coordinates and the locally lowest/highest coordinates for each building
Tracks
@param filePathList  A list of .las/.laz files to be preprocessed
@return An array in the form of [globalLowestX, globalLowestY, globalHighestX, globalHighestY, {lasFile1: (lowestCoords, highestCoords), lasFile2: (...), ...}]
"""
def preProcessLasFiles(filePathList, callback=util.printProgressToConsole):
    firstFile = filePathList[0]
    firstFileReader = PointCloudFileIO(util.getPathToFile(firstFile))

    low = firstFileReader.file.header.min
    high = firstFileReader.file.header.max

    globalLowestX = low[0]
    globalLowestY = low[1]
    globalHighestX = high[0]
    globalHighestY = high[1]

    coordsForPaths = {}

    count = len(filePathList)
    i = 0
    callback(i, count)
    for lasFile in filePathList:
        lasFileReader = PointCloudFileIO(util.getPathToFile(lasFile))

        lowestCoords = lasFileReader.file.header.min
        highestCoords = lasFileReader.file.header.max

        if(lowestCoords[0] < globalLowestX):
            globalLowestX = lowestCoords[0]
        if(lowestCoords[1] < globalLowestY):
            globalLowestY = lowestCoords[1]

        if(highestCoords[0] > globalHighestX):
            globalHighestX = highestCoords[0]
        if(highestCoords[1] > globalHighestY):
            globalHighestY = highestCoords[1]

        coordsForPaths[lasFile] = (lowestCoords, highestCoords)
        i += 1
        callback(i, count)

    return [globalLowestX, globalLowestY, globalHighestX, globalHighestY, coordsForPaths]

"""
Combine buildings inside a cadaster to new buildings (so that they represent actual, physical buildings)
@param buildings  A list of all buildings
@return  A list of all PHYSICAL buildings
"""
def combineBuildingsToGroups(buildings):
    uniquePoints = {}
    buildingGroups = {}
    i = 0
    foundCommonPoints = 0
    for building in buildings:
        hadMatchingPoint = False
        foundGroup = False

        for point in building.coordinates:
            if(point in uniquePoints and uniquePoints[point] != i):
                otherBuildingIndex = uniquePoints[point]
                otherBuilding = buildings[otherBuildingIndex]
                # print("Building({}) and Building({}) have a point in common: Point at ({}, {}, {})".format(i, otherBuildingIndex, point.x, point.y, point.z))
                foundCommonPoints += 1
                hadMatchingPoint = True

                if(otherBuildingIndex in buildingGroups and not building in buildingGroups[otherBuildingIndex]):
                    buildingGroups[otherBuildingIndex].add(building)
                    foundGroup = True

            else:
                uniquePoints[point] = i
        if(not hadMatchingPoint):
            buildingGroups[i] = {building}
        i += 1
    # print("Found common points: {}".format(foundCommonPoints))
    # print("Found building groups: {}".format(len(buildingGroups)))

    countGroups = 0
    combinedBuildings = []
    for index, buildingGroup in buildingGroups.items():
        if(len(buildingGroup) > 1):
            result = combineBuildingGroup(buildingGroup)
            if(type(result) == type([])): #Case: Joining buildings failed, returned 2 or more buildings in a list
                for building in result:
                    combinedBuildings.append(building)
            else: #Case: Joining succeeded, result is a building
                combinedBuildings.append(result)

        else:
            combinedBuildings.append(buildingGroup.pop())
            # pass

    i = 0
    for building in combinedBuildings:
        points = []
        for point in building.coordinates:
            points.append((point.x, point.y, point.z))
        p = Polygon(points)
        bounds = p.bounds
        # print("Group({}): Polygon: {} with Area {} | Bounds Length: ({:.3f}, {:.3f})".format(buildingGroupCount, i, p, p.area, bounds[2] - bounds[0], bounds[3] - bounds[1]))
        # print("Group({}): Polygon with Area {} | Bounds Length: ({:.3f}, {:.3f})".format(i, p.area, bounds[2] - bounds[0], bounds[3] - bounds[1]))
        i += 1

    return combinedBuildings

"""
Groups buildings that use the same pointcloud files
@param lasFilesByBuilding  See the return value from "getLasFilesForBuildings"
@return  A dictionary in this form: {"concattedPointsCloudPath1" : [building1, building2, building3], "concattedPointsCloudPath2" : [building4, building10], ...}
"""
def groupBuildingsByPointclouds(lasFilesByBuilding):
    groups = {}
    maxPoints = 0
    maxPointsActual = 0
    for building, buildingInfo in lasFilesByBuilding.items():
        maxPoints = max(maxPoints, len(buildingInfo[0]))
        maxPointsActual = max(maxPointsActual, len(building.coordinates))
        if(False in buildingInfo[0]):
            continue
        # print("Found building that is completely inside our region!")
        concattedPaths = util.concatPointcloudPaths(buildingInfo[1])
        if(concattedPaths in groups):
            groups[concattedPaths].append(building)
        else:
            groups[concattedPaths] = [building]
    return groups



"""
Pre process a list of buildings
 470958.232
5755390.323
"""
def preProcessBuildingList(buildingList, pointLeeway=0.001, callback=util.printProgressToConsole):
    uniquePoints = {}
    buildingGroups = []
    i = 0
    replacedPoints = 0
    notReplaced = 0
    max = len(buildingList)
    for building in buildingList:
        for point in building.coordinates:
            foundNear = False
            for uniquePoint in uniquePoints:
                # if(uniquePoints[uniquePoint] != i and (abs(point.x - uniquePoint.x) < pointLeeway) and (abs(point.y - uniquePoint.y < pointLeeway)) and (abs(point.z - uniquePoint.z < pointLeeway))):
                if(uniquePoints[uniquePoint] != i and not (abs(point.x - uniquePoint.x) > pointLeeway*30) and not (abs(point.y - uniquePoint.y) > pointLeeway*30) and not (abs(point.z - uniquePoint.z) > pointLeeway*30)):
                    shapelyPoint = Point(point.x, point.y, point.z)
                    shapelyUniquePoint = Point(uniquePoint.x, uniquePoint.y, uniquePoint.z)
                    if(shapelyPoint != shapelyUniquePoint and shapelyPoint.distance(shapelyUniquePoint) < pointLeeway):
                        # print("Found point({}) close to unique point({}): {} --- {}".format(i, uniquePoints[uniquePoint], point, uniquePoint))
                        point.x = uniquePoint.x
                        point.y = uniquePoint.y
                        point.z = uniquePoint.z
                        foundNear = True
                        replacedPoints += 1
            if(foundNear == True):
                otherBuildingIndex = uniquePoints[point]
                otherBuilding = buildingList[otherBuildingIndex]
                # print("Building({}) and Building({}) have a point in common: Point at ({}, {}, {})".format(i, otherBuildingIndex, point.x, point.y))
                found = False
                for buildingGroup in buildingGroups:
                    if(otherBuilding in buildingGroup and not building in buildingGroup):
                        buildingGroup.append(building)
                        found = True
                if(found == False):
                    buildingGroups.append([building])
            else:
                uniquePoints[point] = i
                notReplaced += 1
        i += 1
        callback(i, max)

    # print("Replaced a total of ({})/({}) points.".format(replacedPoints, notReplaced+replacedPoints))


buildingGroupCount = 0
"""
Combines one group of buildings to a total building
"""
def combineBuildingGroup(buildingGroup, pointLeeway=0.001):
    global buildingGroupCount
    polygons = []
    i = 0
    for building in buildingGroup:
        points = []
        for point in building.coordinates:
            points.append((point.x, point.y, point.z))
        p = Polygon(points)
        polygons.append(p)
        bounds = p.bounds
        # print("Group({}): Area of polygon({}) before union: {}".format(buildingGroupCount, i, util.getBuildingArea(building)))
        # print("Group({}): Polygon({}): Polygon: {} with Area {} | Bounds Length: ({:.3f}, {:.3f})".format(buildingGroupCount, i, p, p.area, bounds[2] - bounds[0], bounds[3] - bounds[1]))
        i += 1

    # for poly in polygons:
        # print("Polygon: {}".format(poly))

    union = cascaded_union(polygons)
    building = cadaster.Building()
    if(union.boundary.is_closed == False):
        # print("Failed boundary!")
        buildings = []
        for boundary in union.boundary:
            building = cadaster.Building()
            for coord in boundary.coords:
                building.coordinates.append(cadaster.Coordinate(coord[0], coord[1], coord[2]))
            buildings.append(building)
        buildingGroupCount += 1
        return buildings
    # print("Group({}): Area of union: {}".format(buildingGroupCount, union.area))
    for coord in union.boundary.coords:
        # print("Group({}): Coords: ({}, {}, {})".format(buildingGroupCount, coord[0], coord[1], coord[2]))
        building.coordinates.append(cadaster.Coordinate(coord[0], coord[1], coord[2]))
        # print("Building coordinates count: {}".format(len(building.coordinates)))
    # print("Group({}): Area of union building AFTER manual merge: {}\n".format(buildingGroupCount, util.getBuildingArea(building)))
    buildingGroupCount += 1
    return building


"""
Cuts out a pointcloud fitting a given building, saves it to a certain file
@param pointcloudReader  The pointcloud containing the building
@param building  The building to be cut out
@param savePath  The path for the new pointcloud to be saved to
@param extendInclude  (optional) Extends the buildings bounds a little to avoid cutting the edges (too) narrow
@param insetExclude  (optional) Excludes the inside of the building to speed up the algorithm
@param pointsEnclosingDistance  (optional) The distance for the points around the edges to be included recursively in the algorithm, default as 1 meter distance
"""
def cutBuildingFromPointcloud(pointsAbsList, writablePointsList, boundsList, lasFileHeader, building, saveFolder, callback=util.printProgressToConsole, extendInclude=1.01, insetExclude=0.90, pointsEnclosingDistance=1, maximumBoundsExtend=1.05):
    from laspy.file import File

    poly = Polygon([(point.x, point.y) for point in building.coordinates])

    polyExtend = affinity.scale(poly, extendInclude, extendInclude, extendInclude)
    polyMaximum = affinity.scale(poly, maximumBoundsExtend, maximumBoundsExtend, maximumBoundsExtend)
    maxBounds = polyMaximum.bounds
    minX = maxBounds[0]
    minY = maxBounds[1]
    maxX = maxBounds[2]
    maxY = maxBounds[3]

    # polyInset = affinity.scale(poly, insetExclude, insetExclude, insetExclude) #not needed currently

    anchor = poly.centroid

    filename = "{}_{}_{}.las".format(int(round(anchor.x, 0)), int(round(anchor.y, 0)), int(round(building.coordinates[0].z, 0)))
    # print("Filename: {}".format(filename))
    # print("Poly bounds normal:  {} | Area: {}".format(poly.bounds, poly.area))
    # print("Poly bounds extend:  {}".format(polyExtend.bounds))
    # print("Poly bounds maximum: {}".format(polyMaximum.bounds))

    cutPoints = []
    cutWritableList = []

    for i in range(len(pointsAbsList)):
        pointsAbs = pointsAbsList[i]
        writablePoints = writablePointsList[i]
        bounds = boundsList[i]
        pcMinX = bounds[0][0]
        pcMinY = bounds[0][1]
        pcMaxX = bounds[1][0]
        pcMaxY = bounds[1][1]

        polyBounds = Polygon([(pcMinX, pcMinY), (pcMaxX, pcMinY), (pcMaxX, pcMaxY), (pcMinX, pcMaxY)])
        pipPolygon = polyBounds.intersection(polyExtend)

        selection = (pointsAbs[:, 0] > minX) & (pointsAbs[:, 1] > minY) & (pointsAbs[:, 0] < maxX) & (pointsAbs[:, 1] < maxY)

        pointsAbs = pointsAbs[selection]
        writablePoints = writablePoints[selection]

        selection = []
        for point in pointsAbs:
            shapelyPoint = Point(point[0], point[1])
            if(pipPolygon.contains(shapelyPoint)):
                selection.append(True)
            else:
                selection.append(False)

        cutPoints.append(pointsAbs[selection])
        cutWritableList.append(writablePoints[selection])

    combinedPoints = np.concatenate(cutPoints)
    combinedPointsWritable = np.concatenate(cutWritableList)

    if(len(combinedPoints) == 0):
        # print("Found empty selection of points, skipping building...")
        return


    outFile = File("{}/{}".format(saveFolder, filename), mode='w', header=lasFileHeader)
    outFile.points = combinedPointsWritable
    outFile.set_x_scaled(combinedPoints[:, 0])
    outFile.set_y_scaled(combinedPoints[:, 1])
    outFile.set_z_scaled(combinedPoints[:, 2])
    outFile.close()
