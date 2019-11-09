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


def line_counter(file_to_count):
    global num_lines
    try:
        # hopefully the way it is called below should ensure this works.
        count_this = open(file_to_count, "r")
        array_of_lines = count_this.readlines()
        num_lines = array_of_lines.length()
        print("Lines Counted!")
        return num_lines
    except IOError:
        print("could not count the lines in the specified file")
    except:
        print("Something went wrong with line_counter")


# This function will create files for us that we can access and append to later.


def file_maker(name_of_file):
    try:
        file_made = open(name_of_file, "x")
        file_made.close()
        print(name_of_file + "file created and closed")
    except IOError:
        print("file already exist")
    except:
        print("Something else went wrong with file_maker")


# A function to process an element of an array of strings
# into an array delimited by two white spaces. So it should
# process a string into an array.


def string_processor(string_to_proc):
    string_array = string_to_proc.strip("  ")
    return string_array


# This function should take in a filename, a lineArray and an index of the line array to append.


def file_appender(file_name, line_array, index_of_line_array):
    try:
        file_to_append = open(file_name, "a")
        file_to_append.write(line_array[index_of_line_array] + "\n")
        file_to_append.close()
        print("string added to " + file_name)
    except IOError:
        print("Could not append string to file")
        quit()
    except:
        print("something went wrong with file_appender.")


def array_processor():
    # Open the file we are processing
    user_input_file = input("Enter a coordinate file to process.")
    try:
        coord_to_proc = open(user_input_file, "r")
        # Get a count of the lines in coord_to_proc
        line_count = line_counter(coord_to_proc)
    except:
        print("the file does not exist")
        return

    # process into an array of lines

    array_of_lines = coord_to_proc.readlines()

    # print the count
    print(line_counter(coord_to_proc))

    # Create the files we will append data to
    file_maker("xCoords")
    file_maker("yCoords")
    file_maker("zCoords")

    # declare a counter
    current_line = 0

    while current_line < line_count:
        # Process this element of array_of_lines a string to an array
        current_line_array = string_processor(array_of_lines[current_line])

        # This case makes the end of a frame, so we should also append a new line
        if current_line % 39 == 0 and current_line != 0:
            file_appender("zCoords", current_line_array, 0)
            file_appender("xCoords", current_line_array, 1)
            file_appender("yCoords", current_line_array, 2)
            file_appender("zCoords", current_line_array, 3)
        if current_line % 3 == 0:
            for i in range(0, 10):
                file_appender("xCoords", current_line_array, i)
                i += 3
            for i in range(1, 8):
                file_appender("yCoords", current_line_array, i)
                i += 3
            for i in range(2, 9):
                file_appender("zCoords", current_line_array, i)
                i += 3
        if current_line % 3 == 1:
            for i in range(0, 10):
                file_appender("yCoords", current_line_array, i)
                i += 3
            for i in range(1, 8):
                file_appender("zCoords", current_line_array, i)
                i += 3
            for i in range(2, 9):
                file_appender("xCoords", current_line_array, i)
                i += 3
        if current_line % 3 == 2:
            for i in range(0, 10):
                file_appender("zCoords", current_line_array, i)
                i += 3
            for i in range(1, 8):
                file_appender("xCoords", current_line_array, i)
                i += 3
            for i in range(2, 9):
                file_appender("yCoords", current_line_array, i)
                i += 3
        current_line += 1


array_processor()
