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
