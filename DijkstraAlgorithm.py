import networkx as nx
import heapq


def neighbors(G: nx.MultiDiGraph, nodeid: str):
    neighbors_list = []
    for edge in G.edges(data=True):
        if edge[0] == nodeid:
            neighbor = [edge[1], edge[2]["length"]]
            neighbors_list.append(neighbor)
    return neighbors_list


def DSearch(G: nx.MultiDiGraph, nodestart: str, nodefinish: str):
    visited = set()
    parent = {}
    heu = {}
    for node in G.nodes():
        heu[node] = 10000
    heu[nodestart] = 0
    queue = []
    heapq.heappush(queue, (0, nodestart))

    # Initialize the counter
    nodes_visited_count = 0

    while queue:
        current_node = heapq.heappop(queue)

        if current_node[1] == nodefinish:
            break

        visited.add(current_node[1])
        nodes_visited_count += 1  # Increment the counter

        for neighbor in neighbors(G, current_node[1]):
            if neighbor[0] not in visited:
                if heu[current_node[1]] + float(neighbor[1]) < heu[neighbor[0]]:
                    parent[neighbor[0]] = current_node[1]
                    heu[neighbor[0]] = heu[current_node[1]] + float(neighbor[1])
                    heapq.heappush(queue, (heu[neighbor[0]], neighbor[0]))

    path = []
    current = nodefinish

    while current is not None:
        a = []
        x = G.nodes[current]["x"]
        y = G.nodes[current]["y"]
        a.append(float(y))
        a.append(float(x))
        path.insert(0, a)
        current = parent.get(current, None)

    return path, nodes_visited_count
