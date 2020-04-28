"""This file, written by Andrew H. Pometta, is the main file for the Deathroll
project this file is apart of.  It uses both DRSimulate.py and
DeathrollCalc.py to get data on the winrates and average roll counts in
Deathroll games of different starting conditions, as a guide for players that
wish to know the expected results of a Deathroll.  It uses this data to
generate graphs, to be used in a larger report."""

"""A temporary holder function to generate random data in the vague form of
what my actual data might be.  One of these is the experimental data, the
other is mathed."""

import numpy as np
import matplotlib.pyplot as plt
from math import log

"""Helper function to input random data for testing.  To be replaced with a
real function later."""


def __rdata():
    exp = np.array([1, 2 / 3, 0.62, 0.59])
    for i in range(96):
        diff_exp = exp[len(exp) - 1] - 0.5
        exp = np.append(exp, np.random.random() * diff_exp + 0.5)

    return exp

# initializing data sets - using random data until good data is in
x = range(1, 101)
p1_winrate_mc = 1 - __rdata()
p2_winrate_mc = 1 - p1_winrate_mc
p1_winrate_calc = 1 - __rdata()
p2_winrate_calc = 1 - p1_winrate_calc
roll_count = [0]
for i in range(2, 101):
    roll_count.append(log(i))
roll_count = np.array(roll_count)

# We get make two separate figures - one for the winrates, and one for the
# roll counts.  Might add a graph of the proportion between the two later.

# set up the figure for winrates
winrate_fig = plt.figure(1)
winrate_fig.canvas.set_window_title("Deathroll Win Probability")
winrates = plt.subplot(111, xlabel="/roll value",
                       ylabel="Probability of winning")
plt.plot(x, p1_winrate_mc, "x", color="darkred")
plt.plot(x, p2_winrate_mc, "x", color="darkblue")
plt.plot(x, p1_winrate_calc, "-", color="red")
plt.plot(x, p2_winrate_calc, "-", color="blue")
plt.show()
