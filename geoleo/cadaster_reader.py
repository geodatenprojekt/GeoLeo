import xml.etree.ElementTree as ET
from geoleo import cadaster

import xml.etree.ElementTree as ET
from geoleo import cadaster
from geoleo import file_helper

CORE_NAME_SPACE = "{http://www.opengis.net/citygml/1.0}"
BLDG_NAME_SPACE = "{http://www.opengis.net/citygml/building/1.0}"
GML_NAME_SPACE = "{http://www.opengis.net/gml}"

XML_CITY_OBJECT_MEMBER = CORE_NAME_SPACE + "cityObjectMember"
XML_BUILDING = BLDG_NAME_SPACE + "Building"
XML_LOD_1_SOLID = BLDG_NAME_SPACE + "lod1Solid"
XML_SOLID = GML_NAME_SPACE + "Solid"
XML_EXTERIOR = GML_NAME_SPACE + "exterior"
XML_COMPOSITE_SURFACE = GML_NAME_SPACE + "CompositeSurface"
XML_SURFACE_MEMBER = GML_NAME_SPACE + "surfaceMember"
XML_POLYGON = GML_NAME_SPACE + 'Polygon'
XML_LINEAR_RING = GML_NAME_SPACE + 'LinearRing'
XML_POS_LIST = GML_NAME_SPACE + 'posList'


def get_coordinates(points):
    """Get a Building object from a string array of coordinate points

    Args:
        points: string array of coordinate points

    Returns:
        A Building object with all coordinates
    """
    building = cadaster.Building()
    building.coordinates = list()

    #for counter in range(0, len(points)):
    for counter in enumerate(points):
        counter = counter[0]
        coord = (counter + 1) % 3
        if coord == 1:
            _x = float(points[counter])
        elif coord == 2:
            _y = float(points[counter])
        elif coord == 0:
            _z = float(points[counter])

            coord = cadaster.Coordinate(x, y, z)
            building.coordinates.append(coord)

    return coordinates

def get_buildings(directory):
    """Get all Buildings from a CityGML file

    Args:
        directory: directory name with all CityGML filey

    Returns:
        A List with all Building objects
    """
    file_names = file_helper.get_all_paths_from_dir(directory)

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

def get_xml_element(elems, xml_elem):
    """Get the XML Element of the CityGML including the points

    Args:
       elems: XML elements to go to the goal element
       xml_elem: Current XML element

    """

    if xml_elem is None:
        return None

    xml_elem = xml_elem.find(elems[0])

    if len(elems) > 1:
        elems.pop(0)
        xml_elem = get_xml_element(elems, xml_elem)

    return xml_elem
