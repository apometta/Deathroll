"""This file, written by Andrew H. Pometta, is the file responsible for
running the Deathroll simulations.  It creates a large number of
DeathrollSim objects, using a particular starting roll number (n).  This
run will only keep track 2 data points - the average win ratio of the first
player, and the average number of rolls per game.  Two separate Numpy lists
are used to keep track of this.

At current the plan is to simply store the data in these lists, then simply
import this file into the main graphing script and use it right in-line.
Later I might add functionality to export it to a basic .txt file.  If you
want anything more complicated (spreadsheet/database), write it yourself.
"""

from time import perf_counter  # new version of time.clock()
from sys import argv
from DeathrollSim import DeathrollSim as dsm

"""Main and only function to initialize data for exporting.  Requires
range of die sides to test, number of simulations to run per die side, and
whether to print runtime information.  The default, for arguments not
provided, are 1-100 sided dice, testing one hundred thousand times per die
side, and printing information about runtime of the function (as opposed to
silent output).  Returns a pair of lists.  The first contains, in each index
n-1 for an n sided die, the probability of the first roller winning.  The
second contains the average number of rolls per game for the respective index.
Undefined results if anything other than positive integers for the first 3
arguments are given."""


def run_sims(n_min=1, n_max=100, sim_count=100000, time_info=True):
    # Begin timing here
    if time_info:
        print("Beginning clock for building Deathroll simulation data with "
              "{} simulations for each n-sided die "
              "for all n in [{}, {}).".format(sim_count, n_min, n_max))
        start_time = perf_counter()

    avg_p1wins = []
    avg_rolls = []

    # Manually input data for a 1-sided die.
    if n_min == 1:
        avg_p1wins.append(0)
        avg_rolls.append(0)
        n_min += 1

    for n in range(n_min, n_max + 1):  # For all roll of n-sided die
        p1_wins = 0
        roll_count = 0
        for i in range(sim_count):
            # Run a simulation and log the data
            sim = dsm(n)
            p1_wins += 1 if sim.winner == 1 else 0
            roll_count += sim.roll_count

        # Average it and place the die data in the appropriate index
        avg_p1wins.append(p1_wins / sim_count)
        avg_rolls.append(roll_count / sim_count)

    # Print time information if relevant
    if time_info:
        print("Time elapsed: {:.4f}s.".format(perf_counter()))
    return ((avg_p1wins, avg_rolls))

"""If run as a standalone program, interpret command line arguments as
arguments to the function above, and print the data for each index in each
list, as well as the timing information if relevant.  Run with no command line
arguments or with -h to see a usage statement."""
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Deathroll simulations.",
                                     epilog="Alternatively, import this module"
                                     " and use the run_sims "
                                     "function to perform simulations in"
                                     " another Python program.")
