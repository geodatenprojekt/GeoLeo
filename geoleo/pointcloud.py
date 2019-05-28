import laspy.file 
import numpy as np
import File
import util

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

        self.file = File(self.path, mode='r')


    """
    Saves the input file to a specified output file.
    Can save only certain points in the PointCloud if needed.
    @param path  The path to the new file
    @param keepPoints  An array of booleans to determine which points are saved. Needs to have the same length as the points array
    """
    def writeFileToPath(self, path, keepPoints=None):
        if(self.file != None):
            outFile = File(path, mode='w', header=self.file.header)
            if(keepPoints == None):
                outFile.points = self.file.points
            else:
                outFile.points = self.file.points[keepPoints]
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


    def getPath(self):
        return self.path

    def getFile(self):
        return self.file

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
