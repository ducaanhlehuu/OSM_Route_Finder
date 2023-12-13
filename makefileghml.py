import osmnx as ox

# vẽ đồ thị giao thông bằng kinh độ vĩ độ
G = ox.graph_from_bbox(
    21.02743,
    21.02221,
    105.83977,
    105.82522,
    network_type="all_private",
    retain_all=True,
)

# tạo file để để lưu đồ thị
path = r"data\QTGfull.graphml"

# lưu đồ thị
ox.save_graphml(G, filepath=path)
