import random
import heapq
import copy
import statistics as stats
from enum import Enum

debug = False

def test():
    i = [[1,2], [0,3]]
    f = [[1,2], [3,0]]
    puzzle = SBP(i, f)
    

def main():
    initsbp = [[1, 2, 3, 4],[6, 9, 0, 8],[5, 10, 7, 11], [12, 13, 14, 15]]
    finsbp = [[1,2,3,4],[5,6,7,8],[9,0,10,11], [12, 13, 14, 15]]
    init = [[1,2,3,4], [5,6,7,8], [9, 10, 0, 11], [12,13,14,15]]
    i = [[1,2], [0,3]]
    f = [[1,2], [3,0]]
    puzzle = SBP(initsbp, finsbp, rounds)
    if puzzle.sol == None:
        print(str(puzzle.pop[0].seq))
    else:
        print("score " + str(puzzle.sol.score) + " and solution length " + str(puzzle.sol.solpos+1))
        puzzle.sol.show()
    
    printboard(initsbp)
    printboard(finsbp)
    #explore(puzzle)

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
    for i in range(len(seq)):
        print(seq[i][0], end=", ")
    print()

def seeseqs(select):
    for item in select:
        l = item.solpos + 1
        if len == 0:
            l = len(item.seq)    
        print("Score: " + str(item.score) + "\tLength: " + str(l))

def getavg(select):
    tot = 0
    for i in select:
        tot+=i.score
    return tot/len(select)
    
class Compass():
    LEFT = (0,-1)
    RIGHT = (0,1)
    UP = (-1,0)
    DOWN = (1,0)
    
    def opp(dir):
        if dir == Compass.LEFT:
            return Compass.RIGHT
        if dir == Compass.RIGHT:
            return Compass.LEFT
        if dir == Compass.UP:
            return Compass.DOWN
        if dir == Compass.DOWN:
            return Compass.UP
            
    def name(dir):
        if dir == Compass.LEFT:
            return "LEFT"
        if dir == Compass.RIGHT:
            return "RIGHT"
        if dir == Compass.UP:
            return "UP"
        if dir == Compass.DOWN:
            return "DOWN"


class Board():
    def __init__(self, problem, pieces):
        self.matrix = problem
        self.pieces = copy.deepcopy(pieces)

    def copy(self):
        return Board(copy.deepcopy(self.matrix), self.pieces)
        
    def getpiece(self, loc = (-1,-1), id = None):
        if id == None:
            r,c = loc
            id = self.matrix[r][c]
        return self.pieces[id]
        
class SBP():

    EMPTY = 0
    
    dirs = {'u': Compass.UP, 'd': Compass.DOWN, 'r': Compass.RIGHT, 'l': Compass.LEFT}
    
    def __init__(self, problem, goal):
        length = 7
        popsize = 100
        self.sol = None
        self.zero = SBP.findzeros(problem)
        self.board = Board(problem, SBP.getPieces(problem))
        self.gb = SBP.getgoal(goal)

        self.found = False
        
        self.pop = self.getpop(self.board, length, popsize)
        self.sel = self.select()
        if debug:
            print("END INITIAL POPULATION")
        avg = []
        i=0
        self.lastavg = None
        self.inc = 0
        while self.keepgoing():
        #while i< 1:
            self.pop = self.crossover(self.sel)
            self.sel = self.select()
            self.lastavg = getavg(self.sel)
            if debug:
                print("END GENERATION " + str(i))
                print("WITH POP AVERAGE: " + str(getavg(self.pop)))
                print("WITH ELITE AVERAGE: " + str(self.lastavg))
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

        for k in pieces:
            pieces[k].setDirs()
        return pieces

    def getPieces(problem):
        return SBP.piecesFromMatrix(problem)
    
    def getgoal(goal):
        return SBP.piecesFromMatrix(goal)

    def keepgoing(self):
        avg = getavg(self.sel)
        if avg == self.lastavg:
            self.inc += 1
        else:
            self.inc = 0

        if avg == 0:
            self.found = True
            self.inc = 0
            return False
        elif self.inc%5 == 0:
            self.extend()
            return True
        elif self.inc == 51:
            print("Halting without solution")
            return False
        return True
               
    def extend(self):
        for i in range(len(self.pop)):
            self.pop[i].extend(self.getsequence(7, self.pop[i].ib))
        
    def getpop(self, ib, l, popsize):
        pop = []
        zerolist = SBP.findzeros(ib.matrix)
        score = self.manhattan(ib)
        for i in range(popsize):
            pop.append(self.getsequence(l, ib, zeros=zerolist, ongoingscore=score))
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
    def legal(move, board):
        zr,zc = move.empty
        if board.matrix[zr][zc] != SBP.EMPTY:
            return False
        mr,mc = SBP.add(move.empty, Compass.opp(move.dir))
        if board.matrix[mr][mc] != move.piece.id:
            return False
        return True
                        
    def getchild(self, mum, dad):
        child = []
        ibalter = self.board.copy()
        zeros = self.zero
        score = float("inf")
        solpos = -1
        
        for i in range(len(mum.seq)):
        
            ibmum = ibalter.copy()
            ibdad = ibalter.copy()
            
            mumlegal = SBP.legal(mum.seq[i],ibmum)
            dadlegal = SBP.legal(dad.seq[i],ibdad)
            
            if mumlegal and dadlegal:
            
                adjm, ibmum, mumempty = self.applymove(mum.seq[i], ibmum)
                adjd, ibdad, dadempty = self.applymove(dad.seq[i], ibdad)
                
                totm = self.manhattan(ibmum)
                totd = self.manhattan(ibdad)
                
                chance = random.random()
                
                if (totm < totd and chance<0.8) or (totm>=totd and chance >= 0.8):
                    child.append(mum.seq[i])
                    ibalter = ibmum
                    #zeros = SBP.replace(zeros, mum.seq[i].empty, mumempty)
                    #zeros = SBP.findzeros(ibalter.matrix)
                    if totm<score:
                        score=totm
                else:
                    child.append(dad.seq[i])
                    ibalter = ibdad
                    #zeros = SBP.replace(zeros, dad.seq[i].empty, dadempty)
                    #zeros = SBP.findzeros(ibalter.matrix)
                    if totd<score:
                        score=totd
                        
            elif mumlegal:
                adjm, ibmum, mumempty = self.applymove(mum.seq[i], ibmum)
                totm = self.manhattan(ibmum)
                child.append(mum.seq[i])
                ibalter = ibmum
                #zeros = SBP.replace(zeros, mum.seq[i].empty, mumempty)
                #zeros = SBP.findzeros(ibalter.matrix)
                if totm<score:
                    score=totm
                    
            elif dadlegal:
                adjd, ibdad, dadempty = self.applymove(dad.seq[i], ibdad)
                totd = self.manhattan(ibdad)
                child.append(dad.seq[i])
                ibalter = ibdad
                #zeros = SBP.replace(zeros, dad.seq[i].empty, dadempty)
                #zeros = SBP.findzeros(ibalter.matrix)
                if totd<score:
                    score=totd
                    
            else:
                move = self.getvalidmove(zeros, ibdad)
                adjd, ibdad, newempty = self.applymove(move, ibdad)
                #zeros = SBP.replace(zeros, move.empty, newempty)
                #zeros = SBP.findzeros(ibalter.matrix)
                totd = self.manhattan(ibdad)
                child.append(dad.seq[i])
                ibalter = ibdad
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
        
    def getvalidmove(self, zeros, board):
        zeros = SBP.findzeros(board.matrix)
        possmoves = []
        for z in zeros:
            possmoves += self.getMoves(z, board)
        num = random.randint(0,len(possmoves)-1)
        return possmoves[num] 
        
    def getMoves(self, z, board):
        moves = []
        rz, cz = z
        if board.matrix[rz][cz] != SBP.EMPTY:
            print("BAD!!!!")
        for k in SBP.dirs:
            r,c = SBP.add(z, SBP.dirs[k])
            if self.check(r,c,board) and SBP.moveable(r,c, board, k): # check there is something in that space and it can move
                moves.append(Move(z, Compass.opp(SBP.dirs[k]), board.getpiece(loc=(r,c))))
        return moves
        
            
    def add(t1, t2):
        x,y = t1
        s,p = t2
        return (x+s, y+p)
        
    def adj(self, z, board):
        dirs = ['u', 'd', 'l', 'r']
        check = False
        for d in dirs:
            check = check or self.check(z,board,d)
        return check
            
    def check(self, r, c, board):
        return SBP.within(r, c, board) and board.matrix[r][c] != SBP.EMPTY
        
    def moveable(r,c,board, dir):
        d = board.getpiece(loc=(r,c)).dir
        if d == Dir.BOTH:
            return True
        elif dir == Compass.UP or dir == Compass.DOWN:
            return d == Dir.VERTICAL
        else:
            return d == Dir.HORIZONTAL
        
    def within(r,c,board):
        size = len(board.matrix)
        return r >= 0 and c >= 0 and r<size and c<size
        
    def replace(zeros, old, new):
        for i in range(len(zeros)):
            if zeros[i] == old:
                zeros[i] = new
                return zeros
        return zeros

    # calculate manhattan before running get sequence
    def getsequence(self, length, board, ongoingscore = None, zeros = None):
        if zeros == None:
            zeros = SBP.findzeros(board.matrix) 
        ibalter = board.copy()
        seq = []
        score = float("inf") #arbitrarily high number
        if ongoingscore == None:
            ongoingscore = self.manhattan(board) 
        solpos = -1; 
        for i in range(length):
            move = self.getvalidmove(zeros,ibalter)
            adjscore, ibalter, newempty = self.applymove(move, ibalter)
            #zeros = SBP.replace(zeros, move.empty, newempty)
            #zeros = SBP.findzeros(ibalter.matrix)
            ongoingscore += adjscore
            if ongoingscore<score:
                score = ongoingscore
            seq.append(move)
            if ongoingscore == 0 and solpos == -1:
                solpos = i
        return Sequence(seq, score, ibalter, solpos)
                
    def manhattan(self, ib):
        score = 0
        for id in ib.pieces:
            if id != SBP.EMPTY:
                score += self.evalscore(ib.pieces[id])
        return score

    def evalscore(self, piece):
        if piece.id in self.gb:
            x, y = self.gb[piece.id].posits[0]
            r, c = piece.posits[0]
            score =  abs(x-r) + abs(y-c)
            return score
        return 0
        
    def applymove(self, move, ib):
        l = move.piece.length()
        newempty = SBP.add(move.empty, SBP.times(Compass.opp(move.dir), l))
        positions = ib.getpiece(id=move.piece.id).posits
        before = self.evalscore(move.piece)
        for i in range(len(positions)):
            rold, cold = positions[i]
            positions[i] = SBP.add(positions[i], move.dir)
            r,c = positions[i]
            if r < len(ib.matrix) and r >= 0 and c<len(ib.matrix) and c>=0:
                ib.matrix[r][c] = move.piece.id
            else:
                move.prin()
                printboard(ib.matrix)
            
        ib.getpiece(id=move.piece.id).posits = positions
        ib.matrix[newempty[0]][newempty[1]] = SBP.EMPTY
        after = self.evalscore(move.piece)
        adj = after-before
        return adj, ib, newempty
        
            
    def times(t,n):
        r,c = t
        r*=n
        c*=n
        return (r,c)

class Level():
    EMPTY = 0
    def __init__(self, size, numPieces):
        self.end = self.createBoard(size, numPieces)
        dist = 8
        #self.start = self.genStart(dist)

    def createBoard(self, size, numPieces):
        pieces = list(range(1, numPieces+1))
        empties = (size**2)-numPieces
        for item in range(empties):
            pieces.append(Level.EMPTY)
        random.shuffle(pieces)
        board = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(pieces[i*size+j])
            board.append(row)
        return board
        

class Move():
    def __init__(self, empty, direction, piece):
        self.empty = empty
        self.dir = direction # OF PIECE
        self.piece = piece
        self.describe = "Move " + str(piece.id) + " one space " + Compass.name(self.dir)
        
    def prin(self):
        print(self.describe)
        
        
class Sequence():
    def __init__(self, seq, score, ib, sol):
        self.seq = seq
        self.score = score
        self.ib = ib
        self.solpos = sol

    def extend(self, second):
        self.seq += second.seq
        self.score = second.score
        self.ib = second.ib
        if second.solpos != -1:
            self.solpos = second.solpos+len(self.seq)
            
    def show(self):
        if len(self.seq) == 0:
            print("something has gone wrong")
        else:
            for move in self.seq:
                move.prin()

class Piece():
    def __init__(self, i, pos):
        self.id = i
        self.posits = [pos]
        self.dir = Dir.NEITHER

    def addpos(self, pos):
        self.posits.append(pos)

    def tile(self):
        return len(self.posits) == 1
        
    def length(self):
        return len(self.posits)

    def setDirs(self):
        if self.tile():
            self.dir = Dir.BOTH
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

def levelstuff():
    level1 = Level(4, 15)
    printboard(level1.end)
    
    
if __name__ == "__main__":
    levelstuff()
