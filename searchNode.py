import xml.etree.ElementTree as ET
import networkx as nx


def extract_nodes_from_osm(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    nodes = []

    for node in root.findall(".//node"):
        node_id = node.attrib["id"]
        lat = node.attrib["lat"]
        lon = node.attrib["lon"]

        nodes.append({"id": node_id, "lat": lat, "lon": lon})

    return nodes


def extract_ways_from_osm(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ways = []

    for way in root.findall(".//way"):
        way_id = way.attrib["id"]
        way_nodes = [nd.attrib["ref"] for nd in way.findall("nd")]

        ways.append({"id": way_id, "nodes": way_nodes})

    return ways


def findNodeIdByLatLon(lat: str, lon: str, file_path: str):
    nodes = extract_nodes_from_osm(file_path)
    for node in nodes:
        if node["lat"] == lat and node["lon"] == lon:
            return node["id"]
    return 0


def findLatLonByNodeid(nodeid: str, file_path: str):
    nodes = extract_nodes_from_osm(file_path)
    for node in nodes:
        if node["id"] == nodeid:
            x = node["lat"]
            y = node["lon"]
            a = []
            a.append(x)
            a.append(y)
            return a
    return 0


def findLatLonByNodeid_2(nodeid: str, file_path: str):
    nodes = extract_nodes_from_osm(file_path)
    for node in nodes:
        if node["id"] == nodeid:
            x = node["lat"]
            y = node["lon"]
            a = []
            a.append(float(x))
            a.append(float(y))
            return a
    return 0


def findNearEdgeId(nodeid: str, file_path: str):
    edges = extract_ways_from_osm(file_path)
    for edge in edges:
        for node in edge["nodes"]:
            if node == nodeid:
                return edge["id"]
    return 0


def findNearNodeid(nodeid: str, file_path: str, G: nx.MultiDiGraph):
    edgeid = findNearEdgeId(nodeid, file_path)
    for edge in G.edges(data=True):
        if edge[2]["osmid"] == edgeid:
            return edge[1]
    return edgeid


def findNodeidNearEdge(lat: str, lon: str, file_path: str):
    nodes = extract_nodes_from_osm(file_path)
    min = 10
    for node in nodes:
        d = pow((float(lat) - float(node["lat"])), 2) + pow(
            (float(lon) - float(node["lon"])), 2
        )
        if d < min:
            min = d
            n = node["id"]
    return n
