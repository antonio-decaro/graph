from adt.graph.core import Graph
from typing import Tuple


def is_connected_graph(graph: Graph) -> bool:
    """
    Check if a a is connected.
    :param graph: the a to check
    :return: True if a is connected, False otherwise
    :raises AttributeError: if the graph is directed.
    """
    if graph.is_directed:
        raise AttributeError('The graph must be undirected.')
    discovered = set()
    def _driver_connected_graph(n):
        discovered.add(n)
        for e in graph.get_edges(n):
            if e.n_to not in discovered:
                _driver_connected_graph(e.n_to)
    if len(vertices := list(graph.vertices)) == 0:
        return True
    _driver_connected_graph(vertices[0])
    return len(discovered) == len(graph.vertices)


def shortest_path(graph: Graph, start_node: object, end_node: object) -> Tuple[list, float]:
    """
    This method uses Dijkstra algorithm to find the shortest path from a start node to an end node.
    :param graph: the graph to inspect
    :param start_node: the node from where the algorithm must starts
    :param end_node: the end node of the algorithm
    :return: a tuple representing:
    (the edges of the shortest path from start_node to end_node, the overall distance between start_node and end_node).
    If the end_node is not reachable from the start_node, the result will be: ([], inf)
    :raises AttributeError: if the graph is not weighted or it's directed.
    :raises KeyError: if the graph not contains start_node.
    """
    if not graph.is_directed or not graph.is_weighted:
        raise AttributeError('The graph must be directed and weighted')
    if start_node not in graph:
        raise KeyError(f"The node {start_node=} is not in the graph")

    parents = {v: None for v in graph.vertices}
    distances = {v: float('inf') for v in graph.vertices}
    distances[start_node] = 0

    vertices = graph.vertices.copy()
    # Dijkstra algorithm
    while vertices:
        u = min(vertices, key=lambda v: distances[v])
        # if the extracted node ha infinite distance, it means that none is incident to that node, so terminate
        if distances[u] == float('inf'):
            break
        # if the extracted node is the end node, i can stop the Dijkstra algorithm
        if u == end_node:
            break
        for e in graph.get_edges(u):
            alt_route = distances[e.n_from] + e.cost
            if alt_route < distances[e.n_to]:
                parents[e.n_to] = e
                distances[e.n_to] = alt_route
        vertices.remove(u)

    if distances[end_node] == float('inf'):
        return [], float('inf')
    path = []
    tmp_node = end_node
    while tmp_node != start_node:
        path.insert(0, parents[tmp_node])
        tmp_node = parents[tmp_node].n_from
    return path, distances[end_node]


def is_dag(graph: Graph) -> bool:
    """
    Function that checks if the given directed graph is a DAG (Directed Acyclic Graph)
    :param graph: the input graph
    :return: True if the graph is a DAG (or if is empty), False otherwise
    :raise Attribute Error: if the graph is undirected.
    """
    if not graph.is_directed:
        raise AttributeError('The graph must be directed')
    n_incoming = {v: len(graph.incoming_edges(v)) for v in graph.vertices}
    s = [v for v in graph.vertices if n_incoming[v] == 0]
    while s:
        v = s[0]
        for _, u, *_ in graph.get_edges(v):
            n_incoming[u] -= 1
            if n_incoming[u] == 0:
                s.append(u)
        del s[0]
    return all(x == 0 for x in n_incoming.values()) or not bool(n_incoming.values())


def approx_vertex_cover(graph: Graph) -> set:
    """
    Function that finds the maximum vertex-cover of the given undirected graph.
    :param graph: the input graph
    :return: the maximum vertex-cover of the graph
    :raise AttributeError: if the input graph is a directed graph
    """
    if graph.is_directed:
        raise AttributeError('The graph must be undirected')
    vc = set()
    edges = list(graph.edges)
    while edges:
        n_from, n_to = edges[0]
        vc.add(n_from)
        vc.add(n_to)
        edges = [e for e in edges if e.n_from != n_from and e.n_from != n_to and e.n_to != n_from and e.n_to != n_to]
    return vc
