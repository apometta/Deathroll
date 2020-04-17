"""This file, written by Andrew H. Pometta is the file for calculating and
exporting the probability that the first player is going to win a game of
Deathrolling given a starting roll of an n-sided die.  As opposed to
DeathrollSim.py and DRSimulate.py, this file does not actualy simulate a game
of deathrolling - rather, it mathematically calculates the exact probability
(or as close to the exact as your computer, OS and Python 3 can get).

The details of deriving the math formulas will be relegated to another
document.  Since our solution involves dynamic programming, we will
continually keep track of a summation as our calculations progress.

For finding the expected number of rolls per game, a nearly identical
approach is used, but a small difference in the formula.
"""

import numpy as np

# These global variables will be used to store a counters for our data as
# we progress

# this is the probability of the first player LOSING at the given index, where
# the index i is for a game with starting roll i + 1 (e.g. the 0th index is
# for games with a starting roll of 1, etc.).  The data for 1-sided die is
# input manually.
__p_l1_n = np.array([1], dtype=float)

# This keeps track of the sum of 1 - P(k) for all k in the range [2, k]
# INCLUSIVE.  Used for more efficiently calculating P(k+1).
__sig_p_w1_n = np.array([0], dtype=float)

# The below three arrays are for R(n), the average number of rolls per game.
# The relevant coefficient is called c_r(n), and the cache for R(n) will be
# stored in r_n

# We will, completely aribtrarily, declare R(1) to be 1.  You can also declare
# it so be 0.
__r_n = np.array([1], dtype=float)

# The sum R(k) for all k in the inclusive range [2, k].  Index 0 is for n = 1,
# which isn't in the range and thus it's 0.
__sig_r_n = np.array([0], dtype=float)

"""Custom exception class for ValueError."""


class DeathrollCalcValueError(ValueError):
    pass


"""Local private function for testing if a number is a positive integer."""


def __posint(arg, param="n"):
    try:
        arg = int(arg)
    except ValueError:
        raise DeathrollCalcValueError("Argument {} for {} cannot be cast "
                                      "as an integer".format(arg, param))
    if arg < 1:
        raise DeathrollCalcValueError(
            "Argument {} for {} is not positive".format(arg, param))
    return arg


"""Function for either fetching or, if not previously requested, calculating
the sum of all P_w1(k) in the range [2, k].  Note that P_w1(n) is just
1 - P_l1(n)."""


def __sig_p_w1(n):
    n = __posint(n)
    global __sig_p_w1_n
    try:
        return __sig_p_w1_n[n - 1]
    except IndexError:  # We haven't done this yet, so we calculate it
        # the recursive way
        total = __sig_p_w1(n - 1) + (1 - __p_l1(n))
        __sig_p_w1_n = np.append(__sig_p_w1_n, total)  # update cache
        return total


"""Function for either fetching or, if not previously requested, calculating
P_l1(n)."""


def __p_l1(n):
    n = __posint(n)
    global __p_l1_n
    try:
        return __p_l1_n[n - 1]
    except IndexError:  # calculate new P_l1(n)
        total = (2 + __sig_p_w1(n - 1)) / (n + 1)
        __p_l1_n = np.append(__p_l1_n, total)
        return total


"""Function for either fetching or, if not previously requested, caluclating
the sum of all R(k) in the range [2, k]."""


def __sig_r(n):
    n = __posint(n)
    global __sig_r_n
    try:
        return __sig_r_n[n - 1]
    except IndexError:
        total = __sig_r(n - 1) + __r(n)
        __sig_r_n = np.append(__sig_r_n, total)
        return total


"""Function for either fetching or, if not previously requested, calculating
R(n)."""


def __r(n):
    n = __posint(n)
    global __r_n
    try:
        return __r_n[n - 1]
    except IndexError:
        total = (n + __sig_r(n - 1)) / (n - 1)
        __r_n = np.append(__r_n, total)
        return total

"""User-accessible functions begin here.  They are mostly wrappers around the
above functions in one way or another."""

"""Function for getting P_w1(n) for a single value of n.  Raises a
DeathrollCalcValueError if n is not positive, or not castable as an integer."""


def p1_winrate(n):
    return 1 - __p_l1(n)


"""Function for getting P_w2(n) for a single value of n.  Raises a
DeathrollCalcValueError if n is not positive, or not castable as an integer."""


def p2_winrate(n):
    return __p_l1(n)


"""Function for getting a range of values for P, in the range [m, n) with a
difference between each integer by value step.  Default step of 1, or negative
1 if m > n.  Default m of 1 if only one argument supplied.  Raises a
DeathrollCalcValueError should any of the arguments not be castable as an
integer, or if either m or n are not positive."""


def p1_winrate_range(m, n=None, step=1):
    if n == None:
        m, n = 1, m
    if n != 0:
        # manually skip checking for 0, since it's allowed for n (not for m)
        n = __posint(n, "n")
    m = __posint(m, "m")
    try:
        step = int(step)
    except ValueError:
        raise DeathrollCalcValueError(
            "Argument {} for step not castable as an integer".format(step))
    __p_l1(max(m, n))  # ensure that all relevant values are calculated
    if m > n and step == 1:
        step = -1

    print(m, n, step)
    # 0 is a valid input for n, but we have to do it this way or else the
    # slicing doesn't work right
    data = __p_l1_n[m - 1: n - 1: step] if n > 0 else __p_l1_n[m - 1::step]
    return 1 - data


"""Same as p1_winrate_range, but for player 2's winrate."""


def p2_winrate_range(m, n=None, step=1):
    return 1 - p1_winrate_range(m, n, step)

"""Function for getting R(n) at a given value.   Returns
DeathrollCalcValueError if n is not positive, or castable as an integer."""


def avg_rolls(n):
    n = __posint(n)
    return __r(n)
