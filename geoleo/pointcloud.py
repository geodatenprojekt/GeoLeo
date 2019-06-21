from laspy.file import File
from laspy.header import Header
import numpy as np
from geoleo import util

"""
Class PointCloudFileIO encapsulates read/write access to .laz/.las files
The PointClouds can be read from either format, however .laz files will be
unzipped to .las files beforehands
"""
class PointCloudFileIO:

    """
    Constructs PointCloudFileIO object and reads PointCloud file by default
    @param path  The path to the .las/.laz file
    @param read  Whether or not the file should be read immediately
    """
    def __init__(self, path, read=True):
        self.path = path
        self.file = None
        self.points = None

        if(read):
            self.readFile()

    def __del__(self):
        if(self.file != None):
            self.file.close()


    """
    Reads and parses the files content
    If the file is a .laz file, it will be automatically unzipped to a .las file
    """
    def readFile(self):
        if(self.path.endswith(".laz")): #Further unpacking from LAZ to LAS needed
            util.unzipLAZFile(self.path)
            self.path = ".laz".join(self.path.split(".laz")[0:-1]) + ".las"

        #header = Header(point_format=2)
        # self.file = File(self.path, mode='r', header=header)
        self.file = File(self.path, mode='r')


    """
    Saves the input file to a specified output file.
    Can save only certain points in the PointCloud if needed.
    @param path  The path to the new file
    @param keepPoints  An array of booleans to determine which points are saved. Needs to have the same length as the points array
    """
    def writeFileToPath(self, path, points=None, keepPoints=None):
        if(self.file != None):
            try:
                len(points)
            except TypeError:
                points = self.file.points

            outFile = File(path, mode='w', header=self.file.header)
            if(keepPoints == None):
                outFile.points = points
            else:
                outFile.points = points[keepPoints]
            outFile.close()


    """
    Returns all points in the PointCloud, uses absolute coordinates by default
    """
    def getPoints(self, absolute=True):
        if(self.file != None):
            if(absolute):
                return np.vstack((self.file.x, self.file.y, self.file.z)).transpose()
            else:
                return np.vstack((self.file.X, self.file.Y, self.file.Z)).transpose()

    """
    Returns all points and colors in the PointCloud, uses absolute coordinates by default
    """
    def getPointsWithColors(self, absolute=True):
        if(self.file != None):
            if(absolute):
                return np.vstack((self.file.x, self.file.y, self.file.z, self.file.red, self.file.green, self.file.blue)).transpose()
            else:
                return np.vstack((self.file.X, self.file.Y, self.file.Z, self.file.red, self.file.green, self.file.blue)).transpose()

    def getLowestCoords(self, absolute=True):
        return self.file.header.min

    def getHighestCoords(self, absolute=True):
        return self.file.header.max

    def getPath(self):
        return self.path

    def getFile(self):
        return self.file

    """
    Merges all given pointcloud files into a new pointcloud file
        @param listPaths  A list of paths to .las files to be merged
        @param newPath  The path to the newly merged pointcloud. Will overwrite existing files
    """
    def mergePointClouds(self, listPaths, newPath, callback=util.printProgressToConsole):
        import psutil
        import os

        print("Process Memory used at start: {:.2f}MB".format(util.inMB(psutil.Process(os.getpid()).memory_info().rss)))
        print("Available memory at start: {:.2f}MB | Used: {:.2f}MB | Percent: {}%".format(util.inMB(psutil.virtual_memory().available), util.inMB(psutil.virtual_memory().used), psutil.virtual_memory().percent))

        pointsOwn = self.file.points

        pointsOwnSize = util.inMB(pointsOwn.nbytes)
        # print("INIT pointsOwnSize: {:.2f}MB".format(pointsOwnSize))

        thisOffset = self.file.header.get_offset()

        count = len(listPaths)
        i = 0

        callback(i, count)

        firstOtherReader = PointCloudFileIO(listPaths[0])
        otherOffset = firstOtherReader.file.header.get_offset()

        translate = [otherOffset[0] - thisOffset[0], otherOffset[1] - thisOffset[1], otherOffset[2] - thisOffset[2]]
        translate[0] *= 1000
        translate[1] *= 1000
        translate[2] *= 1000

        realCoords = []
        realCoords.append(np.append(self.file.X, firstOtherReader.file.X + round(translate[0])))
        realCoords.append(np.append(self.file.Y, firstOtherReader.file.Y + round(translate[1])))
        realCoords.append(np.append(self.file.Z, firstOtherReader.file.Z + round(translate[2])))

        xSize = util.inMB(realCoords[0].nbytes)
        ySize = util.inMB(realCoords[1].nbytes)
        zSize = util.inMB(realCoords[2].nbytes)

        # pointsCombined = np.append(pointsOwn, firstOtherReader.file.points)
        pcrList = [self, firstOtherReader]
        pointsList = [pointsOwn, firstOtherReader.file.points]

        # pointsCombinedSize = util.inMB(pointsCombined.nbytes)
        # print("INIT pointsCombinedSize: {:.2f}MB".format(pointsCombinedSize))

        print("Process Memory used after first merge: {:.2f}MB".format(util.inMB(psutil.Process(os.getpid()).memory_info().rss)))
        print("Available memory after first merge: {:.2f}MB | Used: {:.2f}MB | Percent: {}%".format(util.inMB(psutil.virtual_memory().available), util.inMB(psutil.virtual_memory().used), psutil.virtual_memory().percent))

        i += 1
        callback(i, count)

        currentIndex = 0
        #combined = np.zeros((14000000, 12))

        for i in range(1, len(listPaths)):
            otherReader = PointCloudFileIO(listPaths[i])
            otherOffset = otherReader.file.header.get_offset()
            otherPoints = otherReader.file.points

            otherPointsSize = util.inMB(otherPoints.nbytes)
            # print("otherPointsSize: {:.2f}MB".format(otherPointsSize))

            translate = [otherOffset[0] - thisOffset[0], otherOffset[1] - thisOffset[1], otherOffset[2] - thisOffset[2]]
            translate[0] *= 1000
            translate[1] *= 1000
            translate[2] *= 1000

            realCoords[0] = np.append(realCoords[0], otherReader.file.X + round(translate[0]))
            realCoords[1] = np.append(realCoords[1], otherReader.file.Y + round(translate[1]))
            realCoords[2] = np.append(realCoords[2], otherReader.file.Z + round(translate[2]))

            # pointsCombined = np.concatenate((pointsCombined, otherPoints))
            # pointsCombined = np.append(pointsCombined, otherPoints)
            pointsList.append(otherPoints)
            pcrList.append(otherReader)

            # print("otherPointsLen: {} | PreviousCombinedLen: {} | ExpectedLen: {}".format(len(otherPoints), len(pointsCombined), len(pointsCombined) + len(otherPoints)))

            # pointsCombinedSize = util.inMB(pointsCombined.nbytes)
            # print("pointsCombinedSize: {:.2f}MB".format(pointsCombinedSize))

            print("Process Memory used in loop: {:.2f}MB".format(util.inMB(psutil.Process(os.getpid()).memory_info().rss)))
            print("Available memory in loop: {:.2f}MB | Used: {:.2f}MB | Percent: {}%".format(util.inMB(psutil.virtual_memory().available), util.inMB(psutil.virtual_memory().used), psutil.virtual_memory().percent))

            i += 1
            callback(i, count)

        # minX = np.amin(realCoords[0])
        # minY = np.amin(realCoords[1])
        # minZ = np.amin(realCoords[2])
        #
        # maxX = np.amax(realCoords[0])
        # maxY = np.amax(realCoords[1])
        # maxZ = np.amax(realCoords[2])

        print("Process Memory after loop: {:.2f}MB".format(util.inMB(psutil.Process(os.getpid()).memory_info().rss)))
        print("Available memory after loop: {:.2f}MB | Used: {:.2f}MB | Percent: {}%".format(util.inMB(psutil.virtual_memory().available), util.inMB(psutil.virtual_memory().used), psutil.virtual_memory().percent))

        pointsCombined = np.concatenate(pointsList)
        print("PointsCombined: {}\nSize: {}".format(pointsCombined, util.inMB(pointsCombined.nbytes)))

        # print("PointsCombined: Length: {}, first Half: {}".format(pointsCombined.shape, pointsCombined[0:6698927]))



        outFile = File(newPath, mode='w', header=self.file.header)
        outFile.points = pointsCombined
        outFile.X = realCoords[0]
        outFile.Y = realCoords[1]
        outFile.Z = realCoords[2]
        # outFile.header.set_min([minX, minY, minZ])
        # outFile.header.set_max([maxX, maxY, maxZ])
        outFile.close()

if __name__ == "__main__":
    pcReader = PointCloudFileIO(util.getPathToFile("../backend/example_data/47078_575419_0011.laz"))
    points = pcReader.getPoints()
    [print(x) for x in points[0:20]]


"""
=== Explanation of the points array ===
# PointCloudFileIO.getPoints() returns a numpy array of points in this form:
# point = numpy.ndarray([i4, i4, i4, u2, u2, u2])
# This means a point in this array looks like this with semantics:
# point = numpy.ndarray([x, y, z, red, green, blue])
# And like this with example values:
# point = numpy.ndarray([11683, 25476,  8710,  19380, 21165, 23205])
# All numpy functions can be used to create a modified version of the points array
=== Example usage of class PointCloudReader ===
# Create new PointCloudFileIO object with the path to the laz/las file as parameter
pcReader = PointCloudFileIO(util.getPathToFile("example_data/47078_575419_0011.laz"))
points = pcReader.getPoints()
print(points[0]) # The first point in the list
print(points[0][0]) # The x coordinate of the first point
print(points[0][1]) # The y coordinate of the first point
print(points[0][2]) # The z coordinate of the first point
pcReader.writeFileToPath(util.getPathToFile("test.las")) # Write the input file to another file
# Example of how to calculate distances between the first 20 points and all other points
# This will print how many points are closer or exactly 1000 units away for each of the first 20 points
pcReader = PointCloudFileIO(util.getPathToFile("example_data/47078_575419_0011.laz"))
points = pcReader.getPoints()
for p in points[0:20]:
    selection = util.getPointsCloseToAnchor(p, points, distance=1000)
    pointsFiltered = points[selection]
    print("'{}' points are left from the pointcloud".format(len(pointsFiltered)))
# Example of how to keep only points that are closer than 5000 units to the first point in the PointCloud,
# and write the result to an output file
pcReader = PointCloudFileIO(util.getPathToFile("example_data/47078_575419_0011.laz"))
points = pcReader.getPoints()
firstPoint = points[0]
selection = util.getPointsCloseToAnchor(firstPoint, points, distance=5000)
pcReader.writeFileToPath(util.getPathToFile("test.las"), selection)
# More examples of how to modify the points array:
# https://pythonhosted.org/laspy/tut_part_1.html
"""
