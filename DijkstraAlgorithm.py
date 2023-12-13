import networkx as nx
from queue import Queue
import getfromgraph as gfg
import searchNode as sN


# hàm chuyển hàng đợi thành mảng
def list_to_queue(my_arr: list):
    my_queue = Queue()
    for element in my_arr:
        my_queue.put(element)
    return my_queue


# hàm chuyển mảng thành hàm đợi
def queue_to_list(queue):
    result_list = []
    while not queue.empty():
        result_list.append(queue.get())
    return result_list


# hàm sắp xếp mảng nodeid theo theo giá trị hàm heuristic
def quick_sort(arr, heu):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        pivot_heu = heu[pivot]

        less_than_pivot = [x for x in arr[1:] if heu[x] <= pivot_heu]
        greater_than_pivot = [x for x in arr[1:] if heu[x] > pivot_heu]

        return (
            quick_sort(less_than_pivot, heu)
            + [pivot]
            + quick_sort(greater_than_pivot, heu)
        )


# hàm gọi các node lân cận của node
def neighbors(G: nx.MultiDiGraph, nodeid: str):
    neighbors_list = []
    for edge in G.edges(data=True):
        if edge[0] == nodeid:
            neighbor = [edge[1], edge[2]["length"]]
            neighbors_list.append(neighbor)
    return neighbors_list


# hàm tìm đường đi theo thuật toán dijkstra
def DSearch(G: nx.MultiDiGraph, nodestart: str, nodefinish: str):
    visited = set()
    parent = {}
    heu = {}
    heu[nodestart] = 0
    queue = Queue()
    queue.put(nodestart)
    # duyệt các node theo thuật toán dijkstra
    while not queue.empty():
        current_node = queue.get()
        # kiểm tra đã tìm được node đích chưa
        if current_node == nodefinish:
            break
        visited.add(current_node)
        for neighbor in neighbors(G, current_node):
            if neighbor[0] not in visited:
                # lưu node cha của node đang xét
                parent[neighbor[0]] = current_node
                # tính hàm heuristic
                heu[neighbor[0]] = heu[current_node] + float(neighbor[1])
                queue.put(neighbor[0])
        # sắp xếp lại hàng đợi
        arr = queue_to_list(queue)
        arr = quick_sort(arr, heu)
        queue = list_to_queue(arr)
    path = []
    current = nodefinish
    # lưu danh sách các node trên đường đi
    while current is not None:
        x = sN.findLatLonByNodeid_2(current, r"data\map.osm")
        path.insert(0, x)
        current = parent.get(current, None)
    return path
