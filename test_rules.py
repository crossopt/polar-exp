import unittest
from graph import Node, Edge
from rules import upper_rule, lower_rule, vertical_rule, left_rule, right_rule


class TestUpperRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.UPPER
        self.edges = [Edge(self.nodes[1], self.nodes[0]),
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

    def test_upperRuleDoNotApplyPropagate(self):
        for edge, value in zip(self.edges, ['?', '*', '*']):
            edge.value = value
        self.assertTrue(upper_rule(self.nodes[0], apply_propagate=False))
        for edge, value in zip(self.edges, ['?', '*', '*']):
            self.assertEqual(value, edge.value)


class TestLowerRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.LOWER
        self.edges = [Edge(self.nodes[1], self.nodes[0]),
                      Edge(self.nodes[2], self.nodes[0]),
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

    def test_lowerRuleDoNotApplyPropagate(self):
        for edge, value in zip(self.edges, ['?', '*', '*']):
            edge.value = value
        self.assertTrue(lower_rule(self.nodes[0], apply_propagate=False))
        for edge, value in zip(self.edges, ['?', '*', '*']):
            self.assertEqual(value, edge.value)


class TestVerticalRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.UPPER
        self.nodes[2].type = Node.NodeType.LOWER
        self.edges = [Edge(self.nodes[1], self.nodes[0]),
                      Edge(self.nodes[4], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[3]),
                      Edge(self.nodes[2], self.nodes[5])]

    def test_verticalRuleEdgeIsKnown(self):
        for edge, value in zip(self.edges, ['?', '*', '*', '*', '?']):
            edge.value = value
        self.assertFalse(vertical_rule(self.nodes[0]))
        self.assertFalse(vertical_rule(self.nodes[2]))
        for edge, value in zip(self.edges, ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_verticalRuleEdgeIsNotPropagated(self):
        for edge, value in zip(self.edges, ['*', '?', '?', '?', '?']):
            edge.value = value
        self.assertFalse(vertical_rule(self.nodes[0]))
        self.assertFalse(vertical_rule(self.nodes[2]))
        for edge, value in zip(self.edges, ['*', '?', '?', '?', '?']):
            self.assertEqual(value, edge.value)

    def test_verticalRuleEdgeIsPropagated_fromLower(self):
        for edge, value in zip(self.edges,  ['?', '*', '?', '?', '?']):
            edge.value = value
        self.assertTrue(vertical_rule(self.nodes[0]))
        for edge, value in zip(self.edges,  ['?', '*', '*', '?', '*']):
            self.assertEqual(value, edge.value)

    def test_verticalRuleEdgeIsPropagated_fromUpper(self):
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            edge.value = value
        self.assertTrue(vertical_rule(self.nodes[2]))
        for edge, value in zip(self.edges,  ['*', '?', '*', '*', '?']):
            self.assertEqual(value, edge.value)

    def test_verticalRuleDoNotApplyPropagate(self):
        for edge, value in zip(self.edges,  ['?', '*', '?', '?', '?']):
            edge.value = value
        self.assertTrue(vertical_rule(self.nodes[0], apply_propagate=False))
        for edge, value in zip(self.edges,  ['?', '*', '?', '?', '?']):
            self.assertEqual(value, edge.value)


class TestLeftRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.UPPER
        self.nodes[2].type = Node.NodeType.LOWER
        self.edges = [Edge(self.nodes[1], self.nodes[0]),
                      Edge(self.nodes[4], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[3]),
                      Edge(self.nodes[2], self.nodes[5])]

    def test_leftRuleEdgeIsKnown(self):
        for edge, value in zip(self.edges, ['*', '*', '?', '?', '?']):
            edge.value = value
        self.assertFalse(left_rule(self.nodes[0]))
        self.assertFalse(left_rule(self.nodes[2]))
        for edge, value in zip(self.edges, ['*', '*', '?', '?', '?']):
            self.assertEqual(value, edge.value)

    def test_leftRuleEdgeIsNotPropagated(self):
        for edge, value in zip(self.edges, ['?', '?', '?', '*', '?']):
            edge.value = value
        self.assertFalse(left_rule(self.nodes[0]))
        self.assertFalse(left_rule(self.nodes[2]))
        for edge, value in zip(self.edges, ['?', '?', '?', '*', '?']):
            self.assertEqual(value, edge.value)

    def test_leftRuleEdgeIsPropagated_simpleUpper(self):
        for edge, value in zip(self.edges,  ['?', '?', '*', '*', '?']):
            edge.value = value
        self.assertTrue(left_rule(self.nodes[0]))
        for edge, value in zip(self.edges,  ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_leftRuleEdgeIsPropagated_simpleLower(self):
        for edge, value in zip(self.edges,  ['?', '?', '?', '?', '*']):
            edge.value = value
        self.assertTrue(left_rule(self.nodes[2]))
        for edge, value in zip(self.edges,  ['?', '*', '*', '?', '*']):
            self.assertEqual(value, edge.value)

    def test_leftRuleEdgeIsPropagated_verticalUpper(self):
        for edge, value in zip(self.edges,  ['?', '*', '?', '*', '?']):
            edge.value = value
        self.assertTrue(left_rule(self.nodes[0]))
        for edge, value in zip(self.edges,  ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_leftRuleEdgeIsPropagated_verticalLower(self):
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            edge.value = value
        self.assertTrue(left_rule(self.nodes[2]))
        for edge, value in zip(self.edges,  ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_leftRuleDoNotApplyPropagate(self):
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            edge.value = value
        self.assertTrue(left_rule(self.nodes[2], apply_propagate=False))
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            self.assertEqual(value, edge.value)


class TestRightRule(unittest.TestCase):
    def setUp(self):
        self.nodes = [Node(), Node(), Node(), Node(), Node(), Node()]
        self.nodes[0].type = Node.NodeType.UPPER
        self.nodes[2].type = Node.NodeType.LOWER
        self.edges = [Edge(self.nodes[1], self.nodes[0]),
                      Edge(self.nodes[4], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[2]),
                      Edge(self.nodes[0], self.nodes[3]),
                      Edge(self.nodes[2], self.nodes[5])]

    def test_rightRuleEdgeIsKnown(self):
        for edge, value in zip(self.edges, ['?', '?', '?', '*', '*']):
            edge.value = value
        self.assertFalse(right_rule(self.nodes[0]))
        self.assertFalse(right_rule(self.nodes[2]))
        for edge, value in zip(self.edges, ['?', '?', '?', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_rightRuleEdgeIsNotPropagated(self):
        for edge, value in zip(self.edges, ['*', '?', '?', '?', '?']):
            edge.value = value
        self.assertFalse(right_rule(self.nodes[0]))
        self.assertFalse(right_rule(self.nodes[2]))
        for edge, value in zip(self.edges, ['*', '?', '?', '?', '?']):
            self.assertEqual(value, edge.value)

    def test_rightRuleEdgeIsPropagated_simpleUpper(self):
        for edge, value in zip(self.edges,  ['*', '?', '*', '?', '?']):
            edge.value = value
        self.assertTrue(right_rule(self.nodes[0]))
        for edge, value in zip(self.edges,  ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_rightRuleEdgeIsPropagated_simpleLower(self):
        for edge, value in zip(self.edges,  ['?', '*', '?', '?', '?']):
            edge.value = value
        self.assertTrue(right_rule(self.nodes[2]))
        for edge, value in zip(self.edges,  ['?', '*', '*', '?', '*']):
            self.assertEqual(value, edge.value)

    def test_rightRuleEdgeIsPropagated_verticalUpper(self):
        for edge, value in zip(self.edges,  ['*', '?', '?', '?', '*']):
            edge.value = value
        self.assertTrue(right_rule(self.nodes[0]))
        for edge, value in zip(self.edges,  ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_rightRuleEdgeIsPropagated_verticalLower(self):
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            edge.value = value
        self.assertTrue(right_rule(self.nodes[2]))
        for edge, value in zip(self.edges,  ['*', '*', '*', '*', '*']):
            self.assertEqual(value, edge.value)

    def test_rightRuleDoNotApplyPropagate(self):
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            edge.value = value
        self.assertTrue(right_rule(self.nodes[2], apply_propagate=False))
        for edge, value in zip(self.edges,  ['*', '?', '?', '*', '?']):
            self.assertEqual(value, edge.value)


if __name__ == '__main__':
    unittest.main()
