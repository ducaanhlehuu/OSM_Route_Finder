import osmnx as ox

# vẽ đồ thị giao thông bằng kinh độ vĩ độ
G = ox.graph_from_bbox(
    21.0318, 21.0211, 105.8394, 105.8239, network_type="bike", retain_all=True
)
# tạo file để để lưu đồ thị
path = r"data\QTGfull.graphml"
# lưu đồ thị
ox.save_graphml(G, filepath=path)
