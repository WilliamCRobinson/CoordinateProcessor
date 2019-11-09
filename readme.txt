'''
Author: William Robinson November 2019 Math and Chemistry BS with a minor in CS, in case your looking to hire me...
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
Heres how I want the program to proceed.
1. Take user input from the console, such as the file to be called. This will make it easy to use in a bash script.

2. Open this file and call it coordToProc, now we have an object with a class that we can manipulate. Hell yeah.

3. Read a line from this file and sort it into an array delimited by at least 2 whitespaces. Here linenumber = 0.

4.Process the coordinates in this array. And append them to the appropriate files.

Global Variables:
    coordToProc - the name of coordinate file that the user will enter. string expexted
    LinesInCoordToProcess - the number of lines in the coordinate file entered. int expected
    xCoord - the name of the file that will be generated for x coords. file expected
    yCoord - the name of the file that will be generated for x coords. file expected
    zCoord - the name of the file that will be generated for x coords. file expected

Functions
    file_opener - simply opens the file specified by the user and opens it.

    file_Maker - will make the coord files that will be generated, this is so that we can focus on appending in the
                in the actual algorithm.

                Be sure to use a try except finally clause to make sure its working.

    array_processor - This is the beef of the module this will take a line from the user specified file and run it
                        through a process that will append the appropriate x, y and z from the array returned
                        file opener to the correct file.

                        It should open a file. then
                        loop through the lines
                            read each line as an array
                            process the array with the function called proccessingAlgorithm(Line_Array,lineNumber)

                        This function should also be sure to open the next line of the array at the end of its loop

                        Be sure to use a try except finally clause to make sure this is working.





'''

#Psuedo Code for pulling and writing coords.
'''
Heres some pseudo code
        take user input call it coord to process
           coordToProc = read in the file coordToProc
        ^^this is a function^^    
        count line in coordToProc
            
        load lines into an array of strings, very large. ArrayofLines[lineNumber]
        
        for lineNumber in range(0,NumberOfLines) or a while loop  
	
        if (linenumber % 3 == 0):
            for i in range(0,10)
                append Line_Array[i] to x coordinate file
                i+=3
            for i in range (1,8):
                append Line_Array[i] to y coordinate file
                i+=3
            for i in range (2,9):
                append Line_Array[i] to z coordinate file
                i+=3
        elseif (linenumber % 3 == 1):
            for i in range(0,10)
                append Line_Array[i] to Y coordinate file
                i+=3
            for i in range (1,8):
                append Line_Array[i] to Z coordinate file
                i+=3
            for i in range (2,9):
                append Line_Array[i] to X coordinate file
                i+=3
        elseif (linenumber % 3 == 2):
            for i in range(0,10)
                append Line_Array[i] to z coordinate file
                i+=3
            for i in range (1,8):
                append Line_Array[i] to x coordinate file
                i+=3
            for i in range (2,9):
                append Line_Array[i] to y coordinate file
                i+=3
        else if (linenumber==39):
            append linenumber[0] to z coordinate file
            append linenumber[1] to x coordinate file
            append linenumber[2] to y coordinate file
            append linenumber[3] to z coordinatefile	
'''