import matplotlib.pyplot as plt
import numpy as np

import heapq

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

def scores_adjusted_graph():
    improvedscores = []
    scores = []
    with open("40ImprovedIncremental_justscores_adjusted", "r+") as read:
        for line in read:
            els = line.split(", ")
            score = float(els[2])
            improvedscores.append(score)

    with open("Data/1000boardsIncremental_scores_best_justscores_adjusted", "r+") as read:
        for line in read:
            els = line.split(", ")
            score = float(els[2])
            scores.append(score)
            if len(scores) == len(improvedscores):
                break

    plt.plot(scores)
    plt.plot(improvedscores)
    plt.show()

def justscores_graph():
    newscores = []
    oldscores = []
    with open("1000boardsIncremental_scores_best_justscores_adjusted", "r+") as read:
        for line in read:
            els = line.split(", ")
            score = 9*float(els[2]) + float(els[3].strip())
            scores.append(score)
            fifteens.append(15)
    
    plt.plot(scores)
    plt.plot(fifteens)
    plt.show()

def scores_graph():
    scores = []
    fifteens = []
    with open("1000boardsIncremental_scores_best_justscores_adjusted", "r+") as read:
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

def getTimes(filename):
    times = []
    with open(filename, "r+") as f:
        for line in f:
            els = line.split()
            if len(els) == 1:
                times.append(int(els[0]))
    return times

def plotTimes():
    inctimes = getTimes("50incs")
    imptimes = getTimes("50imps")
    gentimes = getTimes("50genetics")

    plt.plot(inctimes, label="Basic Incremental Times")
    plt.plot(imptimes, label="Improved Incremental Times")
    plt.plot(gentimes, label="Genetic Times")
    plt.title("Time taken for different generating techniques")
    plt.legend()
    plt.show()

def getLengths(filename):
    lengths = []
    with open(filename+ "_justscores_adjusted", "r+") as f:
        for line in f:
            els = line.split(", ")
            if int(els[3]) != 1:
                lengths.append(int(els[3]))
    return lengths

def plotSolutionLengths():
    plt.plot(getLengths("Data/1000boardsIncremental"), label="Incremental solution lengths")
    plt.plot(getLengths("50imps"), label="Improved Incremental solution lengths")
    print(getLengths("50incs"))
    plt.plot(getLengths("50genetics"), label="Genetic solution lengths")
    plt.legend()
    plt.title("Solution lengths of generation methods")
    plt.show()

def getScores(filename):
    scores = []
    with open(filename+ "_justscores_adjusted", "r+") as f:
        for line in f:
            els = line.split(", ")
            if int(els[3]) != 1:
                scores.append(float(els[1])+float(els[2])+0.3*float(els[3]))
    return scores

def plotScores():
    plt.plot(getScores("Data/1000boardsIncremental"), label="Incremental scores")
    plt.plot(getLengths("50imps"), label="Improved Incremental scores")
    print(getLengths("50incs"))
    plt.plot(getLengths("50genetics"), label="Genetic scores")
    plt.legend()
    plt.title("Scores of generation methods")
    plt.show()

def hiScore(item):
    i, score = item
    return score

def topFromFile(filename):
    scores = []
    i = 0
    with open(filename+ "_justscores_adjusted", "r+") as f:
        for line in f:
            els = line.split(", ")
            if int(els[3]) != 1:
                score = float(els[1])+float(els[2])+0.3*float(els[3])
                scores.append((i, score))
                i+= 1
    return heapq.nlargest(3, scores, key=hiScore)

def topScores():
    inctops = topFromFile("Data/1000boardsIncremental")
    imptops = topFromFile("50imps")
    gentops = topFromFile("50genetics")

    print(f"Incremental: {inctops}")
    print(f"Improved Incremental: {imptops}")
    print(f"Genetic: {gentops}")
 

    
    
    

#plotTimes()
#plotSolutionLengths()
#plotScores()

#distcomp()
#plotdist()

topScores()

#mutatecomp()
#simplebar()
#scores_adjusted_graph()
