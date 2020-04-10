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
import sys
import DeathrollSim as drs
import numpy as np

"""Custom exception class for ValueError."""


class DRSimulateValueError(ValueError):
    pass

"""Custom exception class for file handling."""


class DRSimulateFileError(OSError):
    pass

"""Local private function for testing if a number is a positive integer."""


def __posint(arg, param):
    try:
        arg = int(arg)
    except ValueError:
        raise DRSimulateValueError("Argument {} for {} cannot be cast "
                                   "as an integer".format(arg, param))
    if arg < 1:
        raise DRSimulateValueError(
            "Argument {} for {} is not positive".format(arg, param))
    return arg

"""Function to perform Monte Carlo simulation to find the winrate of the
first roller in a deathroll game and the average number of rolls per game
given n, where n is the number of sides of the first die rolled.

n: The number of sides of the first die rolled.  Mandatory argument.
simulations: the number of simulations to run.  Default 100,000.
time_info: If supplied as true, prints the amount of time taken to run the
           simulation to the open file object passed in to outfile.  Default 
           false.
outfile: The open file object to print the data to.  Default sys.stdout.

Returns a pair, the first of which is a float corresponding to the probability
of the first player winning, and the second of which is the average number of
die rolls per game.

n and simulations are cast as integers, and time_info is cast as a boolean.
If they cannot be cast as such, or if n or simulations are not positive, then
a DRSimulateValueError, an extension of ValueError, is raised.  If any
OSError occurs when printing to outfile, then an extension error called
DRSimulateFileError is raised.
"""


def deathroll_mc(n, simulations=100_000, time_info=False,
                 outfile=sys.stdout):
    # check values - raises a DRSimulateValueError if the numbers inputted
    # aren't positive integers, or if time_info can't be casted as a boolean

    n = __posint(n, "n")
    simulations = __posint(simulations, "simulations")

    try:
        time_info = bool(time_info)
    except ValueError:
        raise DRSimulateValueError("Cannot cast {} as boolean".format(
            time_info))

    try:
        # Begin clock
        if time_info:
            print("Beginning Monte Carlo simulation for {} deathrolls for "
                  "initial roll of {}-sided die.".format(simulations, n),
                  file=outfile)
            start_time = perf_counter()

        # perform simulation
        p1_wins = 0
        roll_count = 0
        for i in range(simulations):
            sim = drs.DeathrollSim(n)
            p1_wins += 1 if sim.winner == 1 else 0
            roll_count += sim.roll_count

        # Print time information if relevant
        if time_info:
            print("Time elapsed: {:.3f}s.".format(perf_counter() - start_time),
                  file=outfile)
    except OSError as ose:
        raise DRSimualteFileError(ose.__str__())

    # returns a pair of floats
    return (p1_wins / simulations, roll_count / simulations)

"""Function to perform deathroll simulations on a range of numbers.
Effectively runs deathroll_mc on numpy.arange(n_min, n_max, step).  Also
optionally prints time information for the whole process.

n_min: The bottom end of the range, inclusive.  Default: 1.
n_max: the upper end of the range, exclusive.
step: The difference between each successive element in the range.  Default 1.
time_info: If supplied as true, prints the amount of time taken to run the
           simulation to the open file object passed in to outfile.  Default 
           false.
outfile: The open file object to print the data to.  Default sys.stdout.

The return value is a 2D Numpy array.  For each entry along the 0th axis, 
the 0th index is the given n in the range, the 1st index is the first roller's 
win probability, and the 2nd index is the average number of rolls.

n_min, n_max, and simulations must be positive.  n_min, n_max, step and 
simulations must be castable as integers, and time must be castable as a 
boolean.  Otherwise, a DRSimulateValueError is raised.  If any error occurs 
printing to the file, a DRSimulateFileError is raised.
"""


def deathroll_mc_range(n_min, n_max=None, step=1, simulations=100_000,
                       time_info=False, outfile=sys.stdout):
    # to simulate Python's range function and numpy's arange function, we
    # have the second argument represented by input if only one argument is
    # supplied
    if n_max == None:
        n_min, n_max = 1, n_min

    # Check arguments
    n_min, n_max = __posint(n_min, "n_min"), __posint(n_max, "n_max")
    simulations = __posint(simulations, "simulations")

    # We check step manually, since it can be negative
    try:
        step = int(step)
    except ValueError:
        raise DRSimulateValueError("Cannot cast step as an integer.")

    try:
        time_info = bool(time_info)
    except ValueError:
        raise DRSimulateValueError("Cannot cast {} as boolean".format(
            time_info))

    try:
        # Begin clock
        if time_info:
            print("Beginning Monte Carlo simulation for {} deathrolls for "
                  "initial roll of n-sided die, for all in [{}, {}) with "
                  "successive change of {}.".format(simulations, n_min,
                                                    n_max, step))
            start_time = perf_counter()

        # run simulations
        data = np.array([])
        n_range = np.arange(n_min, n_max, step)
        for n in n_range:
            d_n = deathroll_mc(n, simulations)
            data = np.append(data, (n, d_n[0], d_n[1]))

        # reshape the data to a 2D array
        data = data.reshape(len(n_range), 3)

        # stop the clock
        if time_info:
            print("Time elapsed: {:.3f}s.".format(perf_counter() - start_time),
                  file=outfile)
    except OSError as ose:
        raise DRSimualteFileError(ose.__str__())

    return data

"""If run as a standalone program, take in options and input into the
deathroll_mc function.  Run the program with the sole option - h to see a
usage statement.  Output is to sys.stdout: use traditional command line
piping / output redirection to control this."""
if __name__ == "__main__":
    # First step: parse and evaluate arguments.
    import argparse
    # function given to argparse to test validity of input.  Excpects a string
    # of the argument supplied, and throws an argparse exception if it is not
    # valid.  Returns the number as an integer if it is (casts floats as
    # integers).

    def posint(n_str):
        n = int(n_str)
        if float(n_str) != n:
            raise argparse.ArgumentTypeError(
                "{} is not an integer".format(n_str))
        elif n < 1:
            raise argparse.ArgumentTypeError(
                "{} is not positive".format(n_str))
        else:
            return n

    parser = argparse.ArgumentParser(description="Run Deathroll simulations.",
                                     epilog="Alternatively, import this module"
                                     " and use the deathroll_mc "
                                     "function to perform simulations in"
                                     " another Python program.")
    parser.add_argument("-t", "--time", action="store_true",
                        help="print runtime diagnostics")
    parser.add_argument("-s", action="store",
                        default=100_000, help="number of simulations to run "
                        "per n-sided die (default: 100000)",
                        metavar="simulations", type=posint)
    parser.add_argument("n", action="store", help="the smallest (or only) "
                        "number of sides for all dice", type=posint)

    args = parser.parse_args()
    # TODO: add option to take in range of arguments.  More annoying to do
    # perfectly with argparse than it seems

    # Run simulation and print relevant data
    data = deathroll_mc(args.n, args.s, args.time)
    print("With initial die of {} sides, player 1 wins {:.3%} of the time "
          "with an average of {:.4f} rolls per game.".format(args.n,
                                                             data[0], data[1]))
