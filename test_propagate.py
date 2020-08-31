import unittest
from graph import Graph
from propagate import lazy_propagate, was_propagation_finished, default_stopping_condition,\
    flooding_propagate, naive_propagate, successive_cancellation_propagate,\
    scheduling_conventional_propagate, scheduling_round_trip_propagate


class TestLazyPropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        lazy_propagate(graph)
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)

    def test_propagationFinishesCorrectly(self):
        graph = Graph(7, 0.7)
        second_graph = graph.get_copy()
        self.assertTrue(was_propagation_finished(graph, second_graph))
        lazy_propagate(graph)
        self.assertFalse(was_propagation_finished(graph, second_graph))
        lazy_propagate(second_graph)
        self.assertTrue(was_propagation_finished(graph, second_graph))


class TestNaivePropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        naive_propagate(graph, default_stopping_condition(graph))
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)

    def test_propagationFinishesCorrectly(self):
        graph = Graph(7, 0.7)
        second_graph = graph.get_copy()
        lazy_propagate(graph)
        naive_propagate(second_graph, default_stopping_condition(second_graph))
        self.assertTrue(was_propagation_finished(graph, second_graph))


class TestFloodingPropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        flooding_propagate(graph, default_stopping_condition(graph))
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)

    def test_propagationFinishesCorrectly(self):
        graph = Graph(7, 0.7)
        second_graph = graph.get_copy()
        lazy_propagate(graph)
        flooding_propagate(second_graph, default_stopping_condition(second_graph))
        self.assertTrue(was_propagation_finished(graph, second_graph))


class TestSimpleSchedulingPropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        scheduling_conventional_propagate(graph, default_stopping_condition(graph))
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)

    def test_propagationFinishesCorrectly(self):
        graph = Graph(7, 0.7)
        second_graph = graph.get_copy()
        lazy_propagate(graph)
        scheduling_conventional_propagate(second_graph, default_stopping_condition(second_graph))
        self.assertTrue(was_propagation_finished(graph, second_graph))


class TestRoundTripSchedulingPropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        scheduling_round_trip_propagate(graph, default_stopping_condition(graph))
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)

    def test_propagationFinishesCorrectly(self):
        graph = Graph(7, 0.7)
        second_graph = graph.get_copy()
        lazy_propagate(graph)
        scheduling_round_trip_propagate(second_graph, default_stopping_condition(second_graph))
        self.assertTrue(was_propagation_finished(graph, second_graph))


class TestSuccessiveCancellationPropagate(unittest.TestCase):
    def test_propagationSetsAllEdges(self):
        graph = Graph(3, 0.1)
        successive_cancellation_propagate(graph, default_stopping_condition(graph))
        for node in graph.inner_nodes:
            for edge in node.edges:
                self.assertEqual('*', edge.value)

    def test_propagationFinishesCorrectly(self):
        graph = Graph(7, 0.7)
        second_graph = graph.get_copy()
        lazy_propagate(graph)
        successive_cancellation_propagate(second_graph, default_stopping_condition(second_graph))
        self.assertTrue(was_propagation_finished(graph, second_graph))


if __name__ == '__main__':
    unittest.main()
