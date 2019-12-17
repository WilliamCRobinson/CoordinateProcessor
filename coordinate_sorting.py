"""
Author: William Robinson December 2019
The purpose of this python module is to the sort the coordinates from an MDCRD output file.
This attempt builds on the successes of CoordinateFrameGenerator Module, which was a minor failur.
I also am going to adopt the data conventions that Lovenia is using for consistency.
"""
import os
import sys
import debugging_tools
# Filename will be equal to the first argument
filename = sys.argv[1]
if os.path.exists("xcoords") or os.path.exists("ycoords") or os.path.exists("zcoords"):
    os.remove("xcoords")
    os.remove("ycoords")
    os.remove("zcoords")
xcoords = open("xcoords", "w+")
ycoords = open("ycoords", "w+")
zcoords = open("zcoords", "w+")
line_num = 1
x_counter = 0
y_counter = 0
z_counter = 0
file = open(filename, "r")
# Skip the header So the pointer is on the first line of data.
file.__next__()
for line in file:
    current_line_string = line
    current_line_string = current_line_string.replace('\n', '')
    current_line_list = current_line_string.split(' ')
    while '' in current_line_list:
        current_line_list.remove('')
    if line_num % 3 == 1:
        # handle first case
        current_list_counter = 0
        while current_list_counter < current_line_list.__len__():
            # x coords are clc % 3 == 0
            if current_list_counter % 3 == 0:
                xcoords.write(str(current_line_list[current_list_counter]) + "\n")
                x_counter = x_counter + 1
                if x_counter == 128:
                    x_counter = 0
                    xcoords.write("\n")
            # y coords are clc % 3 == 1
            elif current_list_counter % 3 == 1:
                ycoords.write(str(current_line_list[current_list_counter]) + "\n")
                y_counter = y_counter + 1
                if y_counter == 128:
                    y_counter = 0
                    ycoords.write("\n")
            # z coords are clc % 3 == 2
            elif current_list_counter % 3 == 2:
                zcoords.write(str(current_line_list[current_list_counter]) + "\n")
                z_counter = z_counter + 1
                if z_counter == 128:
                    z_counter = 0
                    zcoords.write("\n")
            current_list_counter = current_list_counter + 1
    elif line_num % 3 == 2:
        # second case
        current_list_counter = 0
        while current_list_counter < current_line_list.__len__():
            # y coords are clc % 3 == 0
            if current_list_counter % 3 == 0:
                ycoords.write(str(current_line_list[current_list_counter]) + "\n")
                y_counter = y_counter + 1
                if y_counter == 128:
                    y_counter = 0
                    ycoords.write("\n")
            # z coords are clc % 3 == 1
            elif current_list_counter % 3 == 1:
                zcoords.write(str(current_line_list[current_list_counter]) + "\n")
                z_counter = z_counter + 1
                if z_counter == 128:
                    z_counter = 0
                    zcoords.write("\n")
            # x coords are clc % 3 == 2
            elif current_list_counter % 3 == 2:
                xcoords.write(str(current_line_list[current_list_counter]) + "\n")
                x_counter = x_counter + 1
                if x_counter == 128:
                    x_counter = 0
                    xcoords.write("\n")
            current_list_counter = current_list_counter + 1
    elif line_num % 3 == 0:
        # handle third case
        current_list_counter = 0
        while current_list_counter < current_line_list.__len__():
            # z coords are clc % 3 == 0
            if current_list_counter % 3 == 0:
                zcoords.write(str(current_line_list[current_list_counter]) + "\n")
                z_counter = z_counter + 1
                if z_counter == 128:
                    z_counter = 0
                    zcoords.write("\n")
            # x coords are clc % 3 == 1
            elif current_list_counter % 3 == 1:
                xcoords.write(str(current_line_list[current_list_counter]) + "\n")
                x_counter = x_counter + 1
                if x_counter == 128:
                    x_counter = 0
                    xcoords.write("\n")
            # y coords are clc % 3 == 2
            elif current_list_counter % 3 == 2:
                ycoords.write(str(current_line_list[current_list_counter]) + "\n")
                y_counter = y_counter + 1
                if y_counter == 128:
                    y_counter = 0
                    ycoords.write("\n")
            current_list_counter = current_list_counter + 1
    line_num = line_num + 1
xcoords.close()
ycoords.close()
zcoords.close()

debugging_tools.cfc_run()
