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
            start_values.append(node.edges[0].value)
        self.assertEqual(['*', '*', '*', '?', '*', '?', '?', '?'], start_values)

    def test_graphHasCorrectEndEdgesSet(self):
        end_values = []
        for node in self.graph.end_nodes:
            self.assertEqual(1, len(node.edges))
            end_values.append(node.edges[0].value)
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
        layers = [[],  [node for node in self.graph.start_nodes]]
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


if __name__ == '__main__':
    unittest.main()
