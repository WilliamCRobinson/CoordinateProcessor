'''
 Author: William Robinson November 2019
 Histogram Generator
 The purpose of this module is to provide users with a with a way to generate histograms for many MDCRD files at once
 with ease.

 The idea is that an undergraduate should be able to walk up to it and know exactly what to do and why.

I am deciding doing a module to complete this task, I think making a class would be overkill. 

    Firstly we need to understand the data structure we are dealing with before we can even start coding.
'''

# importing some usefull libs for testing.
import pandas
import numpy
import matplotlib.pyplot as plot


# We should know the number of frames, the binsize for the histogram, and the number of atoms/particles in each frame.
# When refactoring we will likely pull this information for system arguments. This assumes one type of atom.
# Casting these variables since we expect numbers.

# Number of frames
number_of_frames = int(input("number of frames expected: "))
# number of atoms per frame
number_of_atoms = int(input("number of atoms expected: "))
# number of lines calculated
num_of_lines = number_of_atoms * number_of_frames
bin_size = int(input("Enter the binsize for the histogram: "))

# Now we want to open the files up and make a file to dump data too.
# Expected to be xCoords, yCoords, zCoords.

name_of_file_to_read = input("Enter the name of the file to pull coordinates from: ")

try:
    coord_file = open(name_of_file_to_read, "r")
except IOError:
    print("Could not open the indicated file, ending run")
finally:
    print("File opened, moving on to next step")

histogram_input_file = open(name_of_file_to_read+"_histogram_input", "w")

# Okay now we can start histograming.

# First we want to pull the lines into a list
list_of_lines = coord_file.readlines()

# Now we want to define a value that is absolutely larger than any of the absolute values in the coordinates.
# We can assume a given box size and that molecules shouldnt go out of bounds because of PBCs.

# cast every element of list of lines to a float.
for i in list_of_lines:
    list_of_lines[i] = float(list_of_lines[i])

# Then set a shift value for this new
shift_value = min(list_of_lines)

# Now shift all the values up by shift_value

for i in list_of_lines:
    list_of_lines[i] = list_of_lines[i] + shift_value

# See 11/25 notes for histogramming notes
length_of_list = list_of_lines.len()
# start at frame 1
current_frame = 1
# Start at first line = 0
current_line = 0

while current_line < length_of_list:
    if current_line % 129 == 0:
        # we  havent started or are at the end of a frame
        current_frame = current_frame + 1
        print("processing frame " + current_frame)
        print("skipping newline " + current_line)
        current_line = current_line + 1
    if current_line % 129 == 1:
    # we are at a new frame add the next 128 lines to an array that we can feed in matplotlib
        i = 1
        frame_array = []
        for i < 128:
            print("adding line " + current_line + "to frame array " + current_frame)
            frame_array[i] = list_of_lines[current_line]
            i = i + 1
            current_line = current_line + 1
        # now make a histogram of frame_array and save it as name_of_file_to_read + "_frame_" + current_frame
        histogram = plot.hist(frame_array, bins=20)
        plot.title("Density Distribution of P atoms")
        plot.xlabel("coordinate")
        plot.ylabel("frequency")
        plot.savefig(name_of_file_to_read + "_frame_" + str(current_frame))








