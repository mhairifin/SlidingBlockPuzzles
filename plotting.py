import matplotlib.pyplot as plt
import numpy as np

nonmut = []
mut = []
dist = []
moves = []

mutnon = [0,0]

def mutatecomp():
    with open("mutatetest1.csv", 'r') as f:
        f.readline()
        for line in f:
            data = line.split(',')
            try:
                nonmut.append(int(data[1]))
                mutnon[1]+=1
            except:
                nonmut.append(None)
            try:
                mut.append(int(data[3]))
                mutnon[0]+=1
            except:
                mut.append(None)

def distcomp():
    with open("mutatedistcomp2.csv", 'r') as f:
        f.readline()
        for line in f:
            data = line.split(',')
            try:
                dist.append(int(data[0]))
            except:
                dist.append(0)
            try:
                moves.append(int(data[1]))
            except:
                dist.pop()

def plotdist():
    plt.plot(dist, moves, 'o', color='black')
    z = np.polyfit(dist, moves, 1)
    p = np.poly1d(z)
    plt.plot(dist,p(dist),"r--")
    plt.show()
    

def bar():
    w=0.3
    x = np.arange(len(nonmut))
    plt.xticks(x)
    plt.bar(x-w/2, nonmut, width=w, color='r', align='center')
    plt.bar(x+w/2, mut, width=w, color='g', align='center')
    plt.show()

def line():
    plt.plot(nonmut)
    plt.plot(mut)
    plt.show()

def simplebar():
    w=0.15
    x = [1, 1.3]
    percs = [float(i)/len(mut) for i in mutnon]
    barlist = plt.bar(x, percs, width=w, color='#96f97b', align='center')
    barlist[1].set_color('#fc5a50')
    plt.xticks(x, ["Solved with mutation", "Solved without mutation"])
    plt.show()

def getdiff(a,b):
    if a == 0 and b != 0:
        return b
    elif a != 0 and b == 0:
        return -a
    return a-b

def diff():
    diff = list(map(getdiff, nonmut, mut))
    plt.plot(diff)
    plt.show()

def piechart():
    # 0: both None 1: nonmut None 2: mut None 3: nonmut>mut 4: mut>nonmut 5: same
    pies = [0,0,0,0,0,0]
    for i in range(len(nonmut)):
        if nonmut[i] == 0 and mut[i] == 0:
            pies[0]+=1
        elif nonmut[i] == 0:
            pies[1]+=1
        elif mut[i] == 0:
            pies[2]+=1
        elif nonmut[i]>mut[i]:
            pies[3]+=1
        elif mut[i]>nonmut[i]:
            pies[4]+=1
        else:
            pies[5]+=1
    labels = "None", "Mutate Found", "NonMutate Found", "Both Found; Mutate Shorter", "Both Found; NonMutate Shorter", "Both Found; Same Length"
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightsalmon', 'thistle']
    plt.pie(pies, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.show()

def scores_graph():
    scores = []
    fifteens = []
    with open("Data/1000boardsIncremental_scores", "r+") as read:
        for line in read:
            els = line.split()
            if len(els) == 1:
                scores.append(float(els[0]))
                fifteens.append(15)
                if len(scores) == 100:
                    break;
    
    plt.plot(scores)
    plt.plot(fifteens)
    plt.show()

#distcomp()
#plotdist()

#mutatecomp()
#simplebar()
scores_graph()
