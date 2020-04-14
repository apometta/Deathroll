"""This file, written by Andrew H. Pometta is the file for calculating and
exporting the probability that the first player is going to win a game of
Deathrolling given a starting roll of an n-sided die.  As opposed to
DeathrollSim.py and DRSimulate.py, this file does not actualy simulate a game
of deathrolling - rather, it mathematically calculates the exact probability
(or as close to the exact as your computer, OS and Python 3 can get).

The details of deriving the math formulas will be relegated to another
document.

The strategy to calculate the values effeciently quite obviously utilizes
dynamic programming, seeing as P_l1(n) is a recursive piecewise function, to
which P_l1(k) for any k requires knowledge of all P_l1(m) for m in [1, k-1].  
We use one list to keep track of the running data for P_l1(n) for quick 
reference, and another few variables to keep track of c_p(n) as n progresses.

For finding the expected number of rolls per game, a nearly identical 
approach is used, but a small difference in the formula has relatively 
important applications that make it worth segmenting the two tasks as separate 
areas.
"""

import numpy as np

# These global variables will be used to store a counters for our data as
# we progress

# this is the probability of the first player LOSING at the given index, where
# the index i is for a game with starting roll i + 1 (e.g. the 0th index is
# for games with a starting roll of 1, etc.).  The data for 1-sided die is
# input manually.
__p_l1_n = np.array([1], dtype=float)

# this is the list to keep track of c_p(n) as n progresses, in a similar manner
# to p_l1_n.  Manually inputting 2 makes our recursive formula for c_p(n)
# work as expected
__c_p_n = np.array([1, 1], dtype=float)

# This array represents, for each index i, the sum off all P_l1(k) for which k
# is in the range [2, k] INCLUSIVE.  For efficient calculating of c_p(n)
__sig_p_l1_n = np.array([0], dtype=float)

# The below three arrays are for R(n), the average number of rolls per game.
# The relevant coefficient is called c_r(n), and the cache for R(n) will be
# stored in r_n

# We will, completely aribtrarily, declare R(1) to be 1.  You can also declare
# it so be 0.
__r_n = np.array([1], dtype=float)

# c_r(1) is less arbitrary, as it is technically correct.  c_r(2) is manually
# input to ensure our recursive formula works, similar to c_p_n
__c_r_n = np.array([1, 1], dtype=float)

__sig_r_n = np.array([0], dtype=float)

"""Custom exception class for ValueError."""


class DeathrollCalcValueError(ValueError):
    pass


"""Local private function for testing if a number is a positive integer."""


def __posint(arg):
    try:
        arg = int(arg)
    except ValueError:
        raise DeathrollCalcValueError("Argument {} for n cannot be cast "
                                      "as an integer".format(arg))
    if arg < 1:
        raise DeathrollCalcValueError(
            "Argument {} for n is not positive".format(arg))
    return arg


"""Function for either fetching or, if not previously requested, calculating 
the sum of all P_l1(k) in the range [2, k]."""


def __sig_p_l1(n):
    n = __posint(n)
    global __sig_p_l1_n
    try:
        return __sig_p_l1_n[n - 1]
    except IndexError:  # We haven't done this yet, so we calculate it
        # the recursive way
        total = __sig_p_l1(n - 1) + __p_l1(n)
        __sig_p_l1_n = np.append(__sig_p_l1_n, total)  # update cache
        return total


"""Function for either fetching or, if not previously requested, calculating 
P_l1(n)."""


def __p_l1(n):
    n = __posint(n)
    global __p_l1_n
    try:
        return __p_l1_n[n - 1]
    except IndexError:  # calculate new P_l1(n)
        total = __c_p(n) * (n / ((n**2) - 1))
        __p_l1_n = np.append(__p_l1_n, total)
        return total


"""Function for either fetching or, if not previously requested, calculating 
c_p(n)."""


def __c_p(n):
    n = __posint(n)
    global __c_p_n, __sig_p_l1_n
    try:
        return __c_p_n[n - 1]
    except IndexError:
        # the recursive way - ONLY works when n >= 3
        assert n >= 3
        mid = ((1 / (n - 1)) * __p_l1(n - 1))
        last = ((1 / n) * __sig_p_l1(n - 1))
        total = __c_p(n - 1) + mid + last
        __c_p_n = np.append(__c_p_n, total)
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
        total = __c_r(n) * (n / (n - 1))
        __r_n = np.append(__r_n, total)
        return total


"""Function for either fetching or, if not previously requested, caluclating 
c_r(n)."""


def __c_r(n):
    n = __posint(n)
    global __c_r_n, __sig_r_n
    try:
        return __c_r_n[n - 1]
    # recursive definition of c_r(n) based off of c_r(n - 1)
    except IndexError:  # is not necessary
        total = 1 + ((1 / n) * __sig_r(n - 1))
        __c_r_n = np.append(__c_r_n, total)
        return total
