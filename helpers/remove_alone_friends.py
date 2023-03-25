def remove_alone_friends(graph):
    to_remove = [node for node in graph.nodes() if graph.degree[node] < 2]
    graph.remove_nodes_from(to_remove)

    print('After deleting with alone friends', graph)

    return graph
