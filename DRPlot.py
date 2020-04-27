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


def __rdata():
    exp = np.array([1, 2 / 3, 0.62, 0.59])
    for i in range(96):
        diff_exp = exp[len(exp) - 1] - 0.5
        exp = np.append(exp, np.random.random() * diff_exp + 0.5)

    return exp
