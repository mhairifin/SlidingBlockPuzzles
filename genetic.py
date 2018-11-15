import random
import heapq
import statistics as stats

def main():
    initsbp = [[1, 2, 3, 4],[6, 9, 0, 8],[5, 10, 7, 11], [12, 13, 14, 15]]
    finsbp = [[1,2,3,4],[5,6,7,8],[9,0,10,11], [12, 13, 14, 15]]
    init = [[1,2,3,4], [5,6,7,8], [9, 10, 0, 11], [12,13,14,15]]
    rounds = 20
    length = 7
    popsize = 100
    puzzle = SBP(initsbp, finsbp, rounds, length, popsize)
    print(str(puzzle.sol.seq) + " with score " + str(puzzle.sol.score) + " and solution length " + str(puzzle.sol.solpos+1))
    printboard(initsbp)
    printboard(finsbp)
    explore(puzzle)

def explore(puzzle):
    yn = input("Would you like to explore this result?")
    if yn=='y':
        us = input("Enter sel for select, pop for population, res to see succesfull sequence, quit to quit")
        while us != "quit":
            if us == "sel":
                seeseqs(puzzle.sel)
            elif us == "pop":
                seeseqs(puzzle.pop)
            elif us == "res":
                print(getrep(puzzle.sol))
            us = input("Enter sel for select, pop for population, res to see succesful sequence, quit to quit")

def getrep(sol):
    seq = sol.seq
    solin = sol.solpos
    for i in range(solin+1):
        print(seq[i][0], end=", ")
    print()

def seeseqs(select):
    for item in select:
        print("Score: " + str(item.score) + "\tLength: " + str(item.solpos+1))

def getavg(select):
    tot = 0
    for i in select:
        tot+=i.score
    return tot/len(select)

class Board():
    def __init__(self, problem, pieces):
        self.matrix = problem
        self.pieces = pieces

    def copy(self):
        return Board(self.board, self.pieces)
        
class SBP():
    def __init__(self, problem, goal, rounds, length, popsize):
        self.zero = SBP.findzeros(problem)
        self.board = Board(problem, pieces)
        self.gb = SBP.getgoal(goal)
        self.pop = self.getpop(problem, length, popsize)
        self.sel = self.select()
        print("END INITIAL POPULATION")
        avg = []
        i=0
        while self.keepgoing():
            self.pop = self.crossover(self.sel)
            self.sel = self.select()
            avg = getavg(self.sel)
            print("END GENERATION " + str(i))
            print("WITH POP AVERAGE: " + str(getavg(self.pop)))
            print("WITH ELITE AVERAGE: " + str(avg))
            i+=1
        self.sol = Sequence("bad", float("inf"), "bad", "bad")
        c = 0
        for el in self.sel:
            if el.score < self.sol.score:
                self.sol = el
            elif el.score == self.sol.score and el.solpos<self.sol.solpos:
                self.sol = el
            c += 1

    def piecesFromMatrix(problem):
        pieces = {}
        for r in range(len(problem)):
            for c in range(len(problem[r])):
                if problem[r][c] in pieces:
                    pieces[problem[r][c]].posits.append((r,c))
                else:
                    pieces[problem[r][c]] = Piece(problem[r][c], (r,c))

        return pieces

    def getPieces(problem):
        return piecesFromMatrix(problem)
                
    
    def getgoal(goal):
        return piecesFromMatrix(goal)

    def keepgoing(self):
        scores = [seq.score for seq in self.pop]
        elitescores = [seq.score for seq in self.sel]
        var = stats.pvariance(scores)
        avg = stats.mean(elitescores)
        if var<1 and avg == 0:
            return False
        elif var<1:
            self.extend()
            return True
        return True
                
    def extend(self):
        for i in range(len(self.pop)):
            self.pop[i].extend(self.getsequence(7, self.pop[i].ib))
        
    def getpop(self, ib, l, popsize):
        pop = []
        zeros = self.findzeros(ib)
        score = self.manhattan(ib)
        for i in range(popsize):
            pop.append(self.getsequence(l, ib, zeros=zeros, ongoingscore=score))
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

    # TODO: update legal for pieces of arbitrary size
    def legal(move,r,c,size):
        rnew = r+move[1][0]
        cnew = c+move[1][1]
        legal = rnew>0 and rnew < size and cnew>0 and cnew<size
        return legal
                    
    def getchild(self, mum, dad):
        child = []
        ibalter = [x[:] for x in self.board.matrix]
        zeros = self.zero
        score = float("inf")
        solpos = -1
        
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
            if score == 0 and solpos == -1:
                solpos = i
                
        return Sequence(child, score, ibalter, solpos)
    
    def findzeros(ib):
        zeros=[]
        for i in range(len(ib)):
            for j in range(len(ib[0])):
                if ib[i][j] == 0:
                    zeros.append((i,j))
        return zeros
                
    def getvalidmove(self, zeros, size):
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

    def validmove(self, zeros, board):
        

    # calculate manhattan before running get sequence
    def getsequence(self, length, ib, ongoingscore = None, zeros = None):
        if zeros = None:
            zeros = SBP.findzeros(ib) # calculate before getsequence
        ibalter = [x[:] for x in ib]
        seq = []
        score = float("inf") #arbitrarily high number
        if ongoingscore = None:
            ongoingscore = self.manhattan(ib) #calculate before getsequence
        solpos = -1;
        for i in range(length):
            move, zeros = SBP.getvalidmove(zeros,len(ibalter))
            adjscore, ibalter = self.applymove(move, ibalter)
            ongoingscore += adjscore
            if ongoingscore<score:
                score = ongoingscore
            seq.append(move)
            if ongoingscore == -1 and solpos == -1:
                solpos = i
        return Sequence(seq, score, ibalter, solpos)
                
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

class Move():
    def __init__(self, empty, direction, piece):
        self.empty = empty
        self.dir = direction # of piece or of empty?? - probably of piece
        self.describe = "Move " + piece.id + " one space to the " + self.dir
        
class Sequence():
    def __init__(self, seq, score, ib, sol):
        self.seq = seq
        self.score = score
        self.ib = ib
        self.solpos = sol

    def extend(self, second):
        self.seq+=second.seq
        self.score=second.score
        self.ib = second.ib
        if second.solpos != -1:
            self.solpos = second.solpos+len(self.seq)

class Piece():
    def __init__(self, i, pos):
        self.id = i
        self.posits = [pos]
        self.dir = Dir.NEITHER

    def addpos(self, pos):
        self.posits.append(pos)

    def tile(self):
        return len(self.posits) == 0

    def setDirs(self):
        if self.tile():
            self.dir = BOTH
        else:
            if self.posits[0][0] == self.posits[1][0]:
                self.dir = Dir.HORIZONTAL
            else:
                self.dir = Dir.VERTICAL
        
class Dir(Enum):
    VERTICAL = [1,0]
    HORIZONTAL = [0,1]
    BOTH = [1,1]
    NEITHER = [0,0]


def printboard(ib):
    for i in range(len(ib)):
        for j in range(len(ib[i])):
            print(str(ib[i][j]) + "\t", end="")
        print()
    print()
    
    
if __name__ == "__main__":
    main()
