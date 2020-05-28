import adt.graph.util.exceptions as exc
from adt.graph.core import Graph, Node, Edge, WeightedEdge
from typing import Set, Union


class AdjacencyListGraph(Graph):
    """
    This class is a representation of graph with adjacent list.
    """
    def __init__(self, *, directed: bool = False, weighted: bool = False):
        super().__init__(directed=directed, weighted=weighted)
        self._rev_adjacent_list = {}
        self._adjacent_list = {}

    @property
    def vertices(self) -> Set[object]:
        return set(self._adjacent_list.keys())

    @property
    def edges(self) -> Set[Union[Edge, WeightedEdge]]:
        return set.union(*self._adjacent_list.values())

    def get_edges(self, node: Node) -> Set[Union[Edge, WeightedEdge]]:
        # if the graph is directed, return the values from the adjacent list
        if self.is_directed:
            return self._adjacent_list[node]
        # if not return all
        else:
            rev_edges = set()
            # get all the reverse edges of the edge
            for n in self._rev_adjacent_list[node]:
                for e in self._adjacent_list[n]:
                    if e.node2 is node:
                        rev_edges.add(WeightedEdge(e.node2, e.node1, e.cost) if self.is_weighted else Edge(e.node2, e.node1))
            return set.union(rev_edges, self._adjacent_list[node])

    def incoming_edges(self, node: Node) -> Set[Union[Edge, WeightedEdge]]:
        if node not in self.vertices:
            raise exc.NotInGraph()
        if self.is_directed:
            return {e for v in self._rev_adjacent_list[node] for e in self._adjacent_list[v] if e.node2 is node}
        else:
            return self.get_edges(node)

    def add_vertex(self, node: Node, *nodes: Node) -> None:
        for node in (node,) + nodes:
            self._adjacent_list.setdefault(node, set())
            self._rev_adjacent_list.setdefault(node, set())

    def add_edge(self, node_from: Node, node_to: Node, *nodes_to: Node, cost: object = 0, reverse: bool = False) -> None:
        for node in (nodes_to := (node_to,) + nodes_to) + (node_from,):
            if node not in self._adjacent_list:
                raise exc.NotInGraph()

        for dst_node in nodes_to:
            edges = self._adjacent_list.get(node_from)
            new_edge = WeightedEdge(node_from, dst_node, cost) if self.is_weighted else Edge(node_from, dst_node)
            if self.is_directed or dst_node not in self._rev_adjacent_list[node_from]:
                edges.add(new_edge)
                self._rev_adjacent_list[dst_node].add(node_from)

        if self.is_directed and reverse:
            for node in nodes_to:
                self.add_edge(node, node_from, cost=cost, reverse=False)

    def remove_vertex(self, node: Node) -> None:
        for node_from in self._rev_adjacent_list[node]:
            self._adjacent_list[node_from] = {edge for edge in self._adjacent_list[node_from] if edge.node2 != node}
        for node_from in (n for n in self._rev_adjacent_list if n != node):
            self._rev_adjacent_list[node_from].remove(node)
        del self._adjacent_list[node]
        del self._rev_adjacent_list[node]

    def remove_edge(self, edge: tuple) -> bool:
        node_from, node_to = edge
        if not self.is_directed and self._rev_adjacent_list[node_from] is not None:
            self._adjacent_list[node_to] = {e for e in self._adjacent_list[node_to] if e.node2 != node_from}
            self._adjacent_list[node_from] = {e for e in self._adjacent_list[node_from] if e.node2 != node_to}
            rem1, rem2 = True, True
            try:
                self._rev_adjacent_list[node_from].remove(node_to)
            except KeyError:
                rem1 = False
            try:
                self._rev_adjacent_list[node_to].remove(node_from)
            except KeyError:
                rem2 = False
            return rem1 or rem2
        else:
            try:
                self._adjacent_list[node_from] = {e for e in self._adjacent_list[node_from] if e.node2 != node_to}
                self._rev_adjacent_list[node_to].remove(node_from)
                return True
            except KeyError:
                return False
