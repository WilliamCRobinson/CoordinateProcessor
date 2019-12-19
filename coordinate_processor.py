"""
Author William Robinson December 2019

The purpose of this file is to synthesize the results of the CppTraj script, coordinate_sorting.py, csv_generator.py,
and histogram_generator.py. It should also allow for the user to run the suite of programs easily.

I also figured it would be faster to have all the imports in one place since some modules had some in common
"""

import os
import sys
import shutil
import pandas as pd
import matplotlib.pyplot as plt

'''
The purpose of this function is to the sort the coordinates from an MDCRD output file.
This attempt builds on the successes of CoordinateFrameGenerator Module, which was a minor failur.
I also am going to adopt the data conventions that Lovenia is using for consistency.
'''


def coordinate_sorting(filename, xout, yout, zout):
    if os.path.exists(xout) or os.path.exists(yout) or os.path.exists(zout):
        os.remove(xout)
        os.remove(yout)
        os.remove(zout)
    xcoords = open(xout, "w+")
    ycoords = open(yout, "w+")
    zcoords = open(zout, "w+")
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


'''
The purpose of the next three functions is to process the results of coordinate_sorting into CSV files of binned frames 
(time) this takes a bit longer to run on our data sets. 5 seconds.
I believe this is working correctly. Although limited debugging has been done dec 17 2019.
'''


# Helper function for run_generator


def directory_cleaner(directory_to_clean):
    if os.path.exists(directory_to_clean):
        shutil.rmtree(directory_to_clean)
    if not os.path.exists(directory_to_clean):
        os.mkdir(directory_to_clean)


# This function takes a specific file and makes a CSV according to Frame Binsize


def csv_gen(file, frame_binsize, dir_string):
    current_frame_bin = 0
    frame_count = 0
    list_to_csv = []
    f = open(file, "r")
    for line in f:
        if line == "\n":
            frame_count += 1
            if frame_count == frame_binsize:
                # load the current list into a CSV! then reset frame count and inrement the current frame bin.
                df = pd.DataFrame(list_to_csv, columns=["Coordinates for bin " + str(current_frame_bin)])
                cwd = os.getcwd()
                os.chdir(dir_string)
                directory_to_inject = os.getcwd()
                os.chdir(cwd)
                df.to_csv(directory_to_inject + "/" + file + "_framebin_" +
                          str(current_frame_bin) + ".csv", index=False)
                frame_count = 0
                # Empty out the list
                list_to_csv = []
                current_frame_bin += 1
        else:
            # add the line to the list
            list_to_csv.append(line)


# This function will run the CSV generator


def run_generator(filex, dir_stringx, filey, dir_stringy, filez, dir_stringz, frame_binsize):
    directory_cleaner(dir_stringx)
    directory_cleaner(dir_stringy)
    directory_cleaner(dir_stringz)
    csv_gen(filex, frame_binsize, dir_stringx)
    csv_gen(filey, frame_binsize, dir_stringy)
    csv_gen(filez, frame_binsize, dir_stringz)


# This function will go through a CSV file prepared by the CSV generator and process it into a histogram

def csv_to_hist(csv_file, num_bins):
    data_frame = pd.read_csv(csv_file)
    plt.title(csv_file[:-4])
    plt.xlabel(csv_file[0] + " coordinate")
    plt.ylabel("Frequency")
    plt.savefig(csv_file[:-4])


def main():
    cwd = os.getcwd()
    mdcrdfilename = "modified_out.crd"
    xfile = "xcoords"
    yfile = "ycoords"
    zfile = "zcoords"
    frame_interval_size = 100
    coordinate_bins = 50

    # These are standard
    dir_stringx = "CSV" + "_" + xfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    dir_stringy = "CSV" + "_" + yfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    dir_stringz = "CSV" + "_" + zfile + "_" + "_frameintervalsize_" + str(frame_interval_size)

    # Sample Command "Python coordinate_processor.py modified_out.crd xcoords ycoords zcoords 20 100"
    # Run Coordinate sorting based on the first argument
    coordinate_sorting(mdcrdfilename, xfile, yfile, zfile)
    # This will output files called xfile, yfile, zfile
    # Now run CSV generator on those files.
    run_generator(xfile, dir_stringx, yfile, dir_stringy, zfile, dir_stringz, frame_interval_size)
    # We should now have three directories CSV_ifile_frameintervalsize_N
    # Enter this directory for xfile
    for csvfile in os.listdir(dir_stringx):
        os.chdir(dir_stringx)
        csv_to_hist(csvfile, coordinate_bins)
        os.chdir(cwd)
    for csvfile in os.listdir(dir_stringy):
        os.chdir(dir_stringy)
        csv_to_hist(csvfile, coordinate_bins)
        os.chdir(cwd)
    for csvfile in os.listdir(dir_stringz):
        os.chdir(dir_stringz)
        csv_to_hist(csvfile, coordinate_bins)
        os.chdir(cwd)


main()
