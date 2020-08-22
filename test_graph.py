import unittest
from graph import Graph, Node


def propagate(last_layer, current_layer):
    next_layer = []
    for node in current_layer:
        for edge in node.edges:
            next_node = edge.other(node)
            if next_node not in last_layer and next_node not in current_layer and next_node not in next_layer:
                next_layer.append(next_node)
    return next_layer


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(3, 0.5)

    def test_graphHasCorrectStartEdgesSet(self):
        start_values = []
        for node in self.graph.start_nodes:
            self.assertEqual(1, len(node.edges))
            start_values.append(node.left().value)
        self.assertEqual(['*', '*', '*', '?', '*', '?', '?', '?'], start_values)

    def test_graphHasCorrectEndEdgesSet(self):
        end_values = []
        for node in self.graph.end_nodes:
            self.assertEqual(1, len(node.edges))
            end_values.append(node.left().value)
        self.assertEqual(['*', '*', '*', '*', '?', '?', '?', '?'], sorted(end_values))

    def test_graphHasCorrectInnerNodesSet(self):
        self.assertEqual(24, len(self.graph.inner_nodes))
        for node in self.graph.inner_nodes:
            self.assertEqual(3, node.degree())

    def test_graphHasCorrectInnerVertexDegreesAndAmount(self):
        used_nodes = []
        queue = [node for node in self.graph.start_nodes]
        while len(queue):
            node = queue.pop()
            if node in used_nodes:
                continue
            used_nodes.append(node)
            node_degree = 1 if (node in self.graph.start_nodes or node in self.graph.end_nodes) else 3
            self.assertEqual(node_degree, node.degree())
            for edge in node.edges:
                if edge.other(node) not in used_nodes:
                    queue.append(edge.other(node))
        self.assertEqual(40, len(used_nodes))
        for node in self.graph.end_nodes:
            self.assertTrue(node in used_nodes)

    def test_graphHasCorrectInnerEdgesSet(self):
        used_nodes = []
        queue = [node for node in self.graph.start_nodes]
        while len(queue):
            node = queue.pop()
            if node in used_nodes:
                continue
            used_nodes.append(node)
            for edge in node.edges:
                if node.degree() == 3 == edge.other(node).degree():
                    self.assertEqual('?', edge.value)
                if edge.other(node) not in used_nodes:
                    queue.append(edge.other(node))

    def test_graphHasCorrectStructure(self):
        def does_edge_exist(first_node, second_node):
            for edge in first_node.edges:
                if edge.other(first_node) == second_node:
                    return True
            return False

        layers = [[],  [node for node in self.graph.start_nodes]]
        for layer_num in range(1, 5):
            layers.append(propagate(layers[layer_num - 1], layers[layer_num]))
        for layer in (layers[1:]):  # check amount of vertices in the layer.
            self.assertEqual(8, len(layer))
        for layer_num in range(2, len(layers)):  # check edges between layers.
            for i in range(len(layers[layer_num])):
                self.assertTrue(does_edge_exist(layers[layer_num - 1][i], layers[layer_num][i]))

        self.assertTrue(does_edge_exist(layers[2][0], layers[2][1]))
        self.assertTrue(does_edge_exist(layers[2][2], layers[2][3]))
        self.assertTrue(does_edge_exist(layers[2][4], layers[2][5]))
        self.assertTrue(does_edge_exist(layers[2][6], layers[2][7]))

        self.assertTrue(does_edge_exist(layers[3][0], layers[3][2]))
        self.assertTrue(does_edge_exist(layers[3][1], layers[3][3]))
        self.assertTrue(does_edge_exist(layers[3][4], layers[3][6]))
        self.assertTrue(does_edge_exist(layers[3][5], layers[3][7]))

        self.assertTrue(does_edge_exist(layers[4][0], layers[4][4]))
        self.assertTrue(does_edge_exist(layers[4][1], layers[4][5]))
        self.assertTrue(does_edge_exist(layers[4][2], layers[4][6]))
        self.assertTrue(does_edge_exist(layers[4][3], layers[4][7]))

    def test_graphHasCorrectNodeTypesSet(self):
        layers = [[], [node for node in self.graph.start_nodes]]
        for layer_num in range(1, 5):
            layers.append(propagate(layers[layer_num - 1], layers[layer_num]))
        for node in layers[1]:
            self.assertEqual(node.type, Node.NodeType.EDGE)
        for node in layers[5]:
            self.assertEqual(node.type, Node.NodeType.EDGE)
        for node in (layers[2][0], layers[2][2], layers[2][4], layers[2][6],
                     layers[3][0], layers[3][1], layers[3][4], layers[3][5],
                     layers[4][0], layers[4][1], layers[4][2], layers[4][3]):
            self.assertEqual(node.type, Node.NodeType.UPPER)
        for node in (layers[2][1], layers[2][3], layers[2][5], layers[2][7],
                     layers[3][2], layers[3][3], layers[3][6], layers[3][7],
                     layers[4][4], layers[4][5], layers[4][6], layers[4][7]):
            self.assertEqual(node.type, Node.NodeType.LOWER)

    def test_graphHasCorrectNodesByLayerDivision(self):
        layers = [[], [node for node in self.graph.start_nodes]]
        for layer_num in range(1, 5):
            layers.append(propagate(layers[layer_num - 1], layers[layer_num]))
        layers.pop(0)
        self.assertEqual(len(layers), len(self.graph.nodes_by_layer))
        for expected_layer, actual_layer in zip(layers, self.graph.nodes_by_layer):
            self.assertEqual(len(expected_layer), len(actual_layer))
            self.assertEqual(set(expected_layer), set(actual_layer))

    def test_graphHasCorrectEdgeOrders_verticalEdges(self):
        for layer in self.graph.inner_layers():
            for node in layer:
                def is_vertical_in_layer(edge):
                    for edge_node in edge.nodes:
                        if edge_node not in layer:
                            return False
                    return True
                self.assertFalse(is_vertical_in_layer(node.left()))
                self.assertTrue(is_vertical_in_layer(node.vertical()))
                self.assertFalse(is_vertical_in_layer(node.right()))

    def test_graphHasCorrectEdgeOrders_leftHorizontalEdges(self):
        for prev_layer, layer in zip(self.graph.nodes_by_layer[0:len(self.graph.nodes_by_layer) - 2],
                                     self.graph.inner_layers()):
            for node in layer:
                def is_from_prev_layer(edge):
                    prev_layer_nodes = sum([edge_node in prev_layer for edge_node in edge.nodes])
                    this_layer_nodes = sum([edge_node in layer for edge_node in edge.nodes])
                    return prev_layer_nodes == this_layer_nodes == 1
                self.assertTrue(is_from_prev_layer(node.left()))
                self.assertFalse(is_from_prev_layer(node.vertical()))
                self.assertFalse(is_from_prev_layer(node.right()))

    def test_graphHasCorrectEdgeOrders_rightHorizontalEdges(self):
        for layer, next_layer in zip(self.graph.inner_layers(),
                                     self.graph.nodes_by_layer[2:len(self.graph.nodes_by_layer)]):
            for node in layer:
                def is_from_next_layer(edge):
                    next_layer_nodes = sum([edge_node in next_layer for edge_node in edge.nodes])
                    this_layer_nodes = sum([edge_node in layer for edge_node in edge.nodes])
                    return next_layer_nodes == this_layer_nodes == 1
                self.assertFalse(is_from_next_layer(node.left()))
                self.assertFalse(is_from_next_layer(node.vertical()))
                self.assertTrue(is_from_next_layer(node.right()))

    def test_graphHasCorrectEdgeDirections_horizontalEdges(self):
        def get_layer(layer_node):
            for index, layer in enumerate(self.graph.nodes_by_layer):
                if layer_node in layer:
                    return index
            return len(self.graph.nodes_by_layer)
        for node in self.graph.inner_nodes:
            self.assertTrue(get_layer(node.left().nodes[0]) < get_layer(node.left().nodes[1]))
            self.assertTrue(get_layer(node.right().nodes[0]) < get_layer(node.right().nodes[1]))

    def test_graphHasCorrectEdgeDirections_verticalEdges(self):
        for node in self.graph.inner_nodes:
            self.assertEqual(node.vertical().nodes[0].type, Node.NodeType.UPPER)
            self.assertEqual(node.vertical().nodes[1].type, Node.NodeType.LOWER)

    def test_graphGetCopyReturnsCorrectCopy(self):
        graph_copy = self.graph.get_copy()
        self.assertEqual(len(self.graph.start_nodes), len(graph_copy.start_nodes))
        self.assertEqual(len(self.graph.inner_nodes), len(graph_copy.inner_nodes))
        self.assertEqual(len(self.graph.end_nodes), len(graph_copy.end_nodes))
        self.assertEqual(len(self.graph.nodes_by_layer), len(graph_copy.nodes_by_layer))
        for layer, layer_copy in zip(self.graph.nodes_by_layer, graph_copy.nodes_by_layer):
            for node, node_copy in zip(layer, layer_copy):
                self.assertEqual(node.type, node_copy.type)
                self.assertEqual(node.degree(), node_copy.degree())
                for edge, edge_copy in zip(node.edges, node_copy.edges):
                    self.assertEqual(edge.value, edge_copy.value)


if __name__ == '__main__':
    unittest.main()
