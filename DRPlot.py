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

"""Settings for both graphs."""

# size of the figure, in inches according to matplotlib documentation
graph_size = (16, 8)
# and the resolution - a multiplier
resolution = 110
# maximum value to calculate for rolls and winrate
calc_max = 1000
# domain for monte carlo
mc_range = [2, 5, 10, 25, 50, 100, 500, 1000]
# sample size for the Monte Carlo simuation
mc_samples = 5_000
# string to represent sample size for annotations - set to empty string to
# disable top annotation
mc_string = "100M"
# whether or not to even graph the winrate graph
wr_graph = True
# and likewise for the rolls
rolls_graph = True

"""Settings for the graph of winrates."""

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
# the ticks for the x axis.  Don't touch if you don't know what you're
# looking at
wr_xticks = np.hstack((np.arange(1, 10, 1), np.arange(10, 50, 5),
                       np.arange(50, 100, 50), np.arange(100, 1001, 100)))
# and the tick labels
wr_xlabels = np.array([1, 2, 3, 4, 5, 10, 25, 50, 100, 500, 1000])

"""Settings for the graph of roll count."""

# add annotation for the rolls graph.  At current this just annotates the
# sample size
rolls_annotate = True
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
rolls_ymax = 10
# ticks for the rolls graph
rolls_xticks = np.arange(0, 1001, 100)

"""Function for streamlining the annotations."""


def annotate(text, x, xarray, xyt):
    plt.annotate(text, xy=(x, xarray[x - 1]), xytext=xyt,
                 arrowprops=dict(arrowstyle='-'), fontsize="small")


"""Initialize the data sets.  Use small mc_samples value for testing, then
only increase when the graph's visual settings are to your liking."""

calc_range = range(1, calc_max + 1)
mc_data = drs.deathroll_mc(mc_range, mc_samples)
p1_winrate_mc = mc_data[:, 0]
p2_winrate_mc = 1 - p1_winrate_mc
avg_rolls_mc = mc_data[:, 1]

if wr_graph:
    # DeathrollCalc stores the information calculated thus far, meaning we
    # aren't reduplicating efforts in getting data twice
    p1_winrate_calc = drc.p1_winrate(calc_range)
    p2_winrate_calc = drc.p2_winrate(calc_range)
if rolls_graph:
    avg_rolls_calc = drc.avg_rolls(calc_range)
    if rolls_log:  # the range of ln, from 1 to 1000
        log_range = np.fromfunction(np.vectorize(lambda n: math.log(n + 1)),
                                    (calc_max,))

"""Create the figure for the winrates."""

# set up the figure for winrates
if wr_graph:
    winrate_fig = plt.figure(1, facecolor="#CCCCCC", figsize=graph_size,
                             dpi=resolution)
    winrate_fig.canvas.set_window_title("Deathroll Win Probability")
    # setting the properties of the axes
    winrates = plt.subplot(111, facecolor="#EEEEEE", xlabel="/roll Value",
                           ylabel="Probability of winning")
    # set the x axis as a log scale if necessary, but keep the tick values
    # scalars
    if wr_logx:
        from matplotlib.ticker import ScalarFormatter
        plt.xscale("log", basex=wr_logbase)
        winrates.xaxis.set_major_formatter(ScalarFormatter())
    # set percentages for y axis if necessary
    if wr_pery:
        from matplotlib.ticker import PercentFormatter
        winrates.yaxis.set_major_formatter(PercentFormatter(xmax=1))

    # set the xticks and yticks
    plt.xticks(wr_xticks)
    # unfortunately setting the x axis tick labels is harder than it seems when
    # you want it particular.
    ticklabels = []
    for i in wr_xticks:
        if i in wr_xlabels:
            ticklabels.append(i)
        else:
            ticklabels.append('')
    winrates.xaxis.set_ticklabels(ticklabels)
    plt.yticks(np.arange(0, 1.1, 0.1))
    # and set the background grid
    plt.grid(axis='y', alpha=0.1)

    """Perform the actual data plotting.  The data from [2, 1000] is plotted
	first with one alpha, for both the calculations and the Monte Carlo data.  
	The legend is then displayed, and the data for [1, 2] is only plotted 
	after this, so it doesn't appear on the legend.  It uses a different alpha 
	value."""

    plt.plot(calc_range[1:], p1_winrate_calc[1:], "-", color="red",
             alpha=wr_alpha, label="Player 1 Winrate (Exact Formula)")
    plt.plot(calc_range[1:], p2_winrate_calc[1:], "-", color="blue",
             alpha=wr_alpha, label="Player 2 Winrate (Exact Formula)")
    plt.plot(mc_range, p1_winrate_mc, "x", color="darkred", alpha=wr_alpha,
             label="Player 1 Winrate (Monte Carlo)")
    plt.plot(mc_range, p2_winrate_mc, "x", color="darkblue", alpha=wr_alpha,
             label="Player 2 Winrate (Monte Carlo)")
    winrates.legend(loc="lower right")
    plt.plot(calc_range[:2], p1_winrate_calc[:2], "-", color="red",
             alpha=wr_first_alpha)
    plt.plot(calc_range[:2], p2_winrate_calc[:2], "-", color="blue",
             alpha=wr_first_alpha)

    """Perform wr graph annotations."""

    if wr_annotate:
        annotate("For a 2 sided-die, the smallest\npossible deathroll, "
                 "the current\nroller only has a 33.3% chance \nof winning.",
                 2, p1_winrate_calc, (1.4, 0))
        annotate("When the die has 5 sides, the \ngap in winrate has already "
                 "substantially\ndecreased: the current roller has \na 46.6% "
                 "chance at winning.", 5, p1_winrate_calc, (3, 0.175))
        annotate("By /roll 10, this probability \nrises barely above 49%.",
                 10, p1_winrate_calc, (7, 0.33))
        annotate("At /roll 25, the difference in \nwinrates is less than "
                 "0.5%.", 25, p2_winrate_calc, (16.2, 0.41))
        annotate("For a deathroll of 100, \nthe difference in winrates is "
                 "\nless then 0.02%.", 100, p1_winrate_calc, (65, 0.41))
        annotate("At /roll 1000, the gap \nbetween winrates is "
                 "\ninfinitesimal.", 1000, p2_winrate_calc, (625, 0.42))

        # manually annotate the sample size
        if mc_string != "":
            plt.annotate("Monte Carlo Sample Size: {}".format(mc_string),
                         xy=(30, 1), fontsize="xx-large", fontweight="bold",
                         color="maroon", ha="center")


"""Set up the rolls graph."""

if rolls_graph:
    rolls_fig = plt.figure(2, facecolor="#CCCCCC", figsize=graph_size,
                           dpi=resolution)
    rolls_fig.canvas.set_window_title("Average Rolls per Deathroll")
    # the axes for rolls is a bit simpler
    rolls = plt.subplot(111, facecolor="#EEEEEE", xlabel="/roll Value",
                        ylabel="Average Rolls per Game")
    # set x axis scale
    if rolls_logx:
            # Since the graph is to be viewed by the less mathematically
            # inclined, scientific notation should be eschewed
        from matplotlib.ticker import ScalarFormatter
        plt.xscale("log", basex=rolls_logbase)
        rolls.xaxis.set_major_formatter(ScalarFormatter())
    # set y maximum
    if rolls_ymax > 0:
        plt.ylim(0, rolls_ymax)

    # set the ticks to be one at a time based on current ylim
    plt.xticks(rolls_xticks)
    plt.yticks(np.arange(0, plt.ylim()[1] + 1, 1))
    # background grid for rolls graph
    plt.grid(axis='y', alpha=0.1)

    """Plot the data for the rolls."""

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

    # annotate sample size for the rolls graph
    if mc_string != "":
        plt.annotate("Monte Carlo Sample Size: {}".format(mc_string),
                     xy=(500, 9.55), fontsize="xx-large", fontweight="bold",
                     color="maroon", ha="center")


# finally, show the graph
plt.show()
