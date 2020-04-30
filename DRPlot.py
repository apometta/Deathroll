"""This file, written by Andrew H. Pometta, is the main file for the Deathroll
project this file is apart of.  It uses both DRSimulate.py and
DeathrollCalc.py to get data on the winrates and average roll counts in
Deathroll games of different starting conditions, as a guide for players that
wish to know the expected results of a Deathroll.  It uses this data to
generate graphs, to be used in a larger report."""

# SETTINGS - change the properties of the graphs here

import math
import numpy as np
import matplotlib.pyplot as plt
import DeathrollCalc as drc
import DRSimulate as drs


# annotate certain points of the graph.  If any other option is changed from
# the default for the winrates figure, turn this off, as it is dependent on
# other options being set to the default
wr_annotate = True
# use logarithmic x scale for the winrates
wr_logx = True
# the base of the log for the x scale
wr_logbase = 10
# use percentages for the y axis for the winrates
wr_pery = True
# alpha level for the main winrate lines
wr_alpha = 0.5
# alpha level from 1 to 2 for winrates.  Set to 0 to disable or to wr_alpha
# to match main data
wr_first_alpha = wr_alpha / 8
# use logarithmic x scale for the rolls
rolls_logx = False
# if the above option is true, this controls the base of the log for the scale
rolls_logbase = math.e
# alpha level for the rolls
rolls_alpha = 0.5
# alpha level for the first line of the rolls
rolls_first_alpha = rolls_alpha / 8
# whether or not to graph ln along with the rolls
rolls_log = False
# maximum y for the rolls graph - care when using this with rolls_log
# set to 0 for automatic calculation
rolls_ymax = 0
# maximum value to calculate for rolls and winrate
calc_max = 1000
# domain for monte carlo
mc_range = [2, 5, 10, 25, 50, 100, 500, 1000]
# sample size for the Monte Carlo simuation
mc_samples = 10_000

# initializing data sets
calc_range = range(1, calc_max + 1)
mc_data = drs.deathroll_mc(mc_range, mc_samples)
p1_winrate_mc = mc_data[:, 0]
p2_winrate_mc = 1 - p1_winrate_mc
avg_rolls_mc = mc_data[:, 1]

p1_winrate_calc = drc.p1_winrate(calc_range)
# Since DeathrollCalc saves the values stored thus far, this isn't double the
# time spent
p2_winrate_calc = drc.p2_winrate(calc_range)
avg_rolls_calc = drc.avg_rolls(calc_range)
if rolls_log:  # the range of log, from 1 to 1000
    log_range = np.fromfunction(np.vectorize(lambda n: math.log(n + 1)),
                                (calc_max,))

# We get make two separate figures - one for the winrates, and one for the
# roll counts.  Might add a graph of the proportion between the two later.

# set up the figure for winrates
winrate_fig = plt.figure(1, facecolor="#CCCCCC", figsize=(16, 8), dpi=110)
winrate_fig.canvas.set_window_title("Deathroll Win Probability")
# setting the properties of the axes
winrates = plt.subplot(111, facecolor="#EEEEEE", xlabel="/roll Value",
                       ylabel="Probability of winning")
# set the x axis as a log scale if necessary, but keep the tick values scalars
if wr_logx:
    from matplotlib.ticker import ScalarFormatter
    plt.xscale("log", basex=wr_logbase)
    winrates.xaxis.set_major_formatter(ScalarFormatter())
# set percentages for y axis if necessary
if wr_pery:
    from matplotlib.ticker import PercentFormatter
    winrates.yaxis.set_major_formatter(PercentFormatter(xmax=1))

# plotting the main data.  We only use the data for 2 and after for the main
# alpha value, and separately plot the first 2 points
plt.plot(calc_range[1:], p1_winrate_calc[1:], "-", color="red",
         alpha=wr_alpha, label="Player 1 Winrate (Exact Formula)")
plt.plot(calc_range[1:], p2_winrate_calc[1:], "-", color="blue",
         alpha=wr_alpha, label="Player 2 Winrate (Exact Formula)")
plt.plot(mc_range, p1_winrate_mc, "x", color="darkred", alpha=wr_alpha,
         label="Player 1 Winrate (Monte Carlo)")
plt.plot(mc_range, p2_winrate_mc, "x", color="darkblue", alpha=wr_alpha,
         label="Player 2 Winrate (Monte Carlo)")
winrates.legend(loc="lower right")
# plotting these later lets us draw the first line with a higher alpha, as
# well as omit it from the legend
plt.plot(calc_range[:2], p1_winrate_calc[:2], "-", color="red",
         alpha=wr_first_alpha)
plt.plot(calc_range[:2], p2_winrate_calc[:2], "-", color="blue",
         alpha=wr_first_alpha)
# perform annotations on the wr graph.
if wr_annotate:
    arrow = dict(arrowstyle='-')
    ann_2 = "For a 2 sided-die, the smallest\n possible deathroll, "\
        "the current\nroller only has a 33.3% chance \nof winning."
    # I won't lie, I only found the xytext location through guess and test
    plt.annotate(ann_2, xy=(2, p1_winrate_calc[1]), xytext=(1.4, 0),
                 arrowprops=arrow, fontsize="small",  wrap=True)
    ann_5 = "When the die has 5 sides, the \ngap in winrate has already "\
        "substantially\ndecreased: the current roller has \na 46.6% chance "\
        "at winning."
    pass
    plt.annotate(ann_5, xy=(5, p1_winrate_calc[4]), xytext=(3, 0.175),
                 arrowprops=arrow, fontsize="small")
    ann_10 = "By /roll 10, this probability \nrises barely above 49%."
    plt.annotate(ann_10, xy=(10, p1_winrate_calc[9]), xytext=(6, 0.37),
                 arrowprops=arrow, fontsize="small")
    ann_25 = "At /roll 25, the difference in \nwinrates is less than 0.5%."
    plt.annotate(ann_25, xy=(25, p2_winrate_calc[24]), xytext=(14, 0.55),
                 arrowprops=arrow, fontsize="small")
    ann_100 = "For a deathroll of 100, \nthe difference in winrates is "\
        "\nless than 0.02%."
    pass
    plt.annotate(ann_100, xy=(100, p1_winrate_calc[99]), xytext=(65, 0.40),
                 arrowprops=arrow, fontsize="small")
    ann_1000 = "At /roll 1000, the gap \nbetween winrates is \ninfinitesimal."
    plt.annotate(ann_1000, xy=(1000, p2_winrate_calc[999]),
                 xytext=(625, 0.55), arrowprops=arrow, fontsize="small")

"""
    # And the figure for rolls
rolls_fig = plt.figure(2, facecolor="#CCCCCC")
rolls_fig.canvas.set_window_title("Average Rolls per Deathroll")
# the axes for rolls is a bit simpler
rolls = plt.subplot(111, facecolor="#EEEEEE", xlabel="/roll Value",
                    ylabel="Average Rolls per Game")
# set x axis scale
if rolls_logx:
    # Since the graph is to be viewed by the less mathematically inclined,
    # scientific notation should be eschewed
    from matplotlib.ticker import ScalarFormatter
    plt.xscale("log", basex=rolls_logbase)
    rolls.xaxis.set_major_formatter(ScalarFormatter())
# set y maximum
if rolls_ymax > 0:
    plt.ylim(0, rolls_ymax)

# plot the roll data
plt.plot(calc_range[1:], avg_rolls_calc[1:], "-", color="green",
         alpha=rolls_alpha, label="Average Rolls per Game (Exact Formula)")
plt.plot(mc_range, avg_rolls_mc, "x", color="darkgreen", alpha=rolls_alpha,
         label="Average Rolls per Game (Monte Carlo)")
# Since the functions converge to each other as x approaches infinite, it
# might be interesting to compare them
if rolls_log:
    plt.plot(calc_range[1:], log_range[1:], "-", color="orange",
             alpha=rolls_alpha, label="log2")
rolls.legend(loc="lower right")
plt.plot(calc_range[:2], avg_rolls_calc[:2], "-", color="green",
         alpha=rolls_first_alpha)
if rolls_log:
    plt.plot(calc_range[:2], log_range[:2], "-", color="orange",
             alpha=rolls_first_alpha)
"""
plt.show()
