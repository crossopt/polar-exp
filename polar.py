""" Module with basic helper functions for polarization. """


def polarize(probs):
    """ Helper function to compute polar code probabilities for channels with probabilities probs. """
    result = []
    for p in probs:
        result.append(p ** 2)
        result.append(2 * p - p ** 2)
    return result


def sort_gates(k, p):
    """
    Sorts the gates of a polar code by their probabilities descending.

    :param k: the power of the amount of gates being encoded.
    :param p: the probability of error for the polar code.
    :return: a list of 2 ** k tuples (i, prob[i]) sorted by prob[i].
    """
    probs = [p]
    for _ in range(k):
        probs = polarize(probs)
    indexed_probs = [(i, probs[i]) for i in range(len(probs))]
    indexed_probs.sort(key=lambda x: (-x[1], x[0]))
    return indexed_probs


def get_n_best_gates(k, p, n):
    """
    Returns a list of the n best gates with the highest probabilities.
    :param k: the power of the amount of gates being encoded.
    :param p: the probability of error for the polar code.
    :param: n: the amount of best gates to return.
    :return: A list of the n indexes of the gates with highest probabilities.
    """
    sorted_gates = sort_gates(k, p)
    return [gate[0] for gate in sorted_gates[:n]]
