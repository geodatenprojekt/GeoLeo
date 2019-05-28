from geoleo.pointcloud import PointCloudFileIO
from geoleo import cadaster
import geoleo.cadaster_reader as CadReader
import geoleo.util as util
from shapely.geometry import Point, Polygon

pcReader = PointCloudFileIO(util.getPathToFile("example_data/pointcloud_examples/47086_575419_0011.las"))
low = pcReader.getLowestCoords()
high = pcReader.getHighestCoords()
diff = high - low;
middle = low + diff/2

print("Higher bounds: {}".format(high))
print("Lower bounds: {}".format(low))
print("Middle bounds: {}".format(middle))
print("Difference bounds: {}".format(diff))

lowRel = pcReader.getLowestCoords(False)
highRel = pcReader.getHighestCoords(False)
diffRel = highRel - lowRel;
middleRel = lowRel + diffRel/2

print("Higher bounds (relative): {}".format(highRel))
print("Lower bounds (relative): {}".format(lowRel))
print("Middle bounds (relative): {}".format(middleRel))
print("Difference bounds (relative): {}".format(diffRel))

eckpunkt1 = (low[0], low[1])
eckpunkt2 = (high[0], low[1])
eckpunkt3 = (low[0], high[1])
eckpunkt4 = (high[0], high[1])

bounds = Polygon([eckpunkt1, eckpunkt2, eckpunkt3, eckpunkt4])

cad = cadaster.Cadaster()
cad.buildings = CadReader.getBuildings("example_data/cadaster_examples/LoD1_470_5754_1_NW.gml")

for building in cad.buildings:
    for firstPoint in building.coordinates:
        point = Point(firstPoint.x, firstPoint.y)
        if(bounds.contains(point)):
            print("Pointcloud contains point [{} {} {}]".format(firstPoint.x, firstPoint.y, firstPoint.z))
        else:
            print("Pointcloud does not contain point [{} {} {}]".format(firstPoint.x, firstPoint.y, firstPoint.z))


#points = pcReader.getPoints()
#print("\n")
#[print(x) for x in points[0:20]]
