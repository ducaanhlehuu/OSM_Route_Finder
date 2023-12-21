import networkx as nx
import heapq
from geopy.distance import geodesic
from math import sin, cos, sqrt, atan2, radians


# Công thức haversine
def haversine_distance(lat1, lon1, lat2, lon2):
    # Chuyển đổi độ sang radian
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c

    return distance


def heu_dist(G: nx.MultiDiGraph, nodeid1: str, nodeid2: str):
    # Lấy thông tin về kinh độ và vĩ độ của hai đỉnh
    lat1, lon1 = float(G.nodes[nodeid1]["x"]), float(G.nodes[nodeid1]["y"])
    lat2, lon2 = float(G.nodes[nodeid2]["x"]), float(G.nodes[nodeid2]["y"])

    # Tính khoảng cách sử dụng haversine_distance
    distance = haversine_distance(lat1, lon1, lat2, lon2)

    return distance


# hàm gọi các node lân cận của node
def neighbors(G: nx.MultiDiGraph, nodeid: str, nodefinish: str):
    neighbors_list = []
    for edge in G.edges(data=True):
        if edge[0] == nodeid:
            neighbor = [edge[1], heu_dist(G, edge[1], nodefinish)]
            neighbors_list.append(neighbor)
    return neighbors_list


# hàm tìm đường đi theo thuật toán Greedy Best-First Search
def GBFSearch(G: nx.MultiDiGraph, nodestart: str, nodefinish: str):
    priority_queue = [(heu_dist(G, nodestart, nodefinish), nodestart, [nodestart])]
    visited = set()
    nodes_visited_count = 0

    while priority_queue:
        current_heuristic, current_node, current_path = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        nodes_visited_count += 1

        if current_node == nodefinish:
            list = []
            for nodeid in current_path:
                a = []
                x = G.nodes[nodeid]["x"]
                y = G.nodes[nodeid]["y"]
                a.append(float(y))
                a.append(float(x))
                list.append(a)
            return list, nodes_visited_count

        neighbors_list = neighbors(G, current_node, nodefinish)

        for neighbor in neighbors_list:
            neighbor_node, heuristic = neighbor
            if neighbor_node not in visited:
                neighbor_path = current_path + [neighbor_node]
                heapq.heappush(
                    priority_queue, (heuristic, neighbor_node, neighbor_path)
                )

    # Trả về none nếu không tìm thấy
    return None, nodes_visited_count
