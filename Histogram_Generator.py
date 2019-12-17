'''
Author: William Robinson December 2019
The purpose of this module is to process the results of coordinate_system.py into a histogram of density over
binned frames (time)
'''

number_of_atoms = 128

# TODO implement function that gets a frame count, takes in file, returns number.
def frame_counter(file):
    f = open(file, "r")
    i = 0
    for line in f:
        if line == "\n":
            i +=1

# TODO implement a functions that collects coordinates into a list, returns list. Takes in file and frame count
def coordinate_collector(file, frame_count):


# TODO implement a function that shifts the values by the largest abs value in shift value.
# Takes in list and shift value returns a list
def shifter (list_of_values, shift_value):


# TODO implement a function similar to the one above but make it a deshifter.
def deshifter(list_of_values, shift_value):


# TODO implement a function that finds the shift value and returns float, takes in a list
def shift_finder(list):



# TODO implement a function that produces a CSV with the correct data
def csv_gen(list)



def main:
    #TODO implement main