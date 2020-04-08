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
from sys import stdout
from sys import stderr
import DeathrollSim as drs


"""Custom exception class for ValueError."""


class DRSimulateValueError(ValueError):
    pass

"""Custom exception class for file handling."""


class DRSimulateFileError(OSError):
    pass

"""Function to run Deathroll simulations across a range of possible die 
sides.  Runs a number of simulations (equal to sim_count) across all possible 
die sides from n_min to n_max.

n_min: The smallest n for any n-sided die to simulate.
n_max: The largest n for any n_sided die to simulate.  Can be less than, equal 
       to or greater than n_min.  Default: n_min
sim_count: The number of simulations to run per die side.
time_info: If flagged as true, print information about time elasped during 
           simulation runtime.
outfile: If time_info is flagged, outfile is a open file object (NOT a path) 
         to output the data to.

If n_min, n_max or sim_count are not castable as integers, or if they are not 
positive, a DRSimulateValueError is raised.  If time_info cannot be cast as a 
boolean, a DRSimulateValueError is raised.  If printing to the outfile would 
otherwise cause an OSError, it is reraised as a DRSimualteFileError with the 
same message.
"""


def run_sims(n_min, n_max=None, sim_count=100000, time_info=False,
             outfile=stdout):
    # check values - this local function is slightly different than the one
    # in the main method

    def check_posint(arg, param):
        try:
            arg = int(arg)
        except ValueError:
            raise DRSimulateValueError("Argument {} for {} cannot be cast "
                                       "as an integer".format(arg, param))
        if arg < 1:
            raise DRSimulateValueError(
                "Argument {} for {} is not positive".format(arg, param))
        return arg

    n_min = check_posint(n_min, "n_min")
    n_max = check_posint(n_max, "n_max")
    sim_count = check_posint(sim_count, "sim_count")

    try:
        time_info = bool(time_info)
    except ValueError:
        raise DRSimulateValueError("Cannot cast {} as boolean".format(
            time_info))

    # reverse if arguments are switched
    step = 1
    if n_min > n_max:
        tmp = n_min
        n_min = n_max
        n_max = tmp
        step = -1

    die_range = range(n_min, n_max + 1, step)
    # Begin timing here
    if time_info:
        try:
            print("Beginning clock for building Deathroll simulation data "
                  "with {} simulations for each n-sided die "
                  "for all n in [{}, {}).".format(sim_count, n_min, n_max))
        except OSError as ose:
            raise DRSimualteFileError(ose.__str__())
        start_time = perf_counter()

    avg_p1wins = []
    avg_rolls = []

    for n in die_range:  # For all roll of n-sided die
        p1_wins = 0
        roll_count = 0
        for i in range(sim_count):
            # Run a simulation and log the data
            sim = drs.DeathrollSim(n)
            p1_wins += 1 if sim.winner == 1 else 0
            roll_count += sim.roll_count

        # Average it and place the die data in the appropriate index
        avg_p1wins.append(p1_wins / sim_count)
        avg_rolls.append(roll_count / sim_count)

    # Print time information if relevant
    if time_info:
        try:
            print("Time elapsed: {:.4f}s.".format(perf_counter() - start_time))
        except OSError as ose:
            raise DRSimualteFileError(ose.__str__())
    return ((die_range, avg_p1wins, avg_rolls))

"""If run as a standalone program, interpret command line arguments as
arguments to the function above, and print the data for each index in each
list, as well as the timing information if relevant.  Run with no command line
arguments or with -h to see a usage statement."""
if __name__ == "__main__":
    # First step: parse and evaluate arguments.
    import argparse

    # local function not needed outside of this part
    def check_posint(n_str):
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
                                     " and use the run_sims "
                                     "function to perform simulations in"
                                     " another Python program.")
    parser.add_argument("-t", "--time", action="store_true",
                        help="print runtime diagnostics")
    parser.add_argument("-s", action="store",
                        default=100000, help="number of simulations to run "
                        "per n-sided die (default: 100000",
                        metavar="simulations", type=check_posint)
    parser.add_argument("min", action="store", help="the smallest (or only) "
                        "number of sides for all dice", type=check_posint)
    parser.add_argument("max", action="store", help="the largest number of "
                        "sides for all dice", nargs=argparse.REMAINDER,
                        type=check_posint)
    # storing the actual arguments
    args = parser.parse_args()
    # The only thing we have to check manually is whether more arguments
    # were supplied.  We mimic the argparse error handling if this is the
    # case
    if len(args.max) == 0:
        args.max = args.min  # sets the var as a number, not a list
    elif len(args.max) == 1:
        args.max = args.max[0]  # an advantage of dynamic typing
    else:
        print("{}: error: too many arguments".format(argv[0]),
              file=stderr)
    # the args variable now has the min, max, simulations and time properties
    # set properly
