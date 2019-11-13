# CoordinateProcessor
For the coordinate processor project

William:
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
ASSUMPTIONS
    1. 1 atom per crd file with N frames and M lines per frame M*N total lines in file.
    2. Assume it is the product of a CPPtraj script
    3. We assume the data structure described above, with new line charactes and 2 white spaces between each number
    4. each number is xx.xxx or _y.yyy if it is single digit. We include the white space with it.

Here's how I want the program to proceed.
1. Take user input from the console, such as the file to be called. This will make it easy to use in a bash script.

2. Open this file and call it coordToProc, now we have an object with a class that we can manipulate.

3. Read a line from this file and sort it into an array delimited by at least 2 whitespaces. Here linenumber = 0.

4.Process the coordinates in this array. And append them to the appropriate files.


Global Variables:
	num_lines - the number of lines in the file read in by the user. 

Functions
	line_counter - this function simply counts the lines of a given file 
	
	file_maker - this function makes the file for array processor to append to. 

	strin_processor - this function turns a string into an array, each element delimited by two white spaces.

	file_appender - this function appends a string to a file on a new line, it takes in a file name, a line turned into an array and an index

	array_processor - this function looks at each array of each line and processes the elements according to index and linenumber. 


Notes on Parsing the Strucure

	On line 0 we have cpptraj info we skip that 
	on line 1 we have x in 0,3,6,9
			y in 1,4,7
			z in 2,5,8
	on line 2 we have y in 0,3,6,9
			z in 1,4,7
			x in 2,5,8
	on line 3 we have z in 0,3,6,9
			x in 1,4,7
			y in 2,5,8
	this repeats until the last line of the frame
		we have z in 0
			x in 1
			y in 2
			z in 3
	then the frame ends. 
