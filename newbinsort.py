frameCount = input("Number of Frames: ")
binsize = input("Bin Size: ")
molecules = 128

coordsFile = open("xcoords", "r")
histogramInput = open("histogram", "w")
coordsArray = []

#collects all coordinates being used into one array
lines = coordsFile.read().splitlines()
for frame in range(0,frameCount):
    for coord in range(0+frame*molecules+frame,molecules+frame*molecules+frame):
        coordsArray.append(float(lines[coord]))

#finds shift for negatives
min = 0
for coord in coordsArray:
    if(coord<min):
        min = coord
shift = min*(-1)

#modifies for negatives, applies shift to data
shiftedArray = []
for coord in coordsArray:
    shiftedArray.append(float(coord)+shift)

#calculates bin for each value
binArray = []
for coord in shiftedArray:
    binArray.append(int(coord/binsize))

#gets maximum bin for density array size
max = 1
for coord in binArray:
    if(coord>max):
        max = coord

#sorts into density array
densityArray = [0]*(max+1)
for coord in binArray:
    densityArray[coord] += 1

#generates output file to be graphed
for index in range(0,max+1):
    actualBin = index*binsize-shift
    histogramInput.write(str(actualBin)+"	"+str(densityArray[index])+"\n")
