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
from collections.abc import Iterable

"""Custom exception class for ValueError."""


class DRSimulateValueError(ValueError):
    pass

"""Custom exception class for file handling."""


class DRSimulateFileError(OSError):
    pass

"""Local private function for testing if a number is a positive integer."""


def __posint(arg, param="n"):
    try:
        arg = int(arg)
    except ValueError:
        raise DRSimulateValueError("Argument {} for {} cannot be cast "
                                   "as an integer".format(arg, param))
    if arg < 1:
        raise DRSimulateValueError(
            "Argument {} for {} is not positive".format(arg, param))
    return arg

"""This function performs Monte Carlo simulation of a large amount of 
deathroll games, and returns a 2D numpy.ndarray corresponding to results of 
the simulation.  Each list on the zeroth axis of this array is a pair, the 
first of which corresponds to the first player's winrate for a given starting 
die of n sides, and the second is the average number of rolls.

n: the number of sides on the initial die rolled.  This can either be a 
   single positive scalar, or a data structure that is Iterable (e.g. a list, 
   tuple, numpy.ndarray).  If it is an iterable data type, each element within 
   it will be considered an input for n, and the returned value will have as 
   many pairs as there are elements in n, with the ith index corresponding to 
   the number at n[i].  The returned numpy.ndarray is always a 2D array 
   regardless of what data type was inputted.
time_all: whether or not to print timing information (how long it took to 
          perform ALL of the simulations) about the process as a whole (not 
          each individual value for n) to outfile.  Default False.
simulations: the number of simulations to perform for each n.  Default 100,000.
time_each: whether to print timing information (how long it took to perform 
           the simulations) to the file object passed in to outfile.  Unlike 
           time_all, this prints the time for all simulations for each 
           individual possible n, as opposed to the entirety of the simulation 
           process.  Default False.
outfile: the open file object (NOT pathname or string) to print timing info 
         to.  If neither time_each or time_all is specified, this option is 
         ignored.  Default sys.stdout.

If simulations, n itself (not iterable) or any element within (iterable) 
cannot be casted as an integer, or is not positive, or if time_all or 
time_each cannot be casted as booleans, a DRSimulateValueError is raised.  If 
any OSError occurrs when attempting to print, a DRSimulateFileError is 
raised.  If both time_all or time_each are marked as True, but n is not 
iterable, it is equivalent to marking only one as True.
"""


def deathroll_mc(n, simulations=100_000, time_all=False, time_each=False,
                 outfile=sys.stdout):
    # check all input except outfile
    simulations = __posint(simulations, "simulations")
    try:
        time_all = bool(time_all)
    except ValueError:
        print("Argument {} for time_all not castable as a bool".format(
            time_all))
    try:
        time_each = bool(time_each)
    except ValueError:
        print("Argument {} for time_each not castable as a bool.".format(
            time_each))
    if not isinstance(n, Iterable):
        n = __posint(n)
    else:
        for i in n:
            __posint(i)  # don't actually change the number - just type check

    # start timing if relevant
    try:
        # non iterable n
        if not isinstance(n, Iterable):
            if time_all or time_each:
                time_all = True
                time_each = False
                range_timer = perf_counter()  # start timer for whole sim
            n = np.arange(n, n + 1)
        else:
            if time_all:
                range_timer = perf_counter()
        # n is a range, iterate through it
        data = np.array([])
        for i in n:
            if time_each:  # start individual timer
                unit_timer = perf_counter()
            p1_wins = 0
            roll_count = 0
            for j in range(simulations):
                dr = drs.DeathrollSim(__posint(i))
                p1_wins += 1 if dr.winner == 1 else 0
                roll_count += dr.roll_count
            data = np.append(data, [p1_wins / simulations,  # append data
                                    roll_count / simulations])
            if time_each:
                print("Monte Carlo simulation of {} samples for inital roll "
                      "of {}-sided die complete.  Time elapsed: {}s.".format(
                          simulations, __posint(i),
                          perf_counter() - unit_timer))
        if time_all:
            print("Monte Carlo simulation across {} complete.  Time "
                  "elapsed: {}s.".format(str(n), perf_counter() - range_timer))
    except OSError as ose:
        # there's a number of errors that could have been caused with file
        # I/O, each of which can be a separate subclass of OSError.  We just
        # give the same string we receive, but labelling it as a
        # DRSimulateFileError might assist the user in locating it
        raise DRSimulateFileError(str(ose))

    # reshape array properly
    data = data.reshape(len(data) // 2, 2)
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
                        metavar="simulations", type=__posint)
    parser.add_argument("n", action="store", help="the smallest (or only) "
                        "number of sides for all dice", type=__posint)

    args = parser.parse_args()
    # TODO: add option to take in range of arguments.  More annoying to do
    # perfectly with argparse than it seems

    # Run simulation and print relevant data
    data = deathroll_mc(args.n, args.s, args.time)
    print("With initial die of {} sides, player 1 wins {:.3%} of the time "
          "with an average of {:.4f} rolls per game.".format(args.n,
                                                             data[0][0],
                                                             data[0][1]))
