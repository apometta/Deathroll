"""This file, written by Andrew H. Pometta is the file for calculating and 
exporting the probability that the first player is going to win a game of 
Deathrolling given a starting roll of an n-sided die.  As opposed to 
DeathrollSim.py and DRSimulate.py, this file does not actualy simulate a game 
of deathrolling - rather, it mathematically calculates the exact probability 
(or as close to the exact as your computer, OS and Python 3 can get).

The details of deriving the math formula will be relegated to another 
document.  The math formula requires the use of dynamic programming, so 
the exported data will necessarily be a range of data, containing the 
probability of the first player winning for all n in the range [1, N] where 
N is the user's inputted maximum n.

For reference, the formula for all positive integer n > 1 is:

P(n) = c_n(n/[(n^2)-1]) where P(1) = 1 and 
c(n) = 1 + sum[i=2 to n-1](1/i(sigma[j=2 to i](P(j)))) + 
      1/n(sigma[j=2 to n-1](P(j)))
Alternatively, c can be defined recursively as such:
c(n) = c(n-1) + (1/(n-1))sigma[j=2 to n-1](P(j)) + (1/n)P(n-1) where c(2) = 1


Sorry if my notation sucks.

The strategy to calculate the values effeciently quite obviously utilizes 
dynamic programming, seeing as P(n) is a recursive piecewise function, to 
which P(k) for any k requires knowledge of all P(l) for l in [1, k-1].  We 
use one list to keep track of the running data for P(n) for quick reference, 
and another few variables to keep track of c(n) as n progresses.
"""

import numpy as np

# These global variables will be used to store a counters for our data as
# we progress

# this is the probability of the first player LOSING at the given index, where
# the index i is for a game with starting roll i + 1 (e.g. the 0th index is
# for games with a starting roll of 1, etc.).  The data for 1-sided die is
# input manually.
p_n = np.array([1], dtype=float)

# this is the list to keep track of c(n) as n progresses, in a similar manner
# to p_n.  Technically by the "proper" notation c(1) and c(2) should be 1,
# but c(1) being 0.5 is necessary to make the recursion work.  Nonetheless,
# we can define it properly and just never reference the 0th index
c_n = np.array([1, 1], dtype=float)

# One frequently used note is sum from i=2 to n - 1 of P(i).  It is faster to
# keep a running tally of this as we progress rather than an operation that
# iterates through the p_n array constantly.
sig_p_n = 0.0
