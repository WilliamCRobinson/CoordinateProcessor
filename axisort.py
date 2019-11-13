xcoords = open("xcoords", "w+")
ycoords = open("ycoords", "w+")
zcoords = open("zcoords", "w+")
with open("P31traj.crd", "r") as f:
    f.next()
    num = 0
    xiter = 0
    yiter = 0
    ziter = 0
    for line in f:
        for word in line.split():
            if (num+1)%3==1:
                if xiter<128:
                    xcoords.write(word+"\n")
                    xiter += 1
                else:
                    xcoords.write("frame end\n")
                    xiter = 0
            elif (num+1)%3==2:
                if yiter<128:
                    ycoords.write(word+"\n")
                    yiter += 1
                else:
                    ycoords.write("frame end\n")
                    yiter = 0
            else:
                if ziter<128:
                    zcoords.write(word+"\n")
                    ziter += 1
                else:
                    zcoords.write("frame end\n")
                    ziter = 0
            num += 1
