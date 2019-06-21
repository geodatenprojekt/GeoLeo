from geoleo.pointcloud import PointCloudFileIO
from geoleo import util
from geoleo import algorithms
import numpy as np

paths = ["example_data/pointcloud_examples/47150_575491_0011.las", "example_data/pointcloud_examples/47150_575499_0011.las", "example_data/pointcloud_examples/47150_575507_0011.las", "example_data/pointcloud_examples/47158_575499_0011.las", "example_data/pointcloud_examples/47158_575507_0011.las"]
f1 = PointCloudFileIO(paths[0])
pointsWritable1 = f1.file.points
points1 = f1.getPoints().astype("float32")
# print("PointsWritable1: {}\nSize: {}".format(pointsWritable1, util.inMB(pointsWritable1.nbytes)))
print("Points1: {}\nSize: {}".format(points1, util.inMB(points1.nbytes)))
print("Points1: {}\nSize: {}".format(points1, util.inMB(points1.nbytes)))
print("Points1 length: {}".format(len(points1)))

f2 = PointCloudFileIO(paths[1])
pointsWritable2 = f2.file.points
points2 = f2.getPoints().astype("float32")
# print("PointsWritable2: {}\nSize: {}".format(pointsWritable2, util.inMB(pointsWritable2.nbytes)))
print("Points2: {}\nSize: {}".format(points2, util.inMB(points2.nbytes)))
print("Points2 length: {}".format(len(points2)))

f3 = PointCloudFileIO(paths[2])
pointsWritable3 = f3.file.points
points3 = f3.getPoints().astype("float32")
# print("PointsWritable3: {}\nSize: {}".format(pointsWritable3, util.inMB(pointsWritable3.nbytes)))
print("Points3: {}\nSize: {}".format(points3, util.inMB(points3.nbytes)))
print("Points3 length: {}".format(len(points3)))

f4 = PointCloudFileIO(paths[3])
pointsWritable4 = f4.file.points
points4 = f4.getPoints().astype("float32")
# print("PointsWritable4: {}\nSize: {}".format(pointsWritable4, util.inMB(pointsWritable4.nbytes)))
print("Points4: {}\nSize: {}".format(points4, util.inMB(points4.nbytes)))
print("Points4 length: {}".format(len(points4)))

f5 = PointCloudFileIO(paths[4])
pointsWritable5 = f5.file.points
points5 = f5.getPoints().astype("float32")
# print("PointsWritable5: {}\nSize: {}".format(pointsWritable5, util.inMB(pointsWritable5.nbytes)))
print("Points5: {}\nSize: {}".format(points5, util.inMB(points5.nbytes)))
print("Points5 length: {}".format(len(points5)))

combined = np.concatenate((pointsWritable1, pointsWritable2, pointsWritable3, pointsWritable4, pointsWritable5))
print("Combined: {}\nSize: {}".format(combined, util.inMB(combined.nbytes)))

pointsList = [points1, points2, points3, points4, points5]
pointsWritableList = [pointsWritable1, pointsWritable2, pointsWritable3, pointsWritable4, pointsWritable5]
combinedPoints = np.concatenate(pointsWritableList)
cutPoints = np.concatenate(pointsList)

print("cutPoints length: {}".format(len(cutPoints)))
print("cutWritableList length: {}".format(len(pointsWritableList)))
print("combinedPoints length: {}".format(len(combinedPoints)))
print("All x: {}, len: {}".format(cutPoints[:, 0], len(cutPoints[:, 0])))
