from graph import Graph, Node


def upper_rule(node):
    """ Applies the rule for upper nodes, returns True on success: two existing values set the third. """
    if node.type == Node.NodeType.UPPER:
        if node.get_neighbor_types() == ['*', '*', '?']:
            node.propagate()
            return True
    return False


def lower_rule(node):
    """ Applies the rule for lower nodes, returns True on success: one existing value sets all. """
    if node.type == Node.NodeType.LOWER:
        if '*' in node.get_neighbor_types() and '?' in node.get_neighbor_types():
            node.propagate()
            return True
    return False


def lazy_propagate(graph):
    """ Applies the propagation rules to all nodes in the graph while there was a single success. """
    was_success = True
    while was_success:
        was_success = False
        for node in graph.inner_nodes:
            was_success = was_success or upper_rule(node) or lower_rule(node)
