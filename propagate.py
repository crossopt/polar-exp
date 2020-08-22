""" Module for the various strategies of belief propagation. """
from rules import relevant_rule, left_rule, right_rule, vertical_rule


def was_propagation_finished(propagated_graph, graph):
    """ A simple cutoff for the propagation, checks whether the graph is equal to the graph optimally propagated. """
    for propagated_node, node in zip(propagated_graph.inner_nodes, graph.inner_nodes):
        for propagated_edge, edge in zip(propagated_node.edges, node.edges):
            if propagated_edge.value != edge.value:
                return False
    return True


def default_stopping_condition(original_graph):
    """ The current default stopping condition. Propagation stops once the graph has been fully propagated. """
    propagated_graph = original_graph.get_copy()
    lazy_propagate(propagated_graph)

    def should_stop(graph):
        return was_propagation_finished(propagated_graph, graph)
    return should_stop


def lazy_propagate(graph):
    """ Applies the propagation rules to all nodes in the graph while there was a single success. """
    was_success = True
    while was_success:
        was_success = False
        for node in graph.inner_nodes:
            was_success = was_success or relevant_rule(node)


def flooding_propagate(graph, stopping_condition):
    """ Applies the propagation rules using flooding propagation until stopping_condition is satisfied.

    In a single iteration, flooding propagation applies the relevant rules in all vertices simultaneously in parallel.
    """
    while not stopping_condition(graph):
        nodes_to_update = []
        for node in graph.inner_nodes:
            # Add node to a list of nodes to update to mock the parallel execution of the rule checks.
            # TODO left/right rules here?
            if relevant_rule(node, apply_propagate=False):
                nodes_to_update.append(node)
        for node in nodes_to_update:
            relevant_rule(node)


def scheduling_conventional_propagate(graph, stopping_condition):
    """ Applies the propagation rules using basic scheduling propagation until stopping_condition is satisfied.

    In a single iteration, conventional scheduling iterates over all of the inner layers in order and applies the
    relevant rules in all vertices in a layer simultaneously.
    """
    while not stopping_condition(graph):
        for layer in graph.inner_layers():
            # TODO All upper/lower nodes can be applied first here, think about this & vertical propagation.
            for node in layer:
                left_rule(node)
                right_rule(node)


def scheduling_round_trip_propagate(graph, stopping_condition):
    """ Applies the propagation rules using round-trip scheduling propagation until stopping_condition is satisfied.

    In a single iteration, round-trip scheduling iterates over all of the inner layers twice. On the first iteration it
    applies all of the left-rules to update the left edges' values for the vertices of the layer, and on the second
    iterations it applies all of the right-rules to update the right edges' values for the vertices of the layer.
    """
    while not stopping_condition(graph):
        for layer in graph.inner_layers():
            for node in layer:
                left_rule(node)
        for layer in graph.inner_layers():
            for node in layer:
                right_rule(node)
