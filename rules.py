""" Module for the rules by which the encoding graph propagates. """
from graph import Node


def upper_rule(node, apply_propagate=True, _was_extra_propagation=False):
    """ Applies the rule for upper nodes, returns True on success: two existing values set the third. """
    if node.type == Node.NodeType.UPPER:
        success_no_extra = node.get_neighbor_types() == ['*', '*', '?']
        success_extra = node.get_neighbor_types() == ['*', '?', '?']
        if ((not _was_extra_propagation) and success_no_extra) or (_was_extra_propagation and success_extra):
            if apply_propagate:
                node.propagate()
            return True
    return False


def lower_rule(node, apply_propagate=True, _was_extra_propagation=False):
    """ Applies the rule for lower nodes, returns True on success: one existing value sets all. """
    if node.type == Node.NodeType.LOWER:
        success_no_extra = node.get_neighbor_types() == ['*', '?', '?'] or node.get_neighbor_types() == ['*', '*', '?']
        success_extra = node.get_neighbor_types() == ['?', '?', '?'] or node.get_neighbor_types() == ['*', '?', '?']
        if ((not _was_extra_propagation) and success_no_extra) or (_was_extra_propagation and success_extra):
            if apply_propagate:
                node.propagate()
            return True
    return False


def relevant_rule(node, apply_propagate=True, _was_extra_propagation=False):
    """ Applies the relevant rule for a node, depending on its type. Returns True on success. """
    if node.type == Node.NodeType.EDGE:
        return False
    rule = lower_rule if node.type == Node.NodeType.LOWER else upper_rule if node.type == Node.NodeType.UPPER else None
    return rule(node, apply_propagate=apply_propagate, _was_extra_propagation=_was_extra_propagation)


def vertical_rule(node, apply_propagate=True):
    """ Explicitly applies the vertical rule for the edge's other node.  This is implicitly done in the article.

    If this application is not counted as a step, that would be equivalent to implicitly applying the propagation on
    vertical edges. This is currently possible via counting only left- and right- rule applications for non-scheduling
    propagation as well.
    """
    vertical_value = node.vertical().value
    return relevant_rule(node.vertical().other(node), apply_propagate=apply_propagate) and vertical_value == '?'


def left_rule(node, apply_propagate=True):
    """ The article's L-rule.  Applies the rule for a node to propagate its left edge. Returns True on success. """
    if node.type == Node.NodeType.EDGE:
        return False
    if node.left().value == '?':
        was_propagation = vertical_rule(node, apply_propagate=apply_propagate) and (not apply_propagate)
        return relevant_rule(node, apply_propagate=apply_propagate, _was_extra_propagation=was_propagation)
    return False


def right_rule(node, apply_propagate=True):
    """ The article's R-rule. Applies the rule for a node to propagate its right edge. Returns True on success. """
    if node.type == Node.NodeType.EDGE:
        return False
    if node.right().value == '?':
        was_propagation = vertical_rule(node, apply_propagate=apply_propagate) and (not apply_propagate)
        return relevant_rule(node, apply_propagate=apply_propagate, _was_extra_propagation=was_propagation)
    return False


def any_rule(node, apply_propagate=True):
    """ Applies either L-rule or R-rule. Returns True on success. """
    return left_rule(node, apply_propagate) or right_rule(node, apply_propagate)


def relevant_rule_list(node):
    """ Applies the relevant rule for a node, depending on its type. Returns a list of nodes that the propagation has
    changed enough that they may be interesting with the rules to apply to them. """
    edge_states = [edge.value for edge in node.edges]
    relevant_rule(node, apply_propagate=True, _was_extra_propagation=False)
    node_list = []
    for edge, old_state in zip(node.edges, edge_states):
        if edge.value != old_state:
            node_list.append(edge.other(node))
    return node_list


def vertical_rule_list(node):
    """ Explicitly applies the vertical rule for the edge's other node. Returns a list of nodes that the propagation
    has changed enough that they may be interesting.
    """
    return relevant_rule_list(node.vertical().other(node))


def left_rule_list(node):
    """ The article's L-rule.  Applies the rule for a node to propagate its left edge. Returns a list of nodes that the
    propagation has changed enough that they may be interesting.
    """
    if node.type == Node.NodeType.EDGE or node.left().value != '?':
        return []
    else:
        v_list = vertical_rule_list(node)
        node_list = relevant_rule_list(node)
        if v_list and node.vertical().other(node) in node_list:
            pass
            # Vertical propagation happened, the vertical edge's other node is not interesting.
            node_list.remove(node.vertical().other(node))
        if node_list and node in v_list:
            pass
            # Node propagation happened, the node itself is not interesting any more.
            v_list.remove(node)
        return v_list + node_list


def right_rule_list(node):
    """ The article's R-rule.  Applies the rule for a node to propagate its right edge. Returns a list of nodes that the
    propagation has changed enough that they may be interesting.
    """
    if node.type == Node.NodeType.EDGE or node.right().value != '?':
        return []
    else:
        v_list = vertical_rule_list(node)
        node_list = relevant_rule_list(node)
        if v_list and node.vertical().other(node) in node_list:
            pass
            # Vertical propagation happened, the vertical edge's other node is not interesting.
            node_list.remove(node.vertical().other(node))
        if node_list and node in v_list:
            pass
            # Node propagation happened, the node itself is not interesting any more.
            v_list.remove(node)
        return v_list + node_list
