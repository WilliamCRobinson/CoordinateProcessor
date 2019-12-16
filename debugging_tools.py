"""
Author: William Robinson
Hopefully this file allows us to determine whether or not the other modules are working as expected.

The current mission with this is to check the formatting of the coords files output by the CFG because some coordinates
share the same line in the files. This is bad for making a CSV of every 128 lines for 1800 coordinates.

"""

def coordinate_file_checker(coord):
    coordinates = open(coord, "r")
    # read through the lines and check for ones that have too many numbers.
    list_of_coordinates = coordinates.readlines()
    i = 0
    while i < list_of_coordinates.__len__():
        if list_of_coordinates[i].__len__() >= 9:
            print("Found Bad Line on line " + str(i) + ": ")
            print(list_of_coordinates[i])
        i = i + 1

def cfc_run:
    print("Bad Lines for X coordinates")
    coordinate_file_checker("xCoords")
    print("Bad Lines for Y coordinates")
    coordinate_file_checker("yCoords")
    print("Bad Lines for Z coordinates")
    coordinate_file_checker("zCoords")

cfc_run()