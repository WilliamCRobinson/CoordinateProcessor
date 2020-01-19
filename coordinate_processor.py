"""
Author William Robinson December 2019

The purpose of this module is to synthesize the results of the CppTraj script, coordinate_sorting.py, csv_generator.py,
and histogram_generator.py. It should also allow for the user to run the suite of programs easily.

I also figured it would be faster to have all the imports in one place since some modules had some in common

This needs to run on python 3. python 2 will give you issues on linux.
"""

import os
import shutil
import glob
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
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


def cfc_run():
    print("Bad Lines for X coordinates")
    coordinate_file_checker("xcoords")
    print("Bad Lines for Y coordinates")
    coordinate_file_checker("ycoords")
    print("Bad Lines for Z coordinates")
    coordinate_file_checker("zcoords")


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
                df = pd.DataFrame(list_to_csv, columns=["Time bin " + str(current_frame_bin)])
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
    data_frame.hist(bins=num_bins)
    plt.title(csv_file[:-4])
    plt.xlim(-20, 80)
    plt.ylim(0, 75)
    plt.xlabel(csv_file[0] + " coordinate")
    plt.ylabel("Frequency")
    plt.savefig(csv_file[:-4] + ".png")
    plt.close()


# This function takes in two CSV files and produces a 2d Hexbinned histogram
def heat_mapper(axiscsv1, axiscsv2):
    title = axiscsv1[0] + " vs. " + axiscsv2[0] + " for " + axiscsv1[8:18]
    df1 = pd.read_csv(axiscsv1)
    df2 = pd.read_csv(axiscsv2)
    plt.hexbin(x=df1, y=df2, gridsize=50, cmap="magma")
    plt.title(title)
    plt.savefig(title + ".png")
    plt.show()
    plt.close()


'''
These four methods are intended to assist in processing the data for each of the axes. 
'''


# Creates a directory to store the value count csv files in.
# Handles case, where files exist, this prevents double writing
def create_vc_directory(maindirectorystring, valuecountstring):
    os.chdir(maindirectorystring)
    if os.path.exists(valuecountstring):
        shutil.rmtree(valuecountstring)
        os.mkdir(valuecountstring)
    else:
        os.mkdir(valuecountstring)
    os.chdir(maindirectorystring)


# Defines bin edges to be fed into create_binned_csv_counts
def create_bin_edges(low, high, width):
    bin_edges = []
    i = low
    while i <= high:
        bin_edges.append(i)
        i += width
    return bin_edges


def create_binned_csv_counts(maindirectorystring, bin_edges, valuecountstring):
    for filename in os.listdir(maindirectorystring):
        binnumber = filename[16:19]
        binnumber = binnumber.strip('.').strip('_')
        vcfilestring = str(filename[0:17]) + binnumber + "_value_counts.csv"
        os.chdir(maindirectorystring)
        os.chmod(filename, 0o7777)
        df = pd.read_csv(filename)
        data_array = df["Time bin " + str(binnumber)].to_numpy()
        os.chdir("../")
        os.chdir(valuecountstring)
        pd.cut(data_array, bin_edges).value_counts().to_csv(vcfilestring, index_label="Coordinate Bins",
                                                            index=True, header=["Time bin " + str(binnumber)])
        os.chdir("../")


def change_permission(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for directory in [os.path.join(root, d) for d in dirs]:
            os.chmod(directory, mode)
    for file in [os.path.join(root, f) for f in files]:
        os.chmod(file, mode)


# Combines CSV files of the same index into a main CSV file.
def combine_to_master(coordmastername, csvdir):
    os.chdir(csvdir)
    ext = "csv"

    all_filenames = []
    for i in glob.glob('*.{}'.format(ext)):
        all_filenames.append(i)

    sorted_filenames = sorted(all_filenames, key=lambda a: int(a.split("_")[2]))

    combined_csv = pd.read_csv(sorted_filenames[0])
    for csv_to_merge in sorted_filenames:
        combined_csv = pd.merge(combined_csv, pd.read_csv(csv_to_merge))
    combined_csv.to_csv(coordmastername + ".csv", index=False, encoding="utf-8")


def master_heatmap(master_csv_file):
    data_frame = pd.read_csv(master_csv_file)
    transposed_index_df = data_frame.set_index("Coordinate Bins").T
    fig, ax = plt.subplots()
    sns.heatmap(transposed_index_df)
    fig.savefig(master_csv_file[:-4] + '.png')



def main():
    mdcrdfilename = "modified_out.crd"
    xfile = "xcoords"
    yfile = "ycoords"
    zfile = "zcoords"
    frame_interval_size = 20
    print("Lets get that started!")
    # These are standard
    dir_stringx = "CSV" + "_" + xfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    dir_stringy = "CSV" + "_" + yfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    dir_stringz = "CSV" + "_" + zfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    print("Sorting coordinates from crd file")
    # Sample Command "Python coordinate_processor.py modified_out.crd xcoords ycoords zcoords 20 100"
    # Run Coordinate sorting based on the first argument
    coordinate_sorting(mdcrdfilename, xfile, yfile, zfile)
    print("Coordinates sorted")
    # This will output files called xfile, yfile, zfile
    # Now run CSV generator on those files.
    print("generating CSV files")
    run_generator(xfile, dir_stringx, yfile, dir_stringy, zfile, dir_stringz, frame_interval_size)
    xvcdir = "value_counts_x_frameintervalsize_" + str(frame_interval_size)
    yvcdir = "value_counts_y_frameintervalsize_" + str(frame_interval_size)
    zvcdir = "value_counts_z_frameintervalsize_" + str(frame_interval_size)
    cwd = os.getcwd()
    data_bin_edges = create_bin_edges(-20, 100, 1)
    create_vc_directory(os.getcwd(), xvcdir)
    create_binned_csv_counts(dir_stringx, data_bin_edges, "value_counts_x_frameintervalsize_"
                             + str(frame_interval_size))
    create_vc_directory(os.getcwd(), yvcdir)
    create_binned_csv_counts(dir_stringy, data_bin_edges, "value_counts_y_frameintervalsize_"
                             + str(frame_interval_size))
    create_vc_directory(os.getcwd(), zvcdir)
    create_binned_csv_counts(dir_stringz, data_bin_edges, "value_counts_z_frameintervalsize_"
                             + str(frame_interval_size))
    os.chdir(cwd)
    combine_to_master("xmaster", xvcdir)
    os.chdir(cwd)
    combine_to_master("ymaster", yvcdir)
    os.chdir(cwd)
    combine_to_master("zmaster", zvcdir)
    os.chdir(cwd)
    print("CSV files generated")
    os.chdir(xvcdir)
    master_heatmap("xmaster.csv")
    os.chdir("../")
    os.chdir(yvcdir)
    master_heatmap("ymaster.csv")
    os.chdir("../")
    os.chdir(zvcdir)
    master_heatmap("zmaster.csv")
    os.chdir("../")


main()
