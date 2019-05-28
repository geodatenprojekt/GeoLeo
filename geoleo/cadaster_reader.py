import xml.etree.ElementTree as ET
import Classes

def getBuilding(points):
    """Get a Building object from a string array of coordinate points

    Args:
        points: string array of coordinate points
    
    Returns:
        A Building object with all coordinates    
    """
    building = Classes.Building()
    building.coordinates = list()

    for counter in range(0, len(points)):
        coord = (counter + 1) % 3
        if coord == 1:
            x = points[counter]
        elif coord == 2:
            y = points[counter]
        elif coord == 0:
            z = points[counter]

            coord = Coordinate(x, y, z)
            building.coordinates.append(coord)

    return building

def getBuildings(fileName):
    """Get all Buildings from a CityGML file

    Args:
        Filename of the CityGML file

    Returns:
        A List with all Building objects
    """
    core_nameSpace = "{http://www.opengis.net/citygml/1.0}"
    bldg_nameSpace = "{http://www.opengis.net/citygml/building/1.0}"
    gml_nameSpace = "{http://www.opengis.net/gml}"

    tree = ET.parse(fileName)
    root = tree.getroot()

    buildings = list()

    for xml_member in root.iterfind(core_nameSpace + "cityObjectMember"):
        xml_building = xml_member.find(bldg_nameSpace + "Building")
        if xml_building is not None:
            building = Building()
            xml_lod1Solid = xml_building.find(bldg_nameSpace + "lod1Solid")
            if xml_lod1Solid is not None:
                xml_solid = xml_lod1Solid.find(gml_nameSpace + "Solid")
                if xml_solid is not None:
                    xml_exterior = xml_solid.find(gml_nameSpace + "exterior")
                    if xml_exterior is not None:
                        xml_surface = xml_exterior.find(gml_nameSpace + "CompositeSurface")
                        xml_surfaceMember = xml_surface.findall(gml_nameSpace + "surfaceMember")[0]
                        allPoints = xml_surfaceMember.find(gml_nameSpace + 'Polygon').find(gml_nameSpace + 'exterior').find(gml_nameSpace + 'LinearRing').find(gml_nameSpace + 'posList').text
                        points = allPoints.split()
                        building = getBuilding(points)
                        buildings.append(building)
    return buildings
