from fastapi import FastAPI, HTTPException, logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AStarAlgorithm import *
from typing import List
import time
import GBFSAlgorithm as GA
import DijkstraAlgorithm as DA
import getfromgraph as gfg
import timeit

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

doc = {}
with open("data\QTGfull.graphml", "r", encoding="utf-8") as fd:
    doc = xmltodict.parse(fd.read())

path = "data\QTGfull.graphml"
G = gfg.getgraph(path)

file_path = "data\QTGfull.graphml"
nodes, edges = load_graphml(file_path)


class PathResponse(BaseModel):
    path: List[tuple]
    cost: float
    computation_time: float
    numbers_of_moved_nodes: int


class PointData(BaseModel):
    pntdata: str
    path_find_algo: str
    near_node_algo: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/finding_path")
async def Path_finding(pntdata: str, path_find_algo: str, near_node_algo: str):
    try:
        raw_input = pntdata.split(",")
        # Validate input format
        if len(raw_input) != 4:
            raise ValueError("Invalid input format")

        input_source_loc = (float(raw_input[0]), float(raw_input[1]))
        input_dest_loc = (float(raw_input[2]), float(raw_input[3]))

        # mapped_source_loc = getKNN(input_source_loc, doc)
        # mapped_dest_loc = getKNN(input_dest_loc, doc)
        if near_node_algo == "getKNN":
            mapped_source_loc = getKNN(input_source_loc, doc)
            mapped_dest_loc = getKNN(input_dest_loc, doc)
        elif near_node_algo == "near_edge_node":
            mapped_source_loc = findNearNodeidForstart(
                input_source_loc[0], input_source_loc[1], G
            )
            mapped_dest_loc = findNearNodeidForfinish(
                input_dest_loc[0], input_dest_loc[1], G
            )
        else:
            raise ValueError("Invalid input format")
        source_node_id = getOSMId(mapped_source_loc[0], mapped_source_loc[1], doc)
        destination_node_id = getOSMId(mapped_dest_loc[0], mapped_dest_loc[1], doc)

        s = timeit.default_timer()

        match path_find_algo:
            case "Astar":
                final_path, moved_nodes = astar(
                    nodes, edges, source_node_id, destination_node_id
                )
            case "Dijkstra":
                final_path, moved_nodes = DA.DSearch(
                    G, source_node_id, destination_node_id
                )
            case "GBFS":
                final_path, moved_nodes = GA.GBFSearch(
                    G, source_node_id, destination_node_id
                )
            case _:
                raise ValueError("Invalid input format")

        cost = calculate_path_cost(edges, final_path, doc)
        path_strings = [latlon for latlon in final_path]
        # cost += haversine(input_source_loc, (final_path[0][0], final_path[0][1]))
        # cost += haversine(input_dest_loc, (final_path[-1][0], final_path[-1][1]))
        execute_time = timeit.default_timer() - s
        return PathResponse(
            path=path_strings,
            cost=cost,
            computation_time=execute_time,
            numbers_of_moved_nodes=moved_nodes,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/astar")
# async def A_Star(pntdata: str):
#     try:
#         raw_input = pntdata.split(",")
#         # Validate input format
#         if len(raw_input) != 4:
#             raise ValueError("Invalid input format")

#         input_source_loc = (float(raw_input[0]), float(raw_input[1]))
#         input_dest_loc = (float(raw_input[2]), float(raw_input[3]))

#         # mapped_source_loc = getKNN(input_source_loc, doc)
#         # mapped_dest_loc = getKNN(input_dest_loc, doc)
#         mapped_source_loc = findNearNodeidForstart(
#             input_source_loc[0], input_source_loc[1], G
#         )
#         mapped_dest_loc = findNearNodeidForfinish(
#             input_dest_loc[0], input_dest_loc[1], G
#         )

#         source_node_id = getOSMId(mapped_source_loc[0], mapped_source_loc[1], doc)
#         destination_node_id = getOSMId(mapped_dest_loc[0], mapped_dest_loc[1], doc)

#         s = timeit.default_timer()
#         final_path, moved_nodes = astar(
#             nodes, edges, source_node_id, destination_node_id
#         )
#         cost = calculate_path_cost(edges, final_path, doc)
#         path_strings = [latlon for latlon in final_path]
#         execute_time = timeit.default_timer() - s
#         return PathResponse(
#             path=path_strings,
#             cost=cost,
#             computation_time=execute_time,
#             numbers_of_moved_nodes=moved_nodes,
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/dijkstra")
# async def Dijikstra(pntdata: str):
#     try:
#         raw_input = pntdata.split(",")
#         # Validate input format
#         if len(raw_input) != 4:
#             raise ValueError("Invalid input format")

#         input_source_loc = (float(raw_input[0]), float(raw_input[1]))
#         input_dest_loc = (float(raw_input[2]), float(raw_input[3]))

#         mapped_source_loc = getKNN(input_source_loc, doc)
#         mapped_dest_loc = getKNN(input_dest_loc, doc)
#         source_node_id = getOSMId(mapped_source_loc[0], mapped_source_loc[1], doc)
#         destination_node_id = getOSMId(mapped_dest_loc[0], mapped_dest_loc[1], doc)

#         s = time.time()
#         final_path, moved_nodes = DA.DSearch(G, source_node_id, destination_node_id)
#         cost = calculate_path_cost(edges, final_path, doc)
#         path_strings = [latlon for latlon in final_path]
#         execute_time = time.time() - s
#         return PathResponse(
#             path=path_strings,
#             cost=cost,
#             computation_time=execute_time,
#             numbers_of_moved_nodes=moved_nodes,
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/gbfs")
# async def GBFS(pntdata: str):
#     try:
#         raw_input = pntdata.split(",")
#         # Validate input format
#         if len(raw_input) != 4:
#             raise ValueError("Invalid input format")

#         input_source_loc = (float(raw_input[0]), float(raw_input[1]))
#         input_dest_loc = (float(raw_input[2]), float(raw_input[3]))

#         mapped_source_loc = getKNN(input_source_loc, doc)
#         mapped_dest_loc = getKNN(input_dest_loc, doc)
#         source_node_id = getOSMId(mapped_source_loc[0], mapped_source_loc[1], doc)
#         destination_node_id = getOSMId(mapped_dest_loc[0], mapped_dest_loc[1], doc)

#         s = time.time()
#         final_path, moved_nodes = GA.GBFSearch(G, source_node_id, destination_node_id)
#         cost = calculate_path_cost(edges, final_path, doc)
#         path_strings = [latlon for latlon in final_path]
#         execute_time = time.time() - s
#         return PathResponse(
#             path=path_strings,
#             cost=cost,
#             computation_time=execute_time,
#             numbers_of_moved_nodes=moved_nodes,
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
