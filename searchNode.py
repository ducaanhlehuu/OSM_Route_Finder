import xml.etree.ElementTree as ET
import networkx as nx
import math


def distance_from_point_to_line(x1, y1, x2, y2, x0, y0):
    # Tính hệ số A, B, C của đường thẳng
    A = y2 - y1
    B = x1 - x2
    C = (x2 - x1) * y1 + (y1 - y2) * x1
    denominator = math.sqrt(A**2 + B**2)

    if denominator == 0:
        # Tránh chia cho 0
        return 0

    # Tính khoảng cách
    distance = abs(A * x0 + B * y0 + C) / math.sqrt(A**2 + B**2)

    return distance


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
        if way.find("tag[@k='highway']") is not None:
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


def findNearNodeid(lat, lon, G: nx.MultiDiGraph):
    min_distance = float("inf")
    nearest_node = None

    for edge in G.edges:
        x1, y1 = float(G.nodes[edge[0]]["x"]), float(G.nodes[edge[0]]["y"])
        x2, y2 = float(G.nodes[edge[1]]["x"]), float(G.nodes[edge[1]]["y"])

        d = distance_from_point_to_line(x1, y1, x2, y2, lat, lon)

        if d < min_distance and d != 0:
            min_distance = d
            nearest_node = edge[1]

    return nearest_node
