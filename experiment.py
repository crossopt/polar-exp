""" Runs the main experiment, ie various BP strategies, on generated inputs. """
from graph import Graph
from initialize import get_all_possible_configs
from propagate import default_stopping_condition,\
    flooding_propagate, scheduling_conventional_propagate, scheduling_round_trip_propagate
import matplotlib.pyplot as plt
from datetime import datetime


class ExperimentResult:
    """ Class to store the results of an experiment for all propagation methods. """
    def __init__(self, flooding_result=None, conventional_scheduling_result=None, round_trip_scheduling_result=None):
        self.flooding_result = flooding_result
        self.conventional_scheduling_result = conventional_scheduling_result
        self.round_trip_scheduling_result = round_trip_scheduling_result

    def print(self):
        """ Outputs the result in a human-readable format. """
        print('flooding: {:.2f}    conventional scheduling: {:.2f}  round trip scheduling: {:.2f}'.format(
            self.flooding_result, self.conventional_scheduling_result, self.round_trip_scheduling_result
        ))


def get_average_steps(method, graph_list, stopping_conditions):
    """ Returns the average (over all graphs in a given list) step amount a BP method performs until termination. """
    sum_steps = sum([method(graph.get_copy(), condition) for graph, condition in zip(graph_list, stopping_conditions)])
    return sum_steps / max(len(graph_list), 1)


def perform_average_computation_random(k, p, repeats):
    """ Returns an ExperimentResult containing the average step amount for running various BP methods.

    The propagation methods are run on repeats randomly generated graphs with k start nodes and probability of error p.
    The same graphs are used for all propagation methods. The propagation methods currently being run are
    flooding_propagate, scheduling_conventional_propagate and scheduling_round_trip_propagate.
    """
    graph_list = []
    condition_list = []
    for _ in range(repeats):
        graph = Graph(k, p)
        graph_list.append(graph)
        condition_list.append(default_stopping_condition(graph))
    return ExperimentResult(
        flooding_result=get_average_steps(flooding_propagate, graph_list, condition_list),
        conventional_scheduling_result=get_average_steps(scheduling_conventional_propagate, graph_list, condition_list),
        round_trip_scheduling_result=get_average_steps(scheduling_round_trip_propagate, graph_list, condition_list)
    )


def perform_average_computation_all(k, p):
    """ Returns an ExperimentResult containing the average step amount for running various BP methods.

    The propagation methods are run on all possible generated graphs with k start nodes and probability of error p.
    The propagation methods currently being run are
    flooding_propagate, scheduling_conventional_propagate and scheduling_round_trip_propagate.
    """
    graph_list = []
    condition_list = []
    for end_node_config in get_all_possible_configs(k, p):
        graph = Graph(k, p)
        graph.update_end_nodes(end_node_config)
        graph_list.append(graph)
        condition_list.append(default_stopping_condition(graph))
    return ExperimentResult(
        flooding_result=get_average_steps(flooding_propagate, graph_list, condition_list),
        conventional_scheduling_result=get_average_steps(scheduling_conventional_propagate, graph_list, condition_list),
        round_trip_scheduling_result=get_average_steps(scheduling_round_trip_propagate, graph_list, condition_list)
    )


def plot_graph(name, probs, results):
    plt.plot(probs, [result.flooding_result for result in results], 'r', label='Flooding')
    plt.plot(probs, [result.conventional_scheduling_result for result in results], 'b', label='Conventional scheduling')
    plt.plot(probs, [result.round_trip_scheduling_result for result in results], 'g', label='Round-trip scheduling')

    plt.title(name)
    plt.xlabel('Error probability')
    plt.ylabel('Average step amount')
    plt.legend()

    plt.savefig('results/graph_{}.png'.format(datetime.now()))
    plt.clf()
    print(datetime.now())  # A rough idea of the execution time.


def print_average_result_all(k, prob_step, dbg=False):
    """ Outputs the average step amount dependent on various probabilities taken with a fixed step. """
    results = []
    probs = []
    for prob in range(prob_step):
        probs.append(prob / prob_step)
        results.append(perform_average_computation_all(k, prob / prob_step))
        if dbg:
            results[-1].print()
    plot_graph('Average decoding step amount for all encodings of {} bits'.format(k), probs, results)


def print_average_result_random(k, prob_step, repeats, dbg=False):
    """ Outputs the average step amount dependent on various probabilities taken with a fixed step. """
    results = []
    probs = []
    for prob in range(prob_step):
        probs.append(prob / prob_step)
        results.append(perform_average_computation_random(k, prob / prob_step, repeats))
        if dbg:
            results[-1].print()
    plot_graph('Average decoding step amount for {} random encodings of {} bits'.format(repeats, k), probs, results)


if __name__ == '__main__':
    print(datetime.now())
    print_average_result_all(3, 16)
    print_average_result_all(4, 16)

    print_average_result_random(5, 16, repeats=100)
    print_average_result_random(6, 16, repeats=100)