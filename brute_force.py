# brute_force.py
# By Sebastian Raaphorst, 2020.

from common import *
from itertools import permutations

# A brute force algorithm that tries all permutations of a schedule to determine its best ordering over a night.

def brute_force_search(schedule: Schedule) -> Schedule:
    """
    Try every permutation of the schedules in schedule and check their
    score. Return the one with the highest score.
    :param schedule: the schedule over which to search
    :return: the schedule with the highest score
    """

    # Get the max element amongst all permutations of the schedule.
    best_tuple = sorted(permutations(schedule.schedule),
                        key=lambda x: Schedule(x).evaluate())[-1]
    return Schedule(list(best_tuple))
