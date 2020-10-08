# hillclimbing.py
# By Sebastian Raaphorst, 2020.

from common import *

DEFAULT_UNIMPROVED_ITERATIONS = 5000

# Simple hillclimbing optimization to try to improve a schedule; it is unlikely that this will perform as well
# as the other techniques but we include it for completeness.

def hillclimbing(schedule: Schedule,
                 unimproved_iterations: int = DEFAULT_UNIMPROVED_ITERATIONS) -> Schedule:
    """
    Run the hillclimbing algorithm to try to optimize the schedule.
    :param schedule: the initial schedule to try to optimize
    :param unimproved_iterations: the maximum number of iterations without improvement in which to stop
    :return: the best schedule found so far.
    """
    current_evaluation = schedule.evaluate()
    current_unimproved_iterations = 0

    while current_unimproved_iterations < unimproved_iterations:
        current_unimproved_iterations += 1

        neighbor = schedule.generate_neighbour()
        evaluation = neighbor.evaluate()

        # We allow sideways moves, i.e. moves to the left and right without improvement, but this does not reset
        # the counter.
        if evaluation >= current_evaluation:
            schedule = neighbor
            if evaluation > current_evaluation:
                current_evaluation = evaluation
                current_unimproved_iterations = 0

    return schedule
