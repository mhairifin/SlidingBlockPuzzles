import random
import heapq

def main():
    initsbp = [[1, 2, 3, 4],[6, 9, 0, 8],[5, 10, 7, 11], [12, 13, 14, 15]]
    finsbp = [[1,2,3,4],[5,6,7,8],[9,0,10,11], [12, 13, 14, 15]]
    init = [[1,2,3,4], [5,6,7,8], [9, 10, 0, 11], [12,13,14,15]]
    rounds=15
    length=10
    popsize = 100
    puzzle = SBP(initsbp, finsbp, rounds, length, popsize)
    print(str(puzzle.sol.seq) + " with score " + str(puzzle.sol.score))
    printboard(initsbp)
    printboard(puzzle.sol.ib)

def getavg(select):
    tot = 0
    for i in select:
        tot+=i.score
    return tot/len(select)
        

        
class SBP():
    def __init__(self, problem, goal, rounds, length, popsize):
        self.zero = SBP.findzero(problem)
        self.problem = problem
        self.gb = SBP.getgoal(goal)
        self.pop = self.getpop(problem, length, popsize)
        select = self.select()
        print("END INITIAL POPULATION")
        for i in range(rounds):
            self.pop = self.crossover(select)
            select = self.select()
            print("END GENERATION " + str(i))
            print("WITH POP AVERAGE: " + str(getavg(self.pop)))
            print("WITH ELITE AVERAGE: " + str(getavg(select)))
        lowest = float("inf")
        self.sol = Sequence("bad", "bad", "bad")
        c = 0
        for el in self.pop:
            if el.score < lowest:
                self.sol = el
                lowest = el.score
            c += 1
    
    def getgoal(goal):
        pos = {}
        for i in range(len(goal)):
            for j in range(len(goal[i])):
                pos[goal[i][j]] = [i,j]

        return pos
                
        
    def getpop(self, ib, l, popsize):
        pop = []
        for i in range(popsize):
            pop.append(self.getsequence(l, ib))
        return pop
        
    def select(self):
        best = heapq.nsmallest(int(len(self.pop)/10), self.pop, key=SBP.getscore)
        return best
        
    def getscore(seq):
        return int(seq.score)
    
    def crossover(self, select):
        crosses = []
        for mum in range(len(select)):
            for dad in range(len(select)):
                if mum != dad:
                    crosses.append(self.getchild(select[mum], select[dad]))
        crosses += select
        return crosses

    def legal(move,r,c,size):
        rnew = r+move[1][0]
        cnew = c+move[1][1]
        legal = rnew>0 and rnew < size and cnew>0 and cnew<size
        return legal
                    
    def getchild(self, mum, dad):
        child = []
        ibalter = [x[:] for x in self.problem]
        r,c = self.zero
        score = float("inf")
        
        for i in range(len(mum.seq)):
            ibmum = [x[:] for x in ibalter]
            ibdad = [x[:] for x in ibalter]
            mumlegal = SBP.legal(mum.seq[i],r,c,len(ibmum))
            dadlegal = SBP.legal(dad.seq[i],r,c, len(ibdad))
            if mumlegal and dadlegal:
                mr, mc, adjm, ibmum = self.applymove(mum.seq[i], r, c, ibmum)
                dr, dc, adjd, ibdad = self.applymove(dad.seq[i], r, c, ibdad)
                totm = self.manhattan(ibmum)
                totd = self.manhattan(ibdad)
                chance = random.random()
                if totm<totd:
                    if chance<0.8:
                        child.append(mum.seq[i])
                        ibalter = ibmum
                        r,c = mr,mc
                        if totm<score:
                            score=totm
                    else:
                        child.append(dad.seq[i])
                        ibalter = ibdad
                        r,c = dr,dc
                        if totd<score:
                            score=totd
                else:
                    if chance<0.8:
                        child.append(dad.seq[i])
                        ibalter = ibdad
                        r,c = dr,dc
                        if totd<score:
                            score=totd
                    else:
                        child.append(mum.seq[i])
                        ibalter = ibmum
                        r,c = mr,mc
                        if totm<score:
                            score=totm
            elif mumlegal:
                mr, mc, adjm, ibmum = self.applymove(mum.seq[i], r, c, ibmum)
                totm = self.manhattan(ibmum)
                child.append(mum.seq[i])
                ibalter = ibmum
                r,c = mr,mc
                if totm<score:
                    score=totm
            elif dadlegal:
                dr, dc, adjd, ibdad = self.applymove(dad.seq[i], r, c, ibdad)
                totd = self.manhattan(ibdad)
                child.append(dad.seq[i])
                ibalter = ibdad
                r,c = dr,dc
                if totd<score:
                    score=totd
            else:
                dr, dc, adjd, ibdad = self.applymove(SBP.getvalidmove(r,c,len(ibdad)), r, c, ibdad)
                totd = self.manhattan(ibdad)
                child.append(dad.seq[i])
                ibalter = ibdad
                r,c = dr,dc
                if totd<score:
                    score=totd
                
        return Sequence(child, score, ibalter)
    
    def findzero(ib):
        for i in range(len(ib)):
            for j in range(len(ib[0])):
                if ib[i][j] == 0:
                    return (i,j)
                
    def getvalidmove(r,c, size):
        possmoves = []
        if r > 0:
            possmoves.append(('U',[-1, 0]))
        if r < size-1:
            possmoves.append(('D', [1, 0]))
        if c > 0:
            possmoves.append(('L', [0, -1]))
        if c < size-1:
            possmoves.append(('R', [0, 1]))
        num = random.randint(1,len(possmoves))
        return possmoves[num-1]
        
    def getsequence(self, length, ib):
        r, c = self.zero
        ibalter = [x[:] for x in ib]
        seq = []
        score = float("inf") #arbitrarily high number
        ongoingscore = self.manhattan(ib)
        for i in range(length):
            move = SBP.getvalidmove(r,c,len(ibalter))
            r,c, adjscore, ibalter = self.applymove(move, r, c, ibalter)
            ongoingscore += adjscore
            if ongoingscore<score:
                score = ongoingscore
            seq.append(move)
        return Sequence(seq, score, ibalter)
                
    def manhattan(self, ib):
        score = 0
        for i in range(len(ib)):
            for j in range(len(ib[i])):
                if (ib[i][j] != 0):
                    score += abs(self.gb[ib[i][j]][0] - i) + abs(self.gb[ib[i][j]][1] - j)
                
        return score
        
    def applymove(self, move, r, c, ib):
        adjust = move[1]
        x = r + adjust[0]
        
        y = c + adjust[1]
        
        swap = ib[x][y]
        if swap==0:
            print("ERROR:")
            printboard(ib)
        ib[x][y] = 0
        ib[r][c] = swap
        posgb = self.gb[swap]
        old = abs(posgb[0] - x) + abs(posgb[1] - y)
        new = abs(posgb[0] - r) + abs(posgb[1] - c)
        adjscore = new - old
        return (x,y, adjscore, ib)
        
class Sequence():
    def __init__(self, seq, score, ib):
        self.seq = seq
        self.score = score
        self.ib = ib
    
def printboard(ib):
    for i in range(len(ib)):
        for j in range(len(ib[i])):
            print(str(ib[i][j]) + "\t", end="")
        print()
    print()
    
    
if __name__ == "__main__":
    main()
        
        
