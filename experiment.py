""" Runs the main experiment, ie various BP strategies, on generated inputs. """
from graph import Graph
from initialize import get_all_possible_configs, get_p_list
from propagate import Counter, default_stopping_condition, successive_cancellation_propagate,\
    naive_propagate, flooding_propagate, scheduling_conventional_propagate, scheduling_round_trip_propagate
import matplotlib.pyplot as plt
from datetime import datetime


class ExperimentResult:
    """ Class to store the results of an experiment for all propagation methods. """
    def __init__(self,
                 naive_result=None,
                 flooding_result=None,
                 conventional_scheduling_result=None,
                 round_trip_scheduling_result=None,
                 successive_cancellation_result=None):
        self.naive_result = naive_result
        self.flooding_result = flooding_result
        self.conventional_scheduling_result = conventional_scheduling_result
        self.round_trip_scheduling_result = round_trip_scheduling_result
        self.successive_cancellation_result = successive_cancellation_result

    def print(self):
        """ Outputs the result in a human-readable format. """
        print('''naive: {:.2f}/{:.2f}  flooding: {:.2f}/{:.2f}  conventional scheduling: {:.2f}/{:.2f}'''
              '''   round trip scheduling: {:.2f}/{:.2f}  successive cancellation {:.2f}/{:.2f}'''.format(
                  self.naive_result.steps, self.naive_result.parallel_steps,
                  self.flooding_result.steps, self.flooding_result.parallel_steps,
                  self.conventional_scheduling_result.steps, self.conventional_scheduling_result.parallel_steps,
                  self.round_trip_scheduling_result.steps, self.round_trip_scheduling_result.parallel_steps,
                  self.successive_cancellation_result.steps, self.successive_cancellation_result.parallel_steps,
              ))


def get_average_steps(method, graph_list, stopping_conditions):
    """ Returns the average (over all graphs in a given list) step amount a BP method performs until termination. """
    counter = Counter()
    results = [method(graph.get_copy(), condition) for graph, condition in zip(graph_list, stopping_conditions)]
    counter.steps = sum([result.steps for result in results]) / max(len(graph_list), 1)
    counter.parallel_steps = sum([result.parallel_steps for result in results]) / max(len(graph_list), 1)
    return counter


def perform_average_computation_random(k, p, repeats):
    """ Returns an ExperimentResult containing the average step amount for running various BP methods.

    The propagation methods are run on repeats randomly generated graphs with k start nodes and probability of error p.
    The same graphs are used for all propagation methods. The propagation methods currently being run are
    naive_propagate, scheduling_conventional_propagate and scheduling_round_trip_propagate.
    """
    graph_list = []
    condition_list = []
    for _ in range(repeats):
        graph = Graph(k, p)
        graph_list.append(graph)
        condition_list.append(default_stopping_condition(graph))
    return ExperimentResult(
        naive_result=get_average_steps(naive_propagate, graph_list, condition_list),
        flooding_result=get_average_steps(flooding_propagate, graph_list, condition_list),
        conventional_scheduling_result=get_average_steps(scheduling_conventional_propagate, graph_list, condition_list),
        round_trip_scheduling_result=get_average_steps(scheduling_round_trip_propagate, graph_list, condition_list),
        successive_cancellation_result=get_average_steps(successive_cancellation_propagate, graph_list, condition_list),
    )


def perform_average_computation_all(k, p):
    """ Returns an ExperimentResult containing the average step amount for running various BP methods.

    The propagation methods are run on all possible generated graphs with k start nodes and probability of error p.
    The propagation methods currently being run are
    naive_propagate, scheduling_conventional_propagate and scheduling_round_trip_propagate.
    """
    graph_list = []
    condition_list = []
    for end_node_config in get_all_possible_configs(k, p):
        graph = Graph(k, p)
        graph.update_end_nodes(end_node_config)
        graph_list.append(graph)
        condition_list.append(default_stopping_condition(graph))
    return ExperimentResult(
        naive_result=get_average_steps(naive_propagate, graph_list, condition_list),
        flooding_result=get_average_steps(flooding_propagate, graph_list, condition_list),
        conventional_scheduling_result=get_average_steps(scheduling_conventional_propagate, graph_list, condition_list),
        round_trip_scheduling_result=get_average_steps(scheduling_round_trip_propagate, graph_list, condition_list),
        successive_cancellation_result=get_average_steps(successive_cancellation_propagate, graph_list, condition_list),
    )


def plot_graph(name, k, results):
    passed_amounts = [i for i in range(2 ** k + 1)]
    fig, (step, parallel_step) = plt.subplots(2, 1)
    step.plot(passed_amounts, [result.naive_result.steps for result in results], 'r', label='Naive propagation')
    step.plot(passed_amounts, [result.flooding_result.steps for result in results], 'k', label='Flooding propagation')
    step.plot(passed_amounts, [result.conventional_scheduling_result.steps for result in results], 'b',
             label='Conventional scheduling')
    step.plot(passed_amounts, [result.round_trip_scheduling_result.steps for result in results], 'g',
             label='Round-trip scheduling')
    step.plot(passed_amounts, [result.successive_cancellation_result.steps for result in results], 'y',
             label='Successive cancellation')

    fig.suptitle(name)
    step.set(ylabel='Average number of\noperations')

    parallel_step.plot(passed_amounts, [result.naive_result.parallel_steps for result in results], 'r',
                       label='Naive propagation')
    parallel_step.plot(passed_amounts, [result.flooding_result.parallel_steps for result in results], 'k',
             label='Flooding propagation')
    parallel_step.plot(passed_amounts, [result.conventional_scheduling_result.parallel_steps for result in results], 'b',
             label='Conventional scheduling')
    parallel_step.plot(passed_amounts, [result.round_trip_scheduling_result.parallel_steps for result in results], 'g',
             label='Round-trip scheduling')
    parallel_step.plot(passed_amounts, [result.successive_cancellation_result.parallel_steps for result in results], 'y',
             label='Successive cancellation')

    parallel_step.set(xlabel='Number of non-frozen (informative) bits', ylabel='Average number of\nparallel steps')

    lines, labels = fig.axes[-1].get_legend_handles_labels()
    legend = fig.legend(lines, labels, bbox_to_anchor=(1.0, 1.0), loc='upper left')

    plt.savefig('results/graph_{}.png'.format(datetime.now()),bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.clf()
    print(datetime.now())  # A rough idea of the execution time.


def print_average_result_all(k, dbg=False):
    """ Outputs the average step amount dependent on probabilities that generate different amounts of frozen bits. """
    results = []
    probs = get_p_list(k)
    for prob in probs:
        results.append(perform_average_computation_all(k, prob))
        if dbg:
            results[-1].print()
    plot_graph('Polar encoding with block size {}'.format(2 ** k), k, results)


def print_average_result_random(k, repeats, dbg=False):
    """ Outputs the average step amount dependent on probabilities that generate different amounts of frozen bits. """
    results = []
    probs = get_p_list(k)
    for prob in probs:
        results.append(perform_average_computation_random(k, prob, repeats))
        if dbg:
            results[-1].print()
    plot_graph('Polar encoding with block size {}, {} runs'.format(2 ** k, repeats), k, results)


if __name__ == '__main__':
    print(datetime.now())
    print_average_result_all(3)
    print_average_result_random(5, repeats=100)
