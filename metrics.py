import networkx as nx
import datetime

from helpers.dumps import load_dump
from helpers.remove_alone_friends import remove_alone_friends


def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def count_metrics(graph):
    print("Starting count metrics", get_time())
    print(f"diameter: {nx.diameter(graph)}")

    print("Starting count radius", get_time())
    print(f"radius: {nx.radius(graph)}")

    print("Starting count central_vertices", get_time())
    print(f"central_vertices: {nx.center(graph)}")

    print("Starting count peripheral_vertices", get_time())
    print(f"peripheral_vertices: {nx.periphery(graph)}")

    print("Starting count cliques", get_time())
    cliques = nx.find_cliques(graph)
    print(f"cliques: {max(cliques)}")
    print("End", get_time())

    print("Starting count degree_centrality", get_time())
    degree_centrality = nx.degree_centrality(graph)

    print("Starting count proximity_centrality", get_time())
    proximity_centrality = nx.closeness_centrality(graph)

    print("Starting count eigenvector_centrality", get_time())
    eigenvector_centrality = nx.eigenvector_centrality(graph)

    print("End", get_time())

    print(f"max_degree_centrality: {max(degree_centrality.values())}")
    print(f"max_proximity_centrality: {max(proximity_centrality.values())}")
    print(
        f"max_eigenvector_centrality: {max(eigenvector_centrality.values())}")


graph = load_dump('buildedGraph')
graph = remove_alone_friends(graph)

count_metrics(graph)
