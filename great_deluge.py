# great_deluge.py
# By Sebastian Raaphorst, 2020.

from common import *

DEFAULT_RAIN_SPEED = 1
DEFAULT_INITIAL_WATER_LEVEL = 100
DEFAULT_UNIMPROVED_ITERATIONS = 1000


# We select Dueck's great deluge algorithm as it is more flexible than hill climbing and more easily tuned than
# simulated annealing, and tends to yield better results. The goal is to take a schedule and rearrange it to
# derive an improvement in the schedule.

def deluge_solver(schedule: Schedule,
                  rain_speed = DEFAULT_RAIN_SPEED,
                  water_level = DEFAULT_INITIAL_WATER_LEVEL,
                  unimproved_iterations = DEFAULT_UNIMPROVED_ITERATIONS) -> Schedule:
    """
    Run the deluge solver to try to optimize the schedule.
    :param schedule: the initial schedule to try to optimize
    :param rain_speed: the speed at which the rain falls when improvement is seen
    :param water_level: the current water level, which allows worse moves to avoid local maxima
    :param unimproved_iterations: the maximum number of iterations without improvement in which to stop
    :return: the best schedule found so far.
    """
    best_schedule = schedule
    best_evaluation = schedule.evaluate()

    current_unimproved_iterations = 0

    while current_unimproved_iterations < unimproved_iterations:
        current_unimproved_iterations += 1

        neighbour = schedule.generate_neighbour()
        evaluation = neighbour.evaluate()

        if evaluation > water_level:
            schedule = neighbour
            water_level += rain_speed

            if evaluation > best_evaluation:
                best_schedule, best_evaluation = schedule, evaluation
                current_unimproved_iterations = 0

    return best_schedule
