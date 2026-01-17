"""
Builds the transfer.txt file.
"""
import multiprocessing
import pickle
from multiprocessing import Pool
from time import time
import networkx as nx
import numpy as np
import pandas as pd
from haversine import haversine_vector, Unit
from tqdm import tqdm
import osmnx as ox
from routing.config import *
import services.stop as StopService
import services.transfer as TransferService

breaker = "________________"
WALKING_LIMIT = 100
start_time = 0
def extract_graph(NETWORK_NAME: str) -> tuple:
    """
    Extracts the required OSM.

    Args:
        NETWORK_NAME (str): name of the network
        stops_list (list):

    Returns:
        networkx graph, list of tuple [(stop id, nearest OSM node)]

    Examples:
        >>> G, stops_list = extract_graph("anaheim", breaker)
    """
    try:
        G = pickle.load(open(os.path.join(DATA_PATH, "gtfs_o", f"{NETWORK_NAME}_walk_G.pickle" ), 'rb'))
        #G = pickle.load(open(f"./Data/GTFS/{NETWORK_NAME}/gtfs_o/{NETWORK_NAME}_G.pickle", 'rb'))
        print(G)
        # G = nx.read_gpickle(f"./GTFS/{NETWORK_NAME}/gtfs_o/{NETWORK_NAME}_G.pickle")
        print("Graph imported from disk")
    except (FileNotFoundError, ValueError, AttributeError) as error:
        print(f"Graph import failed {error}. Extracting OSM graph for {NETWORK_NAME}")
        LOCATION_NAME = "San Francisco"
        G = ox.graph_from_place(f"San Francisco", network_type='walk')
        # TODO: Change this to bound box + 1 km
        print(f"Number of Edges: {len(G.edges())}")
        print(f"Number of Nodes: {len(G.nodes())}")
        print(f"Saving {NETWORK_NAME}")
        pickle.dump(G, open(os.path.join(DATA_PATH, "gtfs_o",f"{NETWORK_NAME}_walk_G.pickle"), 'wb'))
        # nx.write_gpickle(G, f"./GTFS/{NETWORK_NAME}/gtfs_o/{NETWORK_NAME}_G.pickle")
    stops_db = pd.DataFrame(StopService.getAllStops())

    """
    stops_db = pd.read_csv(f'./Data/GTFS/{NETWORK_NAME}/stops.txt')
    stops_db = stops_db.sort_values(by='stop_id').reset_index(drop=True)
    """
    stops_list = list(stops_db.stop_id)

    try:
        osm_nodes = ox.nearest_nodes(G, stops_db.stop_lon.to_list(), stops_db.stop_lat.to_list())
    except:
        print("Warning: OSMnx.nearest_nodes failed. Switching to Brute force for finding nearest OSM node...")
        print("Fix the above import for faster results")
        node_names, node_coordinates = [], []
        for node in G.nodes(data=True):
            node_coordinates.append((node[1]["y"], node[1]["x"]))
            node_names.append(node[0])
        dist_list = []
        for _, stop in tqdm(stops_db.iterrows()):
            dist_list.append(haversine_vector(node_coordinates, len(node_coordinates) * [(stop.stop_lat, stop.stop_lon)], unit=Unit.METERS))
        osm_nodes = [node_names[np.argmin(item)] for item in dist_list]
        print(f"Unique STOPS: {len(stops_db)}")
        print(f"Unique OSM nodes identified: {len(set(osm_nodes))}")
    stops_list = list(zip(stops_list, osm_nodes))
    print(stops_db)
    print("_")
    return G, stops_list

def find_transfer_len(G,source_info: tuple, stops_list: list) -> list:
    """
    Runs shortest path algorithm from source stop with cutoff limit of WALKING_LIMIT * 2

    Args:
        source_info (tuple): Format (stop id, nearest OSM node)

    Returns:
        temp_list (list): list of format: [(bus stop id, osm node id, distance between the two nodes)]

    Examples:
        >>> temp_list = find_transfer_len(source_info)
    """
    # print(source_info[0])
    out = nx.single_source_dijkstra_path_length(G, source_info[1], cutoff=WALKING_LIMIT * 2, weight='length')
    reachable_osmnodes = set(out.keys())
    temp_list = [(source_info[0], stopid, round(out[osm_nodet], 1)) for (stopid, osm_nodet) in stops_list if osm_nodet in reachable_osmnodes]
    return temp_list

def find_transfer(G,source_info: tuple, stops_list: list) -> list:
    """
    Runs shortest path algorithm from source stop with cutoff limit of WALKING_LIMIT * 2

    Args:
        source_info (tuple): Format (stop id, nearest OSM node)

    Returns:
        temp_list (list): list of format: [(bus stop id, osm node id, distance between the two nodes)]

    Examples:
        >>> temp_list = find_transfer_len(source_info)
    """
    # print(source_info[0])
    out = nx.single_source_dijkstra(G, source_info[1], cutoff=WALKING_LIMIT * 2, weight='length')
    dist_dict, path_dict = out
    #print(path_dict)
    reachable_osmnodes = set(path_dict.keys())
    temp_list = []
    for (stopid, osm_nodet) in stops_list:
        if osm_nodet in reachable_osmnodes and osm_nodet != source_info[1]:
            temp_list.append((source_info[0], stopid,round(dist_dict[osm_nodet], 1), path_dict[osm_nodet]))
    #print(temp_list)
    return temp_list

def transitive_closure(input_list: tuple, G_new) -> list:
    """
    Ensures transitive closure of footpath graph

    Args:
        input_list (tuple): list of format [(network graph object)]

    Returns:
        new_edges (list):

    """
    graph_object, connected_component = input_list
    new_edges = []
    for source in connected_component:
        for desti in connected_component:
            if source != desti and (source, desti) not in G_new.edges():
                new_edges.append((source, desti, nx.dijkstra_path_length(G_new, source, desti, weight="length")))
    return new_edges
#The transfer db: src, target, [coordinates of path], length

def post_process(G_new, NETWORK_NAME: str, ini_len: int) -> None:
    """
    Post process the transfer file. Following functionality are included:
        1. Checks if the transfers graph is transitively closed.

    Args:
        transfer_file: GTFS transfers.txt file
        WALKING_LIMIT (int): Maximum walking limit
        NETWORK_NAME (str): Network name

    Returns:
        None
    """
    footpath = list(G_new.edges(data=True))
    reve_edges = [(x[1], x[0], x[-1]) for x in G_new.edges(data=True)]
    footpath.extend(reve_edges)
    transfer_file = pd.DataFrame(footpath)
    transfer_file[2] = transfer_file[2].apply(lambda x: list(x.values())[0])
    transfer_file.rename(columns={0: "from_stop_id", 1: "to_stop_id", 2: "min_transfer_time"}, inplace=True)
    transfer_file.sort_values(by=['min_transfer_time', 'from_stop_id', 'to_stop_id']).reset_index(drop=True)
    transfer_file.to_csv(f"./DATA/GTFS/{NETWORK_NAME}/transfers.csv", index=False)
    transfer_file.to_csv(f"./DATA/GTFS/{NETWORK_NAME}/transfers.txt", index=False)
    print(f"Before Transitive closure: {ini_len}")
    print(f"After  Transitive closure (final file): {len(transfer_file)}")
    print(f"Total transfers: {len(transfer_file)}")
    print(f"Longest transfer: {transfer_file.iloc[-1].min_transfer_time} seconds")
    print(f"Time required: {round((time() - start_time) / 60, 1)} minutes")
    return None

#
def build_transfer(NETWORK_NAME):
    USE_PARALLEL = 0

    G, stops_list = extract_graph(NETWORK_NAME)
    
    CORES = 0
    ox.settings.use_cache = True
    ox.settings.log_console = False
    #print(stops_list)
    transfer_db = []
    count = 0
    print("Calculate transfer path")
    for stop in stops_list:
        transfers = find_transfer(G, stop, stops_list)
        #print(transfers)
        for path_id, path in enumerate(transfers):
            transfer_db.append([path[0], path[1],path[2],[]])
            for node_id, osmnode in enumerate(path[3]):
                node = G.nodes[osmnode]
                transfer_db[count][3].append((node["x"], node["y"]))
            count+= 1
    #print(transfer_db)
    
    print(f"Importing into database {len(transfer_db)} paths")

    transfer_df = pd.DataFrame(transfer_db, columns=['src_stop_id', 'dest_stop_id', 'min_transfer_time', 'path'])
    TransferService.importData(transfer_df)
    #print(transfer_df)

    #print(result)
    #for source_info in tqdm(stops_list):

#build_transfer("sfo")