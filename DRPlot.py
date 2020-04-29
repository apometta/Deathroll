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
import DeathrollCalc as drc
import DRSimulate as drs

"""Helper function to input random data for testing.  To be replaced with a
real function later."""


def __rdata():
    exp = np.array([1, 2 / 3, 0.62, 0.59])
    for i in range(96):
        diff_exp = exp[len(exp) - 1] - 0.5
        exp = np.append(exp, np.random.random() * diff_exp + 0.5)

    return exp

# initializing data sets
mc_range = [2, 5, 10, 25, 50, 100]  # domain for monte carlo
calc_range = range(1, 101)

mc_data = drs.deathroll_mc(mc_range, 10_000)
p1_winrate_mc = mc_data[:, 0]
p2_winrate_mc = 1 - p1_winrate_mc
avg_rolls_mc = mc_data[:, 1]

p1_winrate_calc = drc.p1_winrate(calc_range)
p2_winrate_calc = drc.p2_winrate(calc_range)
avg_rolls_calc = drc.avg_rolls(calc_range)

# We get make two separate figures - one for the winrates, and one for the
# roll counts.  Might add a graph of the proportion between the two later.

# set up the figure for winrates
winrate_fig = plt.figure(1, facecolor="#CCCCCC")
winrate_fig.canvas.set_window_title("Deathroll Win Probability")
winrates = plt.subplot(111, facecolor="#EEEEEE", xlabel="/roll value",
                       ylabel="Probability of winning")
plt.plot(calc_range, p1_winrate_calc, "-", color="red",  alpha=0.5,
         label="Player 1 Winrate (Exact Formula)")
plt.plot(calc_range, p2_winrate_calc, "-", color="blue",  alpha=0.5,
         label="Player 2 Winrate (Exact Formula)")
plt.plot(mc_range, p1_winrate_mc, "x", color="darkred", alpha=0.5,
         label="Player 1 Winrate (Monte Carlo, UPDATE samples)")
plt.plot(mc_range, p2_winrate_mc, "x", color="darkblue", alpha=0.5,
         label="Player 2 Winrate (Monte Carlo, UPDATE samples)")
winrates.legend(loc="lower right")

# And the figure for rolls
rolls_fig = plt.figure(2, facecolor="#CCCCCC")
rolls_fig.canvas.set_window_title("Average Rolls per Deathroll")
rolls = plt.subplot(111, facecolor="#EEEEEE", xlabel="/roll value",
                    ylabel="Average Rolls per Game")
plt.plot(calc_range, avg_rolls_calc, "-", color="green", alpha=1,
         label="Average Rolls per Game (Exact Formula)")
plt.plot(mc_range, avg_rolls_mc, "x", color="darkgreen", alpha=1,
         label="Average Rolls per Game (Monte Carlo, UPDATE samples")
rolls.legend(loc="lower right")
plt.show()
