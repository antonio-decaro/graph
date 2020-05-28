import numpy as np
import adt.graph.util.exceptions as exc
from typing import Set, Union
from adt.graph.util.bidict import Bidict
from adt.graph.core import Graph, Node, Edge, WeightedEdge


class AdjacencyMatrixGraph(Graph):
	"""
	Graph implementation with Adjacent Matrix
	"""
	def __init__(self, *, directed: bool = False, weighted: bool = False):
		super().__init__(directed=directed, weighted=weighted)
		# this variable contains the node indexes
		self._nodes_indexes = Bidict()
		# this variable represents the adjacent matrix
		self._matrix = np.array([], dtype=object)

	@property
	def matrix(self) -> np.ndarray:
		"""
		Property
		:return: a copy of the adjacency matrix of the graph
		"""
		return self._matrix.copy()

	@property
	def vertices(self) -> Set[Node]:
		return set(self._nodes_indexes.keys())

	@property
	def edges(self) -> Set[Union[Edge, WeightedEdge]]:
		sets = set.union(*(self.get_edges(node) for node in self._nodes_indexes))
		return sets

	def get_edges(self, node: Node) -> Set[Union[Edge, WeightedEdge]]:
		# check if the node is in the graph
		if self._nodes_indexes.get(node) is None:
			raise exc.NotInGraph()

		# get the row of the edges that starts with input node
		row = self._matrix[self._nodes_indexes[node]]
		# get all the edges incidents to the node
		if self.is_weighted:
			fs = {WeightedEdge(node, self._nodes_indexes.inverse[i][0], row[i]) for i in range(len(row)) if row[i] is not None}
		else:
			fs = {Edge(node, self._nodes_indexes.inverse[i][0]) for i in range(len(row)) if row[i] is not None}

		return fs

	def incoming_edges(self, node: Node) -> Set[Union[Edge, WeightedEdge]]:
		# if the graph is undirected, this method is equals to get_edges
		if not self.is_directed:
			return self.get_edges(node)

		# check if the node is in the graph
		if self._nodes_indexes.get(node) is None:
			raise exc.NotInGraph()

		# get the row of the edges that starts with input node
		col = self._matrix[:, self._nodes_indexes[node]]
		# get all the edges incidents to the node
		if self.is_weighted:
			bs = {WeightedEdge(self._nodes_indexes.inverse[i][0], node, col[i]) for i in range(len(col)) if col[i] is not None}
		else:
			bs = {Edge(self._nodes_indexes.inverse[i][0], node) for i in range(len(col)) if col[i] is not None}

		return bs

	def __new_node_idx(self, node: Node) -> int:
		"""
		Inspect the graph to get the index of a new node
		:param node: the node from which get the index
		:return: index of the new node
		"""
		return len(self._nodes_indexes)

	def add_vertex(self, node: Node, *nodes: Node) -> None:
		# iter the process for all input nodes
		for node in (node,) + nodes:
			# check if the node is already in graph
			if self._nodes_indexes.get(node) is not None:
				raise exc.AlreadyInGraph()

			# assign an index to the node to insert
			self._nodes_indexes[node] = self.__new_node_idx(node)

			# get index of the matrix
			idx = self._nodes_indexes[node]

			# if the size of the array greater than 1, reshape to build the matrix
			if len(self._nodes_indexes) == 1:
				self._matrix = np.insert(self._matrix, idx, [None])
				self._matrix = np.reshape(self._matrix, (1, 1))

			# add a raw and a column only if the matrix is at least a 1x1 size
			if len(self._nodes_indexes) > 1:
				# append the node to the adjacent matrix
				self._matrix = np.insert(self._matrix, idx, [None], axis=0)
				self._matrix = np.insert(self._matrix, idx, [None], axis=1)

	def add_edge(self, node_from: Node, node_to: Node, *nodes_to: Node, cost: object = 0, reverse: bool = False) -> None:
		# get the index of the from node and check if the from node is in the graph
		if (idx_from := self._nodes_indexes.get(node_from)) is None:
			raise exc.NotInGraph()

		# iter the process to all destination nodes
		for node_to in (node_to,) + nodes_to:
			# get the index of the destination node and check if the destination node is in the graph
			if (idx_to := self._nodes_indexes.get(node_to)) is None:
				raise exc.NotInGraph()

			# get the value of the edge, if is weighted, the value will be the cost of the edge
			edge_val = cost if self.is_weighted else 1

			# insert the edge cost to the adjacent matrix
			self._matrix[idx_from, idx_to] = edge_val

			# i symmetrically insert the same edge if the graph is not directed
			if not self.is_directed:
				self._matrix[idx_to, idx_from] = edge_val

			# repeat this process if the reverse mode is selected and the graph is directed
			if reverse and self.is_directed:
				self.add_edge(node_to, node_from, cost=cost, reverse=False)

	def remove_vertex(self, node: Node) -> None:
		if self._nodes_indexes.get(node) is None:
			return

		# get the value of the index node to remove
		rem_idx = self._nodes_indexes[node]

		# remove the i-th column and row from the matrix
		self._matrix = np.delete(self._matrix, rem_idx, axis=0)
		self._matrix = np.delete(self._matrix, rem_idx, axis=1)

		# remove the vertex from the dict of vertex and index
		del self._nodes_indexes[node]

		# update the remaining indexes
		self._nodes_indexes = Bidict({self._nodes_indexes.inverse[i][0]: (i if i < rem_idx else i - 1) for i in self._nodes_indexes.inverse})

	def remove_edge(self, edge: tuple) -> bool:
		node_from, node_to = edge

		# check if the nodes are in the graph
		if self._nodes_indexes.get(node_from) is None or self._nodes_indexes.get(node_to) is None:
			raise exc.NotInGraph()

		# get the indexes of the nodes
		idx_from, idx_to = self._nodes_indexes[node_from], self._nodes_indexes[node_to]

		# if the edge does not exists, return false
		if self._matrix[idx_from, idx_to] is None:
			return False

		# else remove the edge
		self._matrix[idx_from, idx_to] = None

		# remove the other side if the graph is undirected
		if not self.is_directed:
			self._matrix[idx_to, idx_from] = None

		return True
