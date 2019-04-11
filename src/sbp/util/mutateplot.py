"""
Plots the mutation data in order to find the optimal mutation percentage
"""

import matplotlib.pyplot as plt
import numpy as np

def stringToNum(string):
    string = string.strip()
    if string == "False":
        return 0
    else:
        return 1

foundstats = [0]*50
timestats = [0]*50
lengthstats = [0]*50
totalcount = 0

with open("Data/mutatedata3.csv", "r+") as data:
    header = data.readline()
    for line in data:
        els = line.split(", ")
        foundstats[int(els[0])] += stringToNum(els[3])
        if stringToNum(els[3]) == 1:
            lengthstats[int(els[0])] += int(els[2])
            timestats[int(els[0])] += int(els[1])
"""
with open("mutatedata4_20.csv", "r+") as data:
    header = data.readline()
    for line in data:
        els = line.split(", ")
        foundstats[int(els[0])] += stringToNum(els[3])
        if stringToNum(els[3]) == 1:
            lengthstats[int(els[0])] += int(els[2])
            timestats[int(els[0])] += int(els[1])
            
with open("mutatedatamore.csv", "r+") as data:
    header = data.readline()
    for line in data:
        els = line.split(", ")
        foundstats[int(els[0])] += stringToNum(els[3])
        if stringToNum(els[3]) == 1:
            lengthstats[int(els[0])] += int(els[2])
            timestats[int(els[0])] += int(els[1])
"""
# collects only data from rounds where all of them succeeded in solving
def getdatafromfile(name):
    with open(name, "r+") as data:
        header = data.readline()
        i = 0
        alldid = True
        times = []
        lengths = []
        count = 0
        for line in data:
            els = line.split(", ")
            if i<16:
                times.append(int(els[1]))
                lengths.append(int(els[2]))
                alldid = alldid and bool(stringToNum(els[3]))
                i+=1
            else:
                i = 0
                if alldid:
                    count += 1
                    for i in range(len(times)):
                        timestats[i] += times[i]
                        lengthstats[i] += lengths[i]
                times = []
                lengths = []
                alldid = True
        return count

graphlength = [lengthstats[i]/foundstats[i] for i in range(50) if foundstats[i] != 0]

graphtime = [timestats[i]/foundstats[i] for i in range(50) if foundstats[i] != 0]
#totalcount += getdatafromfile("Data/mutatedatamore.csv")
#totalcount += getdatafromfile("Data/mutatedata4_20.csv")

#graphlength = [l/totalcount for l in lengthstats]

#graphtime = [t/totalcount for t in timestats]

x = list(range(0,50))
plt.bar(x, foundstats)
plt.show()

        
