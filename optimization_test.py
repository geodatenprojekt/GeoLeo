from geoleo.pointcloud import PointCloudFileIO
from sys import getsizeof

paths = ["example_data/pointcloud_examples/47150_575499_0011.las", "example_data/pointcloud_examples/47150_575507_0011.las", "example_data/pointcloud_examples/47158_575499_0011.las", "example_data/pointcloud_examples/47158_575507_0011.las"]
f1 = PointCloudFileIO("example_data/pointcloud_examples/47150_575491_0011.las")
f1.mergePointClouds(paths, "someShiet.las")
