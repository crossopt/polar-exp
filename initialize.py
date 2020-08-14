""" Module with basic functions for computing the initial state of the graph before belief propagation. """

import random
from polar import get_n_best_gates


def get_gates(k, p):
    """
    Returns the n = 2 ^ k gates, set to '?' for information bits and '*' for frozen bits.
    There should be pn frozen bits set for the encoding with error probability p.

    :param k: the power of the amount of gates being encoded.
    :param p: the probability of error for the polar code.
    :return: a list of length n with the frozen bits and the information bits differentiated.
    """
    unfrozen_amount = int(2 ** k * (1 - p))
    best_bits = get_n_best_gates(k, p, unfrozen_amount)
    gates = ['*'] * 2 ** k
    for bit in best_bits:
        gates[bit] = '?'
    return gates


def get_endpoints(k, p):
    """
    Randomly generate a possible output for the encoding of n = 2 ^ k bits with error probability p.
    The endpoint is set to '*' for a successfully passed bit and '?' for a lost one.

    :param k: the power of the amount of gates being encoded.
    :param p: the probability of error for the polar code.
    :return: a list of length n with the frozen bits and the information bits differentiated.
    """
    endpoints = ['?'] * 2 ** k
    passed_amount = int(2 ** k * (1 - p))
    successes = random.sample([i for i in range(2 ** k)], passed_amount)
    for success in successes:
        endpoints[success] = '*'
    return endpoints
