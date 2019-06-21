from geoleo.pointcloud import PointCloudFileIO
from geoleo import util
import numpy as np

paths = ["example_data/pointcloud_examples/47150_575491_0011.las", "example_data/pointcloud_examples/47150_575499_0011.las", "example_data/pointcloud_examples/47150_575507_0011.las", "example_data/pointcloud_examples/47158_575499_0011.las", "example_data/pointcloud_examples/47158_575507_0011.las"]
f1 = PointCloudFileIO(paths[0])
points1 = f1.file.points
print("Points1: {}\nSize: {}".format(points1, util.inMB(points1.nbytes)))
points1.setflags(write=1)
points1[0][0][0] = 0
print("Points1: {}\nSize: {}".format(points1, util.inMB(points1.nbytes)))

f2 = PointCloudFileIO(paths[1])
points2 = f2.file.points
print("Points2: {}\nSize: {}".format(points2, util.inMB(points2.nbytes)))

f3 = PointCloudFileIO(paths[2])
points3 = f3.file.points
print("Points3: {}\nSize: {}".format(points3, util.inMB(points3.nbytes)))

f4 = PointCloudFileIO(paths[3])
points4 = f4.file.points
print("Points4: {}\nSize: {}".format(points4, util.inMB(points4.nbytes)))

f5 = PointCloudFileIO(paths[4])
points5 = f5.file.points
print("Points5: {}\nSize: {}".format(points5, util.inMB(points5.nbytes)))

combined = np.concatenate((points1, points2, points3, points4, points5))
print("Combined: {}\nSize: {}".format(combined, util.inMB(combined.nbytes)))

# f1.mergePointClouds(paths[1:], "someShiet.las")
