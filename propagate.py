""" Module for the various strategies of belief propagation. """
from rules import relevant_rule, left_rule, right_rule, left_rule_list, right_rule_list
from graph import Node


class Counter:
    def __init__(self):
        self.steps = 0
        self.parallel_steps = 0


def was_propagation_finished(propagated_graph, graph):
    """ A simple cutoff for the propagation, checks whether the graph is equal to the graph optimally propagated. """
    for propagated_node, node in zip(propagated_graph.inner_nodes, graph.inner_nodes):
        # Because of the way scheduling (does not) handle vertical edges, they may not be propagated even when all the
        # neighboring edges have already been set.
        for propagated_edge, edge in zip(propagated_node.edges[0::2], node.edges[0::2]):
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
            was_success = relevant_rule(node) or was_success


def naive_propagate(graph, stopping_condition):
    """ Applies the propagation rules using naive propagation until stopping_condition is satisfied.

    In a single iteration, naive propagation applies the relevant rules in all vertices simultaneously in parallel.
    Returns the amount of steps (left or right) that the propagation took, or None if the propagation failed.
    """
    counter = Counter()
    while not stopping_condition(graph):
        nodes_to_update = []
        counter.parallel_steps += 1
        for node in graph.inner_nodes:
            # Add node to a list of nodes to update to mock the parallel execution of the rule checks.
            counter.steps += 2
            if left_rule(node, apply_propagate=False) or right_rule(node, apply_propagate=False):
                nodes_to_update.append(node)
        for node in nodes_to_update:
            left_rule(node)
            right_rule(node)
    return counter


def flooding_propagate(graph, stopping_condition):
    """ Applies the propagation rules using flooding propagation until stopping_condition is satisfied.

    In a single iteration, flooding propagation applies the relevant rules in all vertices the neighbors of which had
    been updated last iteration simultaneously in parallel.
    Returns the amount of steps (left or right) that the propagation took, or None if the propagation failed.
    """
    counter = Counter()
    interesting_nodes = []
    for node in graph.start_nodes:
        for edge in node.edges:
            interesting_nodes.append(edge.other(node))
    for node in graph.end_nodes:
        for edge in node.edges:
            interesting_nodes.append(edge.other(node))
    while not stopping_condition(graph):
        nodes_to_update = []
        counter.parallel_steps += 1
        for node in graph.inner_nodes:
            add_value = (node not in interesting_nodes) + 1
            if not (node in interesting_nodes or node.vertical().other(node) in interesting_nodes):
                continue
            # Add node to a list of nodes to update to mock the parallel execution of the rule checks.
            counter.steps += add_value  # We know the rule since we know from where the counter was updated.
            if right_rule(node, apply_propagate=False) or left_rule(node, apply_propagate=False):
                nodes_to_update.append(node)
        interesting_nodes = []
        for node in nodes_to_update:
            interesting_nodes += left_rule_list(node)
            interesting_nodes += right_rule_list(node)
    return counter


def scheduling_conventional_propagate(graph, stopping_condition):
    """ Applies the propagation rules using basic scheduling propagation until stopping_condition is satisfied.

    In a single iteration, conventional scheduling iterates over all of the inner layers in order and applies the
    relevant rules in all vertices in a layer simultaneously.
    Returns the amount of steps (left or right) that the propagation took, or None if the propagation failed.
    """
    counter = Counter()
    while not stopping_condition(graph):
        for layer in graph.inner_layers():
            counter.parallel_steps += 1
            nodes_to_update = []
            for node in layer:
                counter.steps += 2
                if left_rule(node, apply_propagate=False) or right_rule(node, apply_propagate=False):
                    nodes_to_update.append(node)
            for node in nodes_to_update:
                left_rule(node)
                right_rule(node)
    return counter


def scheduling_round_trip_propagate(graph, stopping_condition):
    """ Applies the propagation rules using round-trip scheduling propagation until stopping_condition is satisfied.

    In a single iteration, round-trip scheduling iterates over all of the inner layers twice. On the first iteration it
    applies all of the left-rules to update the left edges' values for the vertices of the layer, and on the second
    iterations it applies all of the right-rules to update the right edges' values for the vertices of the layer.
    Returns the amount of steps (left or right) that the propagation took, or None if the propagation failed.
    """
    counter = Counter()
    while not stopping_condition(graph):
        for layer in graph.inner_layers()[::-1]:
            counter.parallel_steps += 1
            nodes_to_update = []
            for node in layer:
                counter.steps += 1
                if left_rule(node, apply_propagate=False):
                    nodes_to_update.append(node)
            for node in nodes_to_update:
                left_rule(node)
        for layer in graph.inner_layers():
            counter.parallel_steps += 1
            nodes_to_update = []
            for node in layer:
                counter.steps += 1
                if right_rule(node, apply_propagate=False):
                    nodes_to_update.append(node)
            for node in nodes_to_update:
                right_rule(node)
    return counter


def successive_cancellation_propagate(graph, stopping_condition):
    """ Applies the propagation rules using successive cancellation propagation until stopping_condition is satisfied.

    Successive cancellation has no iterations per se. It recursively decodes the whole graph in O(n log n) steps.
    Returns the amount of steps (left or right) that the propagation took, or None if the propagation failed.
    """
    counter = Counter()

    def apply_successive_cancellation(node_list):
        if not node_list:
            return
        upper_nodes = []
        lower_nodes = []
        counter.parallel_steps += 1  # Left updates can be parallel here
        for node in node_list:
            if node.type != Node.NodeType.EDGE:
                counter.steps += 1
                left_rule(node)
            next_node = node.left().other(node)
            if next_node.type == Node.NodeType.UPPER:
                upper_nodes.append(next_node)
            elif next_node.type == Node.NodeType.LOWER:
                lower_nodes.append(next_node)
        apply_successive_cancellation(upper_nodes)
        apply_successive_cancellation(lower_nodes)
        counter.parallel_steps += 1  # Right updates can be parallel here
        for node in node_list:
            if node.type != Node.NodeType.EDGE:
                counter.steps += 1
                right_rule(node)

    apply_successive_cancellation(graph.end_nodes)
    return counter
