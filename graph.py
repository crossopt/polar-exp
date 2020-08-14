""" Module for creating and storing an encoding graph. """
from initialize import get_gates, get_endpoints
from enum import Enum


class Node:
    """ The node of the encoding graph, a single gate. """
    class NodeType(Enum):
        """ The type of node. All inner nodes are either lower or upper based on their edges. """
        EDGE = 0
        LOWER = 1
        UPPER = 2

    def __init__(self, node_type=NodeType.EDGE):
        self.type = node_type
        self.edges = []

    def add_edge(self, edge):
        """ Adds edge to node. One of the edge's endpoints should be this node. """
        self.edges.append(edge)

    def degree(self):
        """ Returns the node's degree. Should be 1 for outer vertices and 2 for inner ones. """
        return len(self.edges)

    def get_neighbor_types(self):
        """ Returns a sorted list of the node's edges' values. """
        return sorted([edge.value for edge in self.edges])

    def propagate(self):
        """ Sets all of the node's neighboring edges to '*'. """
        for edge in self.edges:
            edge.value = '*'


class Edge:
    """ The edge in the encoding graph. Each edge is marked either '?' or '*'. """
    def __init__(self, first_node, second_node, value='?'):
        self.nodes = {first_node, second_node}
        first_node.add_edge(self)
        second_node.add_edge(self)
        self.value = value

    def other(self, node):
        """ Returns the endpoint of the edge different from the given one. """
        for other_node in self.nodes:
            if other_node != node:
                return other_node


class Graph:
    """ Base class for storing a encoding graph. """
    def __init__(self, k, p):
        """
        Creates an encoding graph with the given parameters.

        :param k: the power of the amount of gates being encoded.
        :param p: the probability of error for the polar code.
        """
        # Create the original gates.
        self.start_nodes = [Node() for i in range(2 ** k)]
        self.inner_nodes = []
        current_layer = [i for i in self.start_nodes]

        for layer in range(k):
            for group_start in range(2 ** (k - layer - 1)):
                current_start = 2 ** (layer + 1) * group_start
                for gate_number in range(2 ** layer):
                    # Create new gate and add its edges to the graph.
                    new_top_gate = Node(node_type=Node.NodeType.UPPER)
                    new_bottom_gate = Node(node_type=Node.NodeType.LOWER)
                    self.inner_nodes.append(new_top_gate)
                    self.inner_nodes.append(new_bottom_gate)
                    top_gate_number = gate_number + current_start
                    bottom_gate_number = gate_number + current_start + 2 ** layer
                    top_edge = Edge(new_top_gate, current_layer[top_gate_number])
                    bottom_edge = Edge(new_bottom_gate, current_layer[bottom_gate_number])
                    gate_edge = Edge(new_bottom_gate, new_top_gate)
                    current_layer[top_gate_number] = new_top_gate
                    current_layer[bottom_gate_number] = new_bottom_gate

        # Create the endpoints.
        self.end_nodes = [Node() for i in range(2 ** k)]
        for gate, end_gate in zip(current_layer, self.end_nodes):
            edge = Edge(gate, end_gate)

        # Set the original values for the edges.
        for node, value in zip(self.start_nodes, get_gates(k, p)):
            node.edges[0].value = value
        for node, value in zip(self.end_nodes, get_endpoints(k, p)):
            node.edges[0].value = value
