# This is currently a draft that doesn't run correctly.  No compilation errors, but seems to run indefinitely.

# collects coordinates from the appropriate number of frames into an array


def collectCoords(frameCount, coordsFile):
    currentFrame = 1
    coordsArray = []
    while currentFrame <= frameCount:
        for coord in coordsFile:
            # wcr:Have to change this to "\n" for my data structure.
            if coord == "\n":
                currentFrame += 1
                coordsFile.next()
            else:
                coordsArray.append(coord)
    return coordsArray


# finds the largest negative coordinate for minimum shift in bin sorting
# returns a negative value


def findShift(coordsArray):
    maxNegative = 0
    for coord in coordsArray:
        if coord < maxNegative:
            maxNegative = coord
    return maxNegative * (-1)


# shifts data to the right if negative values are present
# returns the shifted array


def modifyForNegatives(shift, coordsArray):
    shiftedArray = []
    for index in coordsArray.len():
        shiftedArray.append(coordsArray[index] + shift)
    return shiftedArray


# returns maximum value of an array


def getMax(array):
    max = 0
    for i in array:
        if i > max:
            max = i
    return i


# sorts shifted array into bins


def binSort(shiftedArray, binsize):
    binValues = []
    shiftedArray = modifyForNegatives()
    for coord in shiftedArray:
        binValues.append(coord / binsize)
    densityArray = [0] * getMax(binValues)
    for val in binValues.len():
        densityArray[binValues[val]] += 1
    return densityArray


# undoes shift action if necessary and generates gnuplot compatible output file


def generateOutputFile(binsize, shift, densityArray, outputFile):
    for index in densityArray.len():
        actualBinVal = index * binsize - shift
        outputFile.write(actualBinVal + "       " + densityArray[index] + "\n")


# wcr: Changed it to read in the xCoords file instead of xcoords, just cause thats what I had in my directory


def main():
    binsize = 1
    framecount = 1
    coordsFile = open("xCoords", "r")
    outputFile = open("histogramInput", "w")
    coordsArray = collectCoords(framecount, coordsFile)
    shift = findShift(coordsArray)
    shiftedArray = modifyForNegatives(shift, coordsArray)
    densityArray = binSort(shiftedArray, binsize)
    generateOutputFile(binsize, shift, densityArray, outputFile)


if __name__ == "__main__":
    main()
