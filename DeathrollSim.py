"""
This file, written by Andrew H. Pometta, is the file implementing and 
exporting the DeathrollSim class.  An instance of this class corresponds to 
a single game of deathrolling.
"""

# I don't use Numpy for this class, since it's just unnecessary overhead.
# What utilities we would want from Numpy will be used when we analyze the
# data, not in generating it.
from random import seed
from random import randint

"""Custom exception class that is a derivation of the base ValueError."""


class DeathrollValueError(ValueError):
    pass

"""
The DeathrollSim class corresponds to a single game of deathrolling.  It 
contains relevant information such as who won, the starting roll number, the 
number of rolls, and optionally, the exact sequence of rolls.

"""


class DeathrollSim:
    """The constructor for the DeathrollSim object actually does most of the 
    heavy lifting of the object.  In other words, most of the time complexity 
    of making a DeathrollSim object, and doing the actual simulation, happens 
    entirely within the constructor.  The rest of the methods in the class 
    are really for representing the object."""

    def __init__(self, start_roll, log_rolls=False):
        # check for valid input
        try:
            start_roll = int(start_roll)
        except ValueError:
            raise DeathrollValueError("start_roll must be castable as an int")
        if start_roll < 1:
            raise DeathrollValueError("start_roll must be positive")
        try:
            log_rolls = bool(log_rolls)
        except ValueError:
            raise DeathrollValueError("log_rolls must be castable as a bool")

            # internal properties
        self.__finished = False
        self.__first_rolling = True
        self.__detailed = log_rolls
        self.__n = start_roll
        # public properties
        self.initial_n = start_roll
        self.roll_count = 0
        self.winner = 0
        if self.__detailed:
            self.roll_sequence = []  # regular list, not numpy list

        # perform simulation
        while not self.__roll():
            pass

    """Performs an individual roll during the deathroll game.  Flagging the 
	second argument resets the seed generator.  Also updates all appropriate 
	properties.  Returns true if the game is over."""

    def __roll(self, reset_seed=False):
        if reset_seed:
            seed()
        self.__n = randint(1, self.__n)
        self.roll_count += 1
        if self.__detailed:
            self.roll_sequence.append(self.__n)
        if self.__n == 1:
            self.__finished = True
            self.winner = 2 if self.__first_rolling else 1
        else:
            self.__first_rolling = not self.__first_rolling
        return self.__finished

    """Innate method to convert to string implicitly.  Isn't to be used for 
	debugging - use __repr__ instead."""

    def __str__(self):
        s = "Deathroll game:\n"
        s += "\tStarting roll: {}\n".format(self.initial_n)
        s += "\tWinner: {}\n".format(ordinal(self.winner))
        s += "\tRoll Count: {}\n".format(self.roll_count)
        if self.__detailed:
            s += "\tRolls: {}\n".format(str(self.roll_sequence))
        return s

    """Printing method for a DeathrollSim used for developers and debugging.
	For fancier printing, use __str__."""

    def __repr__(self):
        s = "Deathroll (initial_n: {}, n: {}, roll_count: {}".format(
            self.initial_n, self.__n, self.roll_count)
        if self.__detailed:
            s += ", roll_sequence: {}".format(self.roll_sequence)
        s += ", finished: {}".format(self.__finished)
        if self.__finished:
            s += ", winner: {}".format(self.winner)
        s += ")"
        return s
