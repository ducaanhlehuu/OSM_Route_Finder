import heapq as heap
import time
import xmltodict
from haversine import haversine
from searchNode import *
from sklearn.neighbors import KDTree
import numpy as np

doc = {}
with open("data\QTGfull.graphml", "r", encoding="utf-8") as fd:
    doc = xmltodict.parse(fd.read())


# def calculateHeuristic(curr, destination):
#     return haversine(curr, destination)
def getOSMId(lat, lon):
    OSMId = 0
    nodes = doc["graphml"]["graph"]["node"]
    for eachNode in range(len(nodes)):
        if nodes[eachNode]["data"][0]["#text"] == str(lat):
            if nodes[eachNode]["data"][1]["#text"] == str(lon):
                OSMId = nodes[eachNode]["@id"]

    return OSMId


# def getNeighbours(OSMId, destinationLatLon):
#     neighbourDict = {}
#     tempList = []
#     edges = doc["graphml"]["graph"]["edge"]
#     for eachEdge in range(len(edges)):
#         if edges[eachEdge]["@source"] == str(OSMId):
#             temp_nbr = {}

#             neighbourCost = 0
#             neighbourId = edges[eachEdge]["@target"]
#             neighbourLatLon = getLatLon(neighbourId)

#             dataPoints = edges[eachEdge]["data"]
#             for eachData in range(len(dataPoints)):
#                 if dataPoints[eachData]["@key"] == "d13":
#                     neighbourCost = dataPoints[eachData]["#text"]

#             neighborHeuristic = calculateHeuristic(neighbourLatLon, destinationLatLon)

#             temp_nbr[neighbourId] = [neighbourLatLon, neighbourCost, neighborHeuristic]
#             tempList.append(temp_nbr)

#     neighbourDict[OSMId] = tempList
#     return neighbourDict


# def getNeighbourInfo(neighbourDict):
#     neighbourId = 0
#     neighbourHeuristic = 0
#     neighbourCost = 0
#     for key, value in neighbourDict.items():
#         neighbourId = key
#         neighbourHeuristic = float(value[2])
#         neighbourCost = float(value[1]) / 1000
#         neighbourLatLon = value[0]

#     return neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon


# def getLatLon(OSMId):
#     lat, lon = 0, 0
#     nodes = doc["graphml"]["graph"]["node"]
#     for eachNode in range(len(nodes)):
#         if nodes[eachNode]["@id"] == str(OSMId):
#             lat = float(nodes[eachNode]["data"][0]["#text"])
#             lon = float(nodes[eachNode]["data"][1]["#text"])
#     return (lat, lon)


# def aStar(sourceID, destinationID):
#     open_list = []
#     g_values = {}

#     path = {}
#     closed_list = {}

#     source = getLatLon(sourceID)
#     destination = getLatLon(destinationID)
#     g_values[sourceID] = 0
#     h_source = calculateHeuristic(source, destination)

#     open_list.append((h_source, sourceID))

#     s = time.time()
#     while len(open_list) > 0:
#         curr_state = open_list[0][1]

#         # print(curr_state)
#         heap.heappop(open_list)
#         closed_list[curr_state] = ""

#         if curr_state == destinationID:
#             print("We have reached to the goal")
#             break

#         nbrs = getNeighbours(curr_state, destination)
#         values = nbrs[curr_state]
#         for eachNeighbour in values:
#             (
#                 neighbourId,
#                 neighbourHeuristic,
#                 neighbourCost,
#                 neighbourLatLon,
#             ) = getNeighbourInfo(eachNeighbour)
#             current_inherited_cost = g_values[curr_state] + neighbourCost

#             if neighbourId in closed_list:
#                 continue
#             else:
#                 g_values[neighbourId] = current_inherited_cost
#                 neighbourFvalue = neighbourHeuristic + current_inherited_cost

#                 open_list.append((neighbourFvalue, neighbourId))

#             path[str(neighbourLatLon)] = {
#                 "parent": str(getLatLon(destinationID)),
#                 "cost": neighbourCost,
#             }

#         open_list = list(set(open_list))
#         heap.heapify(open_list)

#     print("Time taken to find path(in second): " + str(time.time() - s))
#     return path


# # def aStar(source, destination):
# #     open_list = []
# #     g_values = {}

# #     path = {}
# #     closed_list = {}

# #     sourceID = getOSMId(source[0], source[1])
# #     destID = getOSMId(destination[0], destination[1])

# #     g_values[sourceID] = 0
# #     h_source = calculateHeuristic(source, destination)

# #     open_list.append((h_source, sourceID))

# #     s = time.time()
# #     while len(open_list) > 0:
# #         curr_state = open_list[0][1]

# #         # print(curr_state)
# #         heap.heappop(open_list)
# #         closed_list[curr_state] = ""

# #         if curr_state == destID:
# #             print("We have reached to the goal")
# #             break

# #         nbrs = getNeighbours(curr_state, destination)
# #         values = nbrs[curr_state]
# #         for eachNeighbour in values:
# #             (
# #                 neighbourId,
# #                 neighbourHeuristic,
# #                 neighbourCost,
# #                 neighbourLatLon,
# #             ) = getNeighbourInfo(eachNeighbour)
# #             current_inherited_cost = g_values[curr_state] + neighbourCost

# #             if neighbourId in closed_list:
# #                 continue
# #             else:
# #                 g_values[neighbourId] = current_inherited_cost
# #                 neighbourFvalue = neighbourHeuristic + current_inherited_cost

# #                 open_list.append((neighbourFvalue, neighbourId))

# #             path[str(neighbourLatLon)] = {
# #                 "parent": str(getLatLon(curr_state)),
# #                 "cost": neighbourCost,
# #             }

# #         open_list = list(set(open_list))
# #         heap.heapify(open_list)

# #     print("Time taken to find path(in second): " + str(time.time() - s))
# #     return path


def getKNN(pointLocation):
    nodes = doc["graphml"]["graph"]["node"]
    locations = []
    for eachNode in range(len(nodes)):
        locations.append(
            (nodes[eachNode]["data"][0]["#text"], nodes[eachNode]["data"][1]["#text"])
        )

    locations_arr = np.asarray(locations, dtype=np.float32)
    point = np.asarray(pointLocation, dtype=np.float32)

    tree = KDTree(locations_arr, leaf_size=2)
    dist, ind = tree.query(point.reshape(1, -1), k=3)

    nearestNeighbourLoc = (
        float(locations[ind[0][0]][0]),
        float(locations[ind[0][0]][1]),
    )

    return nearestNeighbourLoc


# def getResponsePathDict(paths, source, destination):
#     finalPath = []
#     child = destination
#     parent = ()
#     cost = 0
#     while parent != source:
#         tempDict = {}
#         cost = cost + float(paths[str(child)]["cost"])
#         parent = paths[str(child)]["parent"]
#         parent = tuple(float(x) for x in parent.strip("()").split(","))

#         tempDict["lat"] = parent[0]
#         tempDict["lng"] = parent[1]

#         finalPath.append(tempDict)
#         child = parent

#     return finalPath, cost

from heapq import heappop, heappush
from geopy.distance import great_circle


class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon


def load_graphml(file_path):
    """Load a graph from a GraphML file."""
    with open(file_path, "r", encoding="utf-8") as fd:
        doc = xmltodict.parse(fd.read())

    nodes = {}
    edges = []

    for node in doc["graphml"]["graph"]["node"]:
        node_id = node["@id"]
        lat = float(node["data"][0]["#text"])
        lon = float(node["data"][1]["#text"])
        nodes[node_id] = Node(node_id, lat, lon)

    for edge in doc["graphml"]["graph"]["edge"]:
        source = edge["@source"]
        target = edge["@target"]
        for eachData in range(len(edge["data"])):
            if edge["data"][eachData]["@key"] == "d13":
                cost = (
                    float(edge["data"][eachData]["#text"]) / 1000
                )  # Assuming the cost is in meters
        edges.append((source, target, cost))

    return nodes, edges


def haversine_distance(node1, node2):
    """Calculate the great-circle distance between two nodes."""
    coord1 = (node1.lat, node1.lon)
    coord2 = (node2.lat, node2.lon)
    return great_circle(coord1, coord2).meters / 1000  # Convert to kilometers


def astar(nodes, edges, source_id, destination_id):
    """Compute the A* path between source and destination."""
    priority_queue = [(0, source_id, [])]  # Add initial cost
    visited = set()

    while priority_queue:
        current_cost, current_node_id, current_path = heappop(priority_queue)

        if current_node_id in visited:
            continue

        current_node = nodes[current_node_id]
        current_path = current_path + [
            (current_node.lat, current_node.lon)
        ]  # Store lat and lon

        if current_node_id == destination_id:
            return current_path  # Return only the path

        visited.add(current_node_id)

        for neighbor_id, target_id, cost in edges:
            if neighbor_id == current_node_id:
                neighbor_node = nodes[target_id]
                heuristic = haversine_distance(neighbor_node, nodes[destination_id])
                total_cost = current_cost + cost + heuristic
                heappush(priority_queue, (total_cost, target_id, current_path))

    return None  # Return None if no path is found


# Example usage:
file_path = "data\QTGfull.graphml"
nodes, edges = load_graphml(file_path)


def calculate_path_cost(edges, path):
    total_cost = 0

    for i in range(len(path) - 1):
        source_node = getOSMId(path[i][0], path[i][1])
        target_node = getOSMId(path[i + 1][0], path[i + 1][1])

        edge = next(
            (e for e in edges if (e[0] == source_node and e[1] == target_node)),
            None,
        )

        if edge:
            total_cost += edge[2]  # Lấy trọng số (cost) từ cạnh
    return total_cost
