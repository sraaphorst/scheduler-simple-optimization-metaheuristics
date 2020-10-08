# common.py
# By Sebastian Raaphorst, 2020.

from typing import List
import random

time, score = int, float

class Observation:
    """
    An observation that comprises part of the schedule.
    """
    def __init__(self, name: str, length: int, timing_function):
        self.name = name
        self.length = length
        self.timing_function = timing_function

    def score_at(self, t: time) -> score:
        return sum(self.timing_function[t:t+self.length])

    def __str__(self):
        s = f'{self.name} {self.length}\n'
        s += f'{[i for i in self.timing_function]}\n\n'
        #return f'{self.name} {self.length} {[i for i in self.timing_function]}'
        return s


class Schedule:
    """
    A current schedule. We attempt to improve it by moving within the neighbourhood of the schedule.
    """
    def __init__(self, schedule: List[Observation]):
        self.schedule = schedule

    def evaluate(self) -> score:
        """
        Evaluate this schedule, which depends on the order of the observations scheduled in it.
        :return: the score of the schedule
        """
        curr_time = 0
        curr_score = 0
        for obs in self.schedule:
            curr_score += obs.score_at(curr_time)
            curr_time += obs.length
        return curr_score

    # def evaluate(self) -> score:
    #     """
    #     Evaluate this schedule, which depends on the order of the observations scheduled in it.
    #     :return: the score of the schedule
    #     """
    #     curr_time = 0
    #     curr_score = 0
    #     print(' '.join([schedule.name for schedule in self.schedule]))
    #     for obs in self.schedule:
    #         print(f"\tcurrtime={curr_time}, score={obs.score_at(curr_time)}")
    #         curr_score += obs.score_at(curr_time)
    #         curr_time += obs.length
    #     return curr_score

    def generate_neighbour(self):
        """
        To generate a neighbour of this schedule, we want to swap two observations at random.
        :return: a new schedule with the observations swapped
        """
        first, second = random.sample(range(len(self.schedule)), 2)
        new_schedule = self.schedule[:]
        new_schedule[first] = self.schedule[second]
        new_schedule[second] = self.schedule[first]
        return Schedule(new_schedule)

    def __str__(self):
        return ' '.join([str(i) for i in self.schedule])
