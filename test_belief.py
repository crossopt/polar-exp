import unittest
from graph import Node, Edge, Graph
from belief import upper_rule, lower_rule, lazy_propagate


class TestUpperRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.UPPER
        self.edges = [Edge(self.nodes[0], self.nodes[1]),
                      Edge(self.nodes[0], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[3])]

    def test_upperRuleNoUnknownBits(self):
        for edge, value in zip(self.edges, ['*', '*', '*']):
            edge.value = value
        self.assertFalse(upper_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_upperRuleAllUnknownBits(self):
        for edge, value in zip(self.edges, ['?', '?', '?']):
            edge.value = value
        self.assertFalse(upper_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['?', '?', '?']):
            self.assertEqual(value, edge.value)

    def test_upperRuleOneUnknownBit(self):
        for edge, value in zip(self.edges, ['?', '*', '*']):
            edge.value = value
        self.assertTrue(upper_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_upperRuleTwoUnknownBits(self):
        for edge, value in zip(self.edges, ['?', '*', '?']):
            edge.value = value
        self.assertFalse(upper_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['?', '*', '?']):
            self.assertEqual(value, edge.value)

    def test_upperRuleWrongType(self):
        for edge, value in zip(self.edges, ['?', '*', '*']):
            edge.value = value
        self.nodes[0].type = Node.NodeType.EDGE
        self.assertFalse(upper_rule(self.nodes[0]))
        self.nodes[0].type = Node.NodeType.LOWER
        self.assertFalse(upper_rule(self.nodes[0]))
        self.nodes[0].type = Node.NodeType.UPPER
        self.assertTrue(upper_rule(self.nodes[0]))


class TestLowerRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.LOWER
        self.edges = [Edge(self.nodes[0], self.nodes[1]),
                      Edge(self.nodes[0], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[3])]

    def test_lowerRuleNoUnknownBits(self):
        for edge, value in zip(self.edges, ['*', '*', '*']):
            edge.value = value
        self.assertFalse(lower_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_lowerRuleAllUnknownBits(self):
        for edge, value in zip(self.edges, ['?', '?', '?']):
            edge.value = value
        self.assertFalse(lower_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['?', '?', '?']):
            self.assertEqual(value, edge.value)

    def test_lowerRuleOneUnknownBit(self):
        for edge, value in zip(self.edges, ['?', '*', '*']):
            edge.value = value
        self.assertTrue(lower_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_lowerRuleTwoUnknownBits(self):
        for edge, value in zip(self.edges, ['?', '*', '?']):
            edge.value = value
        self.assertTrue(lower_rule(self.nodes[0]))
        for edge, value in zip(self.edges, ['*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_lowerRuleWrongType(self):
        for edge, value in zip(self.edges, ['?', '*', '*']):
            edge.value = value
        self.nodes[0].type = Node.NodeType.EDGE
        self.assertFalse(lower_rule(self.nodes[0]))
        self.nodes[0].type = Node.NodeType.UPPER
        self.assertFalse(lower_rule(self.nodes[0]))
        self.nodes[0].type = Node.NodeType.LOWER
        self.assertTrue(lower_rule(self.nodes[0]))


class TestLazyPropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        lazy_propagate(graph)
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)


if __name__ == '__main__':
    unittest.main()
