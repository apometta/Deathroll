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