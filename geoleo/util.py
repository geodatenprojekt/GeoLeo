import os
import subprocess
import numpy as np

"""
Returns the absolute path to the relative path that was specified
    @param file  The file which's path is requested. Can specify file in multiple subfolders
    @return  The absolute path to the file
"""
def getPathToFile(file):
        directory = os.getcwd()
        joined = os.path.join(directory, file)
        return joined


def getPathRelativeToRoot(file):
    rootDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(rootDir, "../"+file)


"""
Unzips a specified '.laz' file to a '.las' file. By default this method uses the
'laszip-cli.exe' located in the current directory
"""
def unzipLAZFile(pathToFile, pathToLASZIP=getPathRelativeToRoot("libs/laszip-cli.exe")):
    subprocess.call([pathToLASZIP, pathToFile])


"""
Returns a boolean list which identifies all points from <numpyArr> that are within <distance> units of <anchor>
    @param anchor  The anchor point used to calculate all distances
    @param numpyArr  The numpy array holding all other points that are compared against the anchor point
    @return  An array of booleans with the same length as <numpyArr>
"""
def getPointsCloseToAnchor(anchor, numpyArr, distance=1000):
    if(numpyArr.shape[1] != 3):
        raise ValueError("numpyArr has invalid dimensions: '{}' columns found, '3' needed.".format(numpyArr.shape[1]))
    if(len(anchor) != 3):
        raise ValueError("numpyArr has invalid dimensions: '{}' found, '(3,)' needed.".format(anchor.shape))
    if(distance < 0):
        raise ValueError("Invalid distance specified: '{}'".format(distance))

    #Coordinate differences between point and all points in numpyArr
    numpyArr -= anchor

    #Convert numpyArr from int32 to int64, otherwise the following operations might cause an overflow
    numpyArr = np.array(numpyArr, dtype=np.int64)

    #Calculate distances between point and all points in numpyArr
    numpyArr = np.square(numpyArr)
    numpyArr = np.sum(numpyArr, axis=1)
    numpyArr = np.sqrt(numpyArr)

    #Return a boolean array where True means a point is within <distance> units of the anchor point
    return numpyArr < distance
