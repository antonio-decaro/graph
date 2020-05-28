import abc
import collections
from typing import Set, Union

Edge = collections.namedtuple('Edge', 'n_from n_to')
WeightedEdge = collections.namedtuple('Edge', 'n_from n_to cost')


class Node:
	"""
	This class models a single item of a graph.
	"""
	def __init__(self, label: object, **kwargs: dict):
		self._label = label
		for varname in kwargs:
			setattr(self, varname, kwargs[varname])

	@property
	def label(self) -> object:
		"""
		Property
		:return: the label of the node
		"""
		return self._label

	@label.setter
	def label(self, new_label: object) -> None:
		"""
		Setter
		:param new_label: the new label value
		"""
		self._label = new_label

	def __str__(self):
		return self._label

	__repr__ = __str__


class Graph(abc.ABC):
	def __init__(self, *, directed: bool = False, weighted: bool = False):
		"""
		Instance initializer
		:param directed: true if is a directed graph, false otherwise
		:param weighted: true if is a weighted graph, false otherwise
		"""
		self._prop_directed = directed
		self._prop_weighted = weighted
		self._weights = {} if weighted else None

	@property
	def is_directed(self) -> bool:
		"""
		Property
		:return: True if is a directed graph, False otherwise
		"""
		return self._prop_directed

	@property
	def is_weighted(self) -> bool:
		"""
		Property
		:return: True if is a weighted graph, False otherwise
		"""
		return self._prop_weighted

	@property
	def vertices(self) -> Set[Node]:
		"""
		Property
		:return: the vertices of the graph
		"""
		raise NotImplementedError()

	@property
	def edges(self) -> Set[Union[Edge, WeightedEdge]]:
		"""
		Property
		:return: the nodes of the graph
		"""
		raise NotImplementedError()

	def get_edges(self, node: Node) -> Set[Union[Edge, WeightedEdge]]:
		"""
		Returns all the edges of a given node.
		If the node doesn't exist, will be raise an Exception
		:param node: the first end of the edges
		:return: all the edges that starts from the given node
		:raises: KeyError
		"""
		raise NotImplementedError()

	def incoming_edges(self, node: Node) -> Set[Union[Edge, WeightedEdge]]:
		"""
		Gets the incoming edges of a given node.
		:param node: The node to check. The node must be in the graph
		:return: The set of the incoming edges of the input node
		:raise AttributeError: if the input node is not in the graph
		"""
		raise NotImplementedError()

	def add_vertex(self, node: Node, *nodes: Node) -> None:
		"""
		This method adds a vertex to the a.
		If the vertex already exists, nothing changes.
		Note: the vertex will be added without any edge.
		:param node: the vertex to add
		:param nodes: other vertexes to add
		:return: None
		"""
		raise NotImplementedError()

	def add_edge(self, node_from: Node, node_to: Node, *nodes_to: Node, cost: object = 0, reverse: bool = False) -> None:
		"""
		Adds an edge in the a.
		The node_from must exists, otherwise an exception will be raised.
		:param node_from: the node which the edge starts
		:param node_to: the end node of the edge
		:param nodes_to: optional argument that indicate if the the a must add other edges.
		:param cost: This parameter can be used only if the a is weighted.
		Represents the cost of this (of those) edges.
		:param reverse: This parameter can be used only if the a is a directed-a.
		If this parameter is True (default), then the edge will be added to the destination node to.
		:return: None
		:raises: AttributeError
		"""
		raise NotImplementedError()

	def remove_vertex(self, node: Node) -> None:
		"""
		Remove a vertex from the graph.
		If the edge doesn't exists, nothing will change.
		:param node: the vertex to remove
		:return: None
		"""
		raise NotImplementedError()

	def remove_edge(self, edge: tuple) -> bool:
		"""
		Removes an edge from the graph.
		If the edge doesn't exists, nothing will change.
		:param edge: a tuple of the form (node_from, node_to). In undirected a, the order doesn't matters.
		:return: True if removes an edge, False otherwise
		:raises: KeyError if the selected nodes don't exist
		"""
		raise NotImplementedError()

	def __getitem__(self, item):
		try:
			return self.get_edges(item)
		except KeyError:
			return None

	def __str__(self) -> str:
		properties = ' | '.join((f'{prop}={vars(self)[prop]}'[6:] for prop in vars(self) if 'prop' in prop))
		state = f'Nodes={self.vertices}\nEdges={self.edges}'
		return properties + '\n' + state

	__repr__ = __str__
