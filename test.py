import getfromgraph as gfg
import DijkstraAlgorithm as DA
import searchNode as SN
import osmnx as ox
import GBFSAlgorithm as GBF

path = r"data\QTGfull.graphml"
osmpath = r"data\map.osm"
G = gfg.getgraph(path)
# print(DA.DSearch(G,"11059028995","5701309388"))
print(SN.findNearNodeid(21.0291682, 105.8275083, G))
