"""
Author: William Robinson November 2019
The purpose of this module is to define functions and variables that can pull either the x, the y or the z, coordinates
in sets of frames from MDCRD files.
"""
#import the system module to take command line arguments
import sys
# I like to think I've been clear but if anything is confusing don't hesitate to reach out to me. :)


# This helper function will create files for us that we can access and append to later.


def file_maker(name_of_file):
    try:
        file_made = open(name_of_file, "x")
        file_made.close()
        print(name_of_file + "file created and closed" + "\n")
    except IOError:
        print("file already exist")
    except:
        print("Something else went wrong with file_maker")


# This helper function should take in a filename, a lineArray and an index of the line array to append.


def file_appender(file_name, line_array, index_of_line_array):
    try:
        file_to_append = open(file_name, "a")
        file_to_append.write(line_array[index_of_line_array] + "\n")
        file_to_append.close()
        # What string is added to what file
        print("string " + line_array[index_of_line_array] + " added to " + file_name)
    except IOError:
        print("Could not append string to file")
    except:
        print("something went wrong with file_appender.")


# This function is the beef of this module. See Attached readme.txt and comments for details on how this works.


def array_processor():
    # Take user input as sys.argv[1] argv[0] is the module name always.
    user_input_file = sys.argv[1]
    # open file from input in read mode
    coord_to_proc = open(user_input_file, "r")
    # read lines into an array
    array_of_lines = coord_to_proc.readlines()
    # take the length of the array to get a line count
    line_count = len(array_of_lines)
    # Confirm this to the user
    print("file opened and lines counted, we have " + str(line_count) + " lines\n")

    # Create the files we will append data to with our helper function.
    file_maker("xCoords")
    file_maker("yCoords")
    file_maker("zCoords")

    # declare a counter, start at 1 because of CPPtraj header info
    current_line = 1

    while current_line < line_count:
        print("\nprocessing line " + str(current_line))
        # Process this current_line element (string) of array_of_lines a string to an array
        # First remove the newline character at the end
        array_of_lines[current_line] = array_of_lines[current_line].strip('\n')
        # then split it by two white spaces into an array
        current_line_array = array_of_lines[current_line].split("  ")
        # because of formatting, position zero is a "" lets take care of that
        current_line_array.pop(0)
        # Check that it looks normal
        print("\nHere is the Current Line Array : " + "\n" + str(current_line_array))

        # This case makes the end of a frame, so we should also append a new line to each of our coord files
        if len(current_line_array) == 4:
            print("Entering Edge Case")
            file_appender("zCoords", current_line_array, 0)
            file_appender("xCoords", current_line_array, 1)
            x_file = open("xCoords", "a")
            x_file.write("\n")
            x_file.close()
            file_appender("yCoords", current_line_array, 2)
            y_file = open("yCoords", "a")
            y_file.write("\n")
            y_file.close()
            file_appender("zCoords", current_line_array, 3)
            z_file = open("zCoords", "a")
            z_file.write("\n")
            z_file.close()
        # This is the first line case
        elif current_line % 3 == 1:
            print("Entering Case 1")
            for i in (0, 3, 6, 9):
                file_appender("xCoords", current_line_array, i)
            for i in (1, 4, 7):
                file_appender("yCoords", current_line_array, i)
            for i in (2, 5, 8):
                file_appender("zCoords", current_line_array, i)
        elif current_line % 3 == 2:
            print("Entering Case 2")
            for i in (0, 3, 6, 9):
                file_appender("yCoords", current_line_array, i)
            for i in (1, 4, 7):
                file_appender("zCoords", current_line_array, i)
            for i in (2, 5, 8):
                file_appender("xCoords", current_line_array, i)
        elif current_line % 3 == 0 and current_line != 70200:
            print("Entering Case 3")
            for i in (0, 3, 6, 9):
                file_appender("zCoords", current_line_array, i)
            for i in (1, 4, 7):
                file_appender("xCoords", current_line_array, i)
            for i in (2, 5, 8):
                file_appender("yCoords", current_line_array, i)
        current_line += 1
    print("Done processing your file")


# This function runs Our program with some side comments


def main_function():
    print("Running Array Processor")
    array_processor()
    print("Array processor successfully run!" + "\n"
          "now go and get some sun")


main_function()

