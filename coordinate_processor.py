"""
Author William Robinson December 2019
The purpose of this module is to process the results of a cpptraj script that strips an MDCRD file of all but one
type of atom into a 2d histograms of where those atoms are in each axis over time. This should allow us to determine at
which frame of a simulation a certain condition has been met. In our case we are looking at cell membrane self assembly,
we stripped out the phosphorous atoms of which there are 128 in our case. Then we strip them into files containing just
x coordinates, just y coordinates and just z coordinates. Then we process these into frame intervals, then we get counts
with respect to the coordinate. We then put all the frame interval counts together and from here we have a 2d histogram
of coordinate vs time with atom count in the time-coordinate bin as the intensity on the colormap.
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


def coordinate_sorting(filename, xout, yout, zout):
    '''
    The purpose of this function is to the sort the coordinates from an MDCRD output file.
    If any function needs to be refactored I would say its this one. Though I hesitate to make tweaks for
    performance because as it stands, this isnt that robust and things may easily go wrong.
    :param filename: name of mdcrd file to pull coordinates from.
    :param xout: name of x output file
    :param yout: name of y output file
    :param zout: name of z output file
    :return: null, generates output files.
    '''
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
    """
    The purpose of this function is for debugging, it checks to make sure the data obtained from the mdcrd is reasonable
    namely that at no point does it contain a line thats a double entry. Helper for CFC_run()
    :param coord: coordinate file to check
    :return: null,
    """
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
    """
    This function runs the coordinate_file_checker based on assumptions that the x file is xcoords,
    and so on for y and z.
    :return: null, prints results.
    """
    print("Bad Lines for X coordinates")
    coordinate_file_checker("xcoords")
    print("Bad Lines for Y coordinates")
    coordinate_file_checker("ycoords")
    print("Bad Lines for Z coordinates")
    coordinate_file_checker("zcoords")


def directory_cleaner(directory_to_clean):
    """
    Remakes a directory after deleting it. Maybe a better way to do this.
    I think we may not need the second case. The logic here doesnt make a ton of sense.
    :param directory_to_clean: directory to rebuild
    :return:
    """
    if os.path.exists(directory_to_clean):
        shutil.rmtree(directory_to_clean)
    if not os.path.exists(directory_to_clean):
        os.mkdir(directory_to_clean)


# This function takes a specific file and makes a CSV according to Frame Binsize


def csv_gen(file, frame_binsize, dir_string):
    """
    This function take in a file, and makes CSV files according to the frame interval size
    :param file: file containing a single coordinate, x,y or z delimited by a blank line for frames.
    :param frame_binsize: the same as frame interval size
    :param dir_string: the directory to make the csv files in
    :return: null, generates files.
    """
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
                          str(current_frame_bin) + "_.csv", index=False)
                frame_count = 0
                # Empty out the list
                list_to_csv = []
                current_frame_bin += 1
        else:
            # add the line to the list
            list_to_csv.append(line)


# This function will run the CSV generator


def run_generator(filex, dir_stringx, filey, dir_stringy, filez, dir_stringz, frame_binsize):
    """
    This function runs the csv generator
    :param filex: x coordinate file
    :param dir_stringx: file for x coordinate csvs to go into
    :param filey: y coordinate file
    :param dir_stringy: file for y coordinate csvs to go into
    :param filez: z coordinate file
    :param dir_stringz: file for z coordinate csvs to go into
    :param frame_binsize: should be set to frame_interval_size
    :return: null, ,generates files
    """
    directory_cleaner(dir_stringx)
    directory_cleaner(dir_stringy)
    directory_cleaner(dir_stringz)
    csv_gen(filex, frame_binsize, dir_stringx)
    csv_gen(filey, frame_binsize, dir_stringy)
    csv_gen(filez, frame_binsize, dir_stringz)


def csv_to_hist(csv_file, num_bins):
    """
    This function will go through a csv file prepared by the csv generator and make a graphical histogram from it.
    :param csv_file:
    :param num_bins:
    :return:
    """
    data_frame = pd.read_csv(csv_file)
    data_frame.hist(bins=num_bins)
    plt.title(csv_file[:-4])
    plt.xlim(-20, 80)
    plt.ylim(0, 75)
    plt.xlabel(csv_file[0] + " coordinate")
    plt.ylabel("Frequency")
    plt.savefig(csv_file[:-4] + ".png")
    plt.close()


def heat_mapper(axiscsv1, axiscsv2):
    """
    This function takes in two csv files and makes a 2d hexbinned histogram
    :param axiscsv1: csv for x axis
    :param axiscsv2: csv for y axis
    :return: null, saves 2d histogram
    """
    title = axiscsv1[0] + " vs. " + axiscsv2[0] + " for " + axiscsv1[8:18]
    df1 = pd.read_csv(axiscsv1)
    df2 = pd.read_csv(axiscsv2)
    plt.hexbin(x=df1, y=df2, gridsize=50, cmap="magma")
    plt.title(title)
    plt.savefig(title + ".png")
    plt.show()
    plt.close()


def create_vc_directory(maindirectorystring, valuecountstring):
    """
    This function creates a directory to store the value count csv files in.
    :param maindirectorystring: Normally the current working directory
    :param valuecountstring: the string to name our new value count directory
    :return: null
    """
    os.chdir(maindirectorystring)
    if os.path.exists(valuecountstring):
        shutil.rmtree(valuecountstring)
        os.mkdir(valuecountstring)
    else:
        os.mkdir(valuecountstring)
    os.chdir(maindirectorystring)


def create_bin_edges(low, high, width):
    """
    This function creates binned edges to be fed into create_binned_csv_counts
    :param low: the lowest bin value
    :param high: the highest bin value
    :param width: the distance between each bin value, int needed for time bins
    :return: An array containing the edges of data bins to be used for making histograms and labels.
    """
    bin_edges = []
    i = low
    while i <= high:
        bin_edges.append(i)
        i += width
    return bin_edges


def create_binned_csv_counts(maindirectorystring, bin_edges, valuecountstring):
    """
    This function takes in a directory of CSV files, and returns binned counts or tabular histograms based
    bin edges.
    :param maindirectorystring: directory of CSV files
    :param bin_edges: array containing binned edges
    :param valuecountstring: directory to put new csv files in
    :return: null
    """
    for filename in os.listdir(maindirectorystring):
        binnumber = filename.split("_")[2]
        vcfilestring = str(filename[0:17]) + str(binnumber) + "_value_counts.csv"
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
    """
    This function recursively changes the permissions of all files in a supplied path to the mode.
    :param path: directory to change permission of.
    :param mode: permission mode to change to.
    :return: null, changes files.
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for directory in [os.path.join(root, d) for d in dirs]:
            os.chmod(directory, mode)
    for file in [os.path.join(root, f) for f in files]:
        os.chmod(file, mode)


def combine_to_master(coordmastername, csvdir, frameintsize, masterdirectory):
    """
    This function combines CSV files of the same index into a main CSV file
    :param coordmastername: name of the master csv to be saved, needs to line up with the names generated by
            create_binned_csv_counts
    :param csvdir: The directory containing our binned counts as csv files.
    :param frameintsize: standard frame_interval_size used in other functions,
    :return: null, generates files
    """
    os.chdir(csvdir)
    ext = "csv"
    all_filenames = []
    for i in glob.glob('*.{}'.format(ext)):
        all_filenames.append(i)
    sorted_filenames = sorted(all_filenames, key=lambda a: int(a.split("_")[2]))
    combined_csv = pd.read_csv(sorted_filenames[0])
    for csv_to_merge in sorted_filenames:
        combined_csv = pd.merge(combined_csv, pd.read_csv(csv_to_merge))
    os.chdir("../")
    os.chdir(masterdirectory)
    combined_csv.to_csv(coordmastername + "_" + frameintsize + "_" + ".csv", index=False, encoding="utf-8")


def master_heatmap(master_csv_file, xlabels, ylabels, axis):
    """
    This function takes in a csv file, and generates a heatmap from it
    :param master_csv_file: csv file to use as dataframe
    :param xlabels: label for horizontal axis
    :param ylabels: label for vertical axis
    :return: null, generates a file
    """
    data_frame = pd.read_csv(master_csv_file)
    index_df = data_frame.set_index("Coordinate Bins")
    sns.set_style("ticks")
    sns.set(font_scale=7.5)
    fig, ax = plt.subplots(figsize=(90, 125))
    sns.heatmap(index_df, xticklabels=xlabels, yticklabels=ylabels)
    plt.xlabel("Time Bins")
    plt.ylabel("Coordinate Bins")
    figure_name = os.getcwd().replace("\\", "_").replace(":", "_")
    plt.title(axis + "_" + figure_name)
    fig.savefig(axis + "_" + figure_name + '.png')
    plt.close(fig)


def frame_counter(mdcrd):
    """
    This function counts the number of frames in a cpptraj generated MDCRD file
    :param mdcrd: output file from cpptraj script containing a single type of atom for 'count' frames
    :return: number of frames, count.
    """
    count = 0
    with open(mdcrd, "r") as f:
        for line in f:
            if line == "\n":
                count += 1
    return count


def main():
    mdcrdfilename = "modified_out.crd"
    xfile = "xcoords"
    yfile = "ycoords"
    zfile = "zcoords"
    frame_interval_size = 50
    mastdir = "master_frameintervalsize_" + str(frame_interval_size)
    # These are standard
    dir_stringx = "CSV" + "_" + xfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    dir_stringy = "CSV" + "_" + yfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    dir_stringz = "CSV" + "_" + zfile + "_" + "_frameintervalsize_" + str(frame_interval_size)
    # Sample Command "Python coordinate_processor.py modified_out.crd xcoords ycoords zcoords 20 100"
    # Run Coordinate sorting based on the first argument
    coordinate_sorting(mdcrdfilename, xfile, yfile, zfile)
    # This will output files called xfile, yfile, zfile
    # Now we can get a frame count.
    frame_count = frame_counter(xfile)
    print("Frame count " + str(frame_count))
    # Now run CSV generator on those files.
    run_generator(xfile, dir_stringx, yfile, dir_stringy, zfile, dir_stringz, frame_interval_size)
    xvcdir = "value_counts_x_frameintervalsize_" + str(frame_interval_size)
    yvcdir = "value_counts_y_frameintervalsize_" + str(frame_interval_size)
    zvcdir = "value_counts_z_frameintervalsize_" + str(frame_interval_size)
    cwd = os.getcwd()
    # This will serve to help create counts and as the y label ticks
    data_bin_edges = create_bin_edges(-20, 80, 1)
    # This will serve as the x label ticks
    time_bin_edges = create_bin_edges(0, frame_count, frame_interval_size)
    directory_cleaner(xvcdir)
    create_vc_directory(os.getcwd(), xvcdir)
    create_binned_csv_counts(dir_stringx, data_bin_edges, "value_counts_x_frameintervalsize_"
                             + str(frame_interval_size))
    directory_cleaner(yvcdir)
    create_vc_directory(os.getcwd(), yvcdir)
    create_binned_csv_counts(dir_stringy, data_bin_edges, "value_counts_y_frameintervalsize_"
                             + str(frame_interval_size))
    directory_cleaner(zvcdir)
    create_vc_directory(os.getcwd(), zvcdir)
    create_binned_csv_counts(dir_stringz, data_bin_edges, "value_counts_z_frameintervalsize_"
                             + str(frame_interval_size))
    # make the master directory and pull data from the vc directories into that directory.
    os.mkdir(mastdir)
    os.chdir(cwd)
    combine_to_master("xmaster", xvcdir, str(frame_interval_size), mastdir)
    os.chdir(cwd)
    combine_to_master("ymaster", yvcdir, str(frame_interval_size), mastdir)
    os.chdir(cwd)
    combine_to_master("zmaster", zvcdir, str(frame_interval_size), mastdir)
    os.chdir(cwd)
    # Make heatmaps
    os.chdir(mastdir)
    master_heatmap("xmaster_" + str(frame_interval_size) + "_.csv", time_bin_edges, data_bin_edges, "x")
    master_heatmap("ymaster_" + str(frame_interval_size) + "_.csv", time_bin_edges, data_bin_edges, "y")
    master_heatmap("zmaster_" + str(frame_interval_size) + "_.csv", time_bin_edges, data_bin_edges, "z")
    # clean up old directories
    os.chdir("../")
    shutil.rmtree(xvcdir)
    shutil.rmtree(yvcdir)
    shutil.rmtree(zvcdir)
    shutil.rmtree(dir_stringx)
    shutil.rmtree(dir_stringy)
    shutil.rmtree(dir_stringz)
main()
