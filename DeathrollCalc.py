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
c_n = 1 + sum[i=2 to n-1](1/i(sigma[j=2 to i](P(j)))) + 
      1/n(sigma[j=2 to n-1](P(j)))

Sorry if my notation sucks.
"""
