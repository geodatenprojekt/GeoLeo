import xml.etree.ElementTree as ET
from geoleo import cadaster

def getBuilding(points):
    """Get a Building object from a string array of coordinate points

    Args:
        points: string array of coordinate points

    Returns:
        A Building object with all coordinates
    """
    building = cadaster.Building()
    building.coordinates = list()

    for counter in range(0, len(points)):
        coord = (counter + 1) % 3
        if coord == 1:
            x = float(points[counter])
        elif coord == 2:
            y = float(points[counter])
        elif coord == 0:
            z = float(points[counter])

            coord = cadaster.Coordinate(x, y, z)
            building.coordinates.append(coord)

    return building

def getBuildings(fileName):
    """Get all Buildings from a CityGML file

    Args:
        fileName: Filename of the CityGML file

    Returns:
        A List with all Building objects
    """
    core_nameSpace = "{http://www.opengis.net/citygml/1.0}"
    bldg_nameSpace = "{http://www.opengis.net/citygml/building/1.0}"
    gml_nameSpace = "{http://www.opengis.net/gml}"

    tree = ET.parse(fileName)
    root = tree.getroot()

    buildings = list()

    for xml_member in root.iterfind( core_nameSpace + "cityObjectMember"):
        elems = [ bldg_nameSpace + "Building",  bldg_nameSpace + "lod1Solid", gml_nameSpace + "Solid", gml_nameSpace + "exterior", gml_nameSpace + "CompositeSurface", gml_nameSpace + "surfaceMember", gml_nameSpace + 'Polygon', gml_nameSpace + 'exterior', gml_nameSpace + 'LinearRing', gml_nameSpace + 'posList' ]

        building = cadaster.Building()
        xml_elem = getXML_Element(elems, xml_member)
        if xml_elem is not -1:
            allPoints = xml_elem.text
            points = allPoints.split()
            building = getBuilding(points)
            buildings.append(building)

    return buildings

def getXML_Element(elems, xml_elem):
    """Get the XML Element of the CityGML including the points

    Args:
       elems: XML elements to go to the goal element
       xml_elem: Current XML element

    """
    if xml_elem is None:
        return -1

    xml_elem = xml_elem.find(elems[0])

    if len(elems) > 1:
        elems.pop(0)
        xml_elem = getXML_Element(elems, xml_elem)
        return xml_elem
    else:
        return xml_elem
