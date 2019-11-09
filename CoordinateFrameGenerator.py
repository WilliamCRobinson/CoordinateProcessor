"""
Author: William Robinson November 2019
The purpose of this module is to define functions and variables that can pull either the x, the y or the z, coordinates
in sets of frames from MDCRD files.

Goal: we start with a MDCRD file stripped of everything but the phosphorous atoms. We want to end with three files.
        A file with x coordinates with each frame set delimited by a blank line. This is outputting to a new file.
        A file with y coordinates with each frame set delimited by a blank line. This is outputting to a new file.
        A file with z coordinates with each frame set delimited by a blank line. This is outputting to a new file.

        Our data structure is something like this
                Ten columns and 38 lines.
                x  y  z  x  y  z  x  y  z  x
                y  z  x  y  z  x  y  z  x  y
                z  x  y  z  x  y  z  x  y  z
                ...
                z  x  y  z
Here's how I want the program to proceed.
1. Take user input from the console, such as the file to be called. This will make it easy to use in a bash script.

2. Open this file and call it coordToProc, now we have an object with a class that we can manipulate.

3. Read a line from this file and sort it into an array delimited by at least 2 whitespaces. Here linenumber = 0.

4.Process the coordinates in this array. And append them to the appropriate files.
"""

# This function will create files for us that we can access and append to later.


def file_maker(name_of_file):
    try:
        file_made = open(name_of_file, "x")
        file_made.close()
        print(name_of_file + "file created and closed" + "\n")
    except IOError:
        print("file already exist")
    except:
        print("Something else went wrong with file_maker")


# This function should take in a filename, a lineArray and an index of the line array to append.


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


def array_processor():
    # Take input
    # user_input_file = input("Enter a coordinate file to process: ")
    # For now just assume the input is always modified_out.crd
    user_input_file = "modified_out.crd"
    # open file from input in read mode
    coord_to_proc = open(user_input_file, "r")
    # read lines into an array
    array_of_lines = coord_to_proc.readlines()
    # take the length of the array to get a line count
    line_count = len(array_of_lines)
    # Confirm this
    print("file opened and lines counted, we have " + str(line_count) + " lines\n")

    # Create the files we will append data to
    file_maker("xCoords")
    file_maker("yCoords")
    file_maker("zCoords")

    # declare a counter, start at 1 because of header info
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

        # This case makes the end of a frame, so we should also append a new line
        if (current_line % 39 == 0 and current_line != 0) or (current_line == line_count - 1):
            print("Entering Edge Case")
            file_appender("zCoords", current_line_array, 0)
            file_appender("xCoords", current_line_array, 1)
            file_appender("yCoords", current_line_array, 2)
            file_appender("zCoords", current_line_array, 3)
        if current_line % 3 == 1:
            print("Entering Case 1")
            for i in (0, 3, 6, 9):
                file_appender("xCoords", current_line_array, i)
            for i in (1, 4, 7):
                file_appender("yCoords", current_line_array, i)
            for i in (2, 5, 8):
                file_appender("zCoords", current_line_array, i)
        if current_line % 3 == 2:
            print("Entering Case 2")
            for i in (0, 3, 6, 9):
                file_appender("yCoords", current_line_array, i)
            for i in (1, 4, 7):
                file_appender("zCoords", current_line_array, i)
            for i in (2, 5, 8):
                file_appender("xCoords", current_line_array, i)
        if current_line % 3 == 0:
            print("Entering Case 3")
            for i in (0, 3, 6, 9):
                file_appender("zCoords", current_line_array, i)
            for i in (1, 4, 7):
                file_appender("xCoords", current_line_array, i)
            for i in (2, 5, 8):
                file_appender("yCoords", current_line_array, i)
        current_line += 1
    print("Done processing your file")

array_processor()
