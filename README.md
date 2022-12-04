# Simple Optimization Metaheuristics

This is a collection of simple optimization metaheuristics, implemented as a part of a trade study on automated scheduler algorithms for Gemini Observatory.

The idea is that given:
1. a schedule of observations `O` for a night; and
2. functions `f_o: T -> ℝ_{≥0}` for each `o ∈ O`, i.e. a function for each observation that assigns
it a nonnegative score based on when it is scheduled;
3. a time-based ordering of the observations `[o_0, o_1, o_2, ...]` corresponding to times `[t_0, t_1, t_2, ...]`; and
3. a _score_ `S = sum_(f_o_i(t_i))`

we can use optimization metaheuristics to try to optimize the schedule up to the order of the
observations.

We provide several different techniques for doing so, along with a brute force algorithm (which tries all permutations
of the observations and finds the one that scores the highest for comparison).
