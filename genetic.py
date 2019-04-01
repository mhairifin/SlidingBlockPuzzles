import random
import heapq
import copy
import statistics as stats
from enum import Enum
import sys, pygame
from pygame import time
import numpy as np

debug = True
messages = False

def test():
    i = [[0,0,0,1,1,1],
         [0,0,0,0,0,0],
         [2,2,0,0,3,0],
         [0,0,4,0,3,0],
         [0,0,4,0,3,0],
         [0,0,0,5,5,0]]
    f = [[0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,2,2],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0]]
    puzzle = SBP(i, f)
    #SBP.getvalidmove(puzzle.board).prin()

    puzzle.solve(mutate=True)
    sollen = puzzle.sol.solpos+1
    if puzzle.sol == None:
        print(str(puzzle.pop[0].seq))
    else:
        print("score " + str(puzzle.sol.score) + " and solution length " + str(puzzle.sol.solpos+1))
        if messages:
            puzzle.sol.show()
    visualize(puzzle)
    
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
    def __init__(self, problem, pieces=None):
        self.matrix = problem
        if pieces == None:
            self.pieces = SBP.piecesFromMatrix(problem)
        else:
            self.pieces = copy.deepcopy(pieces)

    def copy(self):
        return Board(copy.deepcopy(self.matrix), copy.deepcopy(self.pieces))
        
    def getpiece(self, loc = (-1,-1), id = None):
        if id == None:
            r,c = loc
            id = self.matrix[r][c]
        return self.pieces[id]
        
class SBP():

    EMPTY = 0
    
    dirs = {'u': Compass.UP, 'd': Compass.DOWN, 'r': Compass.RIGHT, 'l': Compass.LEFT}
    
    def __init__(self, problem, goal):
        self.length = 7
        self.popsize = 100
        self.sol = None
        self.zero = SBP.findzeros(problem)
        self.board = Board(problem, SBP.getPieces(problem))
        self.goal = goal
        self.gb = SBP.getgoal(goal)

    def generate(self, mutate=True, chance = 0.05):
        self.max = True
        self.solve(mutate=mutate, chance=chance, maximize = True)
                
    def solve(self, mutate=False, chance=0.05, maximize = False):
        self.mutate = mutate
        self.found = False
        self.pop = self.getpop(self.board, self.length, self.popsize)
        self.sel = self.select(max = maximize)
        self.chance = chance
        if debug:
            print("END INITIAL POPULATION")
        avg = []
        i=0
        self.lastavg = None
        self.curravg = None
        self.inc = 0
        while self.keepgoing():
            self.pop = self.crossover(self.sel)
            self.lastsel = self.sel
            self.sel = self.select(max=maximize)
            self.lastavg = self.curravg
            self.curravg = getavg(self.sel)
            if debug:
                print("END GENERATION " + str(i))
                print("WITH POP AVERAGE: " + str(getavg(self.pop)))
                print("WITH ELITE AVERAGE: " + str(self.curravg))
            i+=1
        self.sol = Sequence("bad", float("inf"), "bad", "bad")
        c = 0
        for el in self.sel:
            if el.score < self.sol.score:
                self.sol = el
            elif el.score == self.sol.score and el.solpos<self.sol.solpos:
                self.sol = el
            c += 1

        self.solved = self.sol.solpos+1 != 0

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
        if not self.found:
            if self.lastavg != None and self. curravg != None and self.favours(self.lastavg,self.curravg):
                print("AVERAGE INCREASED")
                """
                for item in self.sel:
                    seeseqs(self.sel)
                for item in self.lastsel:
                    seeseqs(self.sel)
                """
                return False
            if self.curravg == self.lastavg:
                self.inc += 1
            else:
                self.inc = 0

            if self.curravg == 0:
                self.found = True
                self.inc = 0
                return True
            elif self.inc%5 == 0:
                self.extend()
                return True
            elif self.inc == 21:
                print("Halting without solution")
                return False
            return True
        else:
            self.inc += 1
            return self.inc <= 8

    def favours(self, num1, num2):
        if self.max == True:
            return num1>num2
        else:
            return num1<num2
               
    def extend(self):
        for i in range(len(self.pop)):
            self.pop[i].extend(self.getsequence(7, self.pop[i].ib, ongoingscore = self.pop[i].score))
        
    def getpop(self, ib, l, popsize):
        pop = []
        zerolist = SBP.findzeros(ib.matrix)
        score = self.manhattan(ib)
        for i in range(popsize):
            pop.append(self.getsequence(l, ib, zeros=zerolist, ongoingscore=score))
        return pop
        
    def select(self, max = False):
        if max:
            return heapq.nlargest(int(len(self.pop)/10), self.pop, key=SBP.genscore)
        best = heapq.nsmallest(int(len(self.pop)/10), self.pop, key=SBP.getscore)
        return best
        
    def getscore(seq):
        return int(seq.score*100+seq.solpos) #temporary solution -- fix later

    def genscore(seq):
        return int(seq.score)
    
    def crossover(self, select):
        crosses = []
        for mum in range(len(select)):
            for dad in range(len(select)):
                if mum != dad:
                    crosses.append(self.getchild(select[mum], select[dad]))
        crosses += select
        return crosses

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
            rand = random.random()
            if rand >= self.chance or not self.mutate: #5% chance of mutation, or not a mutate round
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

                    if (self.favours(totm,totd) and chance<0.8) or (not self.favours(totm,totd) and chance >= 0.8):
                        child.append(mum.seq[i])
                        ibalter = ibmum
                        if totm<score:
                            score=totm
                    else:
                        child.append(dad.seq[i])
                        ibalter = ibdad
                        if totd<score:
                            score=totd

                elif mumlegal:
                    adjm, ibmum, mumempty = self.applymove(mum.seq[i], ibmum)
                    totm = self.manhattan(ibmum)
                    child.append(mum.seq[i])
                    ibalter = ibmum
                    if totm<score:
                        score=totm

                elif dadlegal:
                    adjd, ibdad, dadempty = self.applymove(dad.seq[i], ibdad)
                    totd = self.manhattan(ibdad)
                    child.append(dad.seq[i])
                    ibalter = ibdad
                    if totd<score:
                        score=totd

                else:
                    move = SBP.getvalidmove(ibalter)        
                    adjd, ibalter, newempty = self.applymove(move, ibalter)
                    tot = self.manhattan(ibalter)
                    child.append(move)
                    if tot<score:
                        score=tot
            else:
                move = SBP.getvalidmove(ibalter)
                adjd, ibalter, newempty = self.applymove(move, ibalter)
                tot = self.manhattan(ibalter)
                child.append(move)
                if tot<score:
                    score=tot    
                    
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
        
    def getvalidmove(board):
        zeros = SBP.findzeros(board.matrix)
        possmoves = []
        for z in zeros:
            possmoves += SBP.getMoves(z, board)
        num = 0
        if len(possmoves)>1:
            num = random.randint(0,len(possmoves)-1)
        try:
            return possmoves[num]
        except:
            printboard(board.matrix)
            print(zeros)
            print(len(possmoves))
   
    def getMoves(z, board):
        moves = []
        rz, cz = z
        if board.matrix[rz][cz] != SBP.EMPTY:
            print("BAD!!!!")
        for k in SBP.dirs:
            r,c = SBP.add(z, SBP.dirs[k])
            if SBP.check(r,c,board) and SBP.moveable(r,c, board, SBP.dirs[k]): # check there is something in that space and it can move
                moves.append(Move(z, Compass.opp(SBP.dirs[k]), board.getpiece(loc=(r,c))))
        return moves
        
            
    def add(t1, t2):
        x,y = t1
        s,p = t2
        return (x+s, y+p)
            
    def check(r, c, board):
        return SBP.within(r, c, board) and board.matrix[r][c] != SBP.EMPTY
        
    def moveable(r,c,board, dir):
        d = board.getpiece(loc=(r,c)).dir
        if d == Dir.BOTH:
            return True
        elif dir == Compass.UP or dir == Compass.DOWN:
            return d == Dir.VERTICAL
        elif dir == Compass.RIGHT or dir == Compass.LEFT:
            return d == Dir.HORIZONTAL
        else:
            return False
        
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
            move = SBP.getvalidmove(ibalter)
            adjscore, ibalter, newempty = self.applymove(move, ibalter)
            #zeros = SBP.replace(zeros, move.empty, newempty)
            #zeros = SBP.findzeros(ibalter.matrix)
            ongoingscore = adjscore
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

    def domove(move, ib):
        if not SBP.legal(move, ib):
            print("This should not happen")
        l = move.piece.length()
        newempty = SBP.add(move.empty, SBP.times(Compass.opp(move.dir), l))
        positions = ib.getpiece(id=move.piece.id).posits
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
        return move, ib, newempty
        
    def applymove(self, move, ib):
        if not SBP.legal(move, ib):
            print("This should not happen")
        #before = self.evalscore(move.piece)
        move, ib, newempty = SBP.domove(move, ib)
        #after = self.evalscore(move.piece)
        #adj = after-before
        adj = self.manhattan(ib)
        return adj, ib, newempty
        
            
    def times(t,n):
        r,c = t
        r*=n
        c*=n
        return (r,c)            
        

class Level():
    EMPTY = 0
    def __init__(self, size, numPieces, dist):
        self.end = self.createBoard(size, numPieces)
        self.genStart(dist)

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
        return Board(board, SBP.piecesFromMatrix(board))

    def genStart(self, dist):
        self.start = self.end.copy()
        moves = []
        for num in range(dist):
            move = SBP.getvalidmove(self.start)
            move, self.start, empty = SBP.domove(move, self.start)
            moves.append(move)
        if messages:
            for move in moves:
                move.prin()
            print("-------------")
            print("Distance: " + str(len(moves)))
            print("-------------")


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

def writeboard(ib):
    string = ""
    for i in range(len(ib)):
        for j in range(len(ib[i])):
            string += str(ib[i][j]) + "\t"
        string += "\n"
    string += "\n\n"
    return string

def tilelevelstuff():
    length = 4
    dist = 15
    level1 = Level(length, length*length-1, dist)
    if messages:
        print("Start: ")
        printboard(level1.start.matrix)
        print("Goal: ")
        printboard(level1.end.matrix)
    puzzle = SBP(level1.start.matrix, level1.end.matrix)
    puzzle.solve(mutate=True)
    sollen = puzzle.sol.solpos+1
    if puzzle.sol == None:
        print(str(puzzle.pop[0].seq))
    else:
        print("score " + str(puzzle.sol.score) + " and solution length " + str(puzzle.sol.solpos+1))
        if messages:
            puzzle.sol.show()
    if sollen != 0:
        visualize(puzzle)
        if sollen <= dist and messages:
            print("Well done!")

def compareDifficulty(dist, f):
    print("Running with distance: " + str(dist))
    length = 4
    level1 = Level(length, length*length-1, dist)
    
    puzzle = SBP(level1.start.matrix, level1.end.matrix)
    start = time.get_ticks()
    puzzle.solve(mutate=True)
    end = time.get_ticks()
    sollen = puzzle.sol.solpos+1

    if sollen == 0:
        sollen = None

    f.write(str(dist) + ", " + str(sollen) + ", " + str(end-start) + "\n")

    print("Length: " + str(sollen))
    print("Took "  + str(end-start) + " ms to find solution")

def compareMutate(f):
    
    length = 4
    dist = 25
    level1 = Level(length, length*length-1, dist)
    
    puzzle = SBP(level1.start.matrix, level1.end.matrix)
    start1 = time.get_ticks()
    puzzle.solve()
    end1 = time.get_ticks()
    sollen = puzzle.sol.solpos+1
    
    puzzle2 = SBP(level1.start.matrix, level1.end.matrix)
    start2 = time.get_ticks()
    puzzle.solve(mutate=True)
    end2 = time.get_ticks()
    sollenm = puzzle.sol.solpos+1

    if sollen == 0:
        sollen = None
    if sollenm == 0:
        sollenm = None
    
    f.write(str(end1-start1) + ", " + str(sollen) + ", " + str(end2-start2) + ", " + str(sollenm) + "\n")

    

    print("w/o mutate: " + str(end1-start1) + " ms\t" + str(sollen) + " moves")
    print("w/ mutate: " + str(end2-start2) + " ms\t" + str(sollenm) + " moves")

class Visual():
    BLACK = 0,0,0
    WHITE = 255,255,255
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.board = puzzle.board.copy()
        self.length = len(puzzle.board.matrix)
        pygame.init()
        size = 700, 300
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(Visual.WHITE)
        pygame.display.flip()
        self.pieceIms = Visual.generateIms(puzzle.board.pieces)
        self.col = Visual.BLACK

    def generateIms(pieces):
        ims = {}
        myfont = pygame.font.SysFont('Arial', 30)
        for id in pieces:
            color = np.random.choice(range(256), size=3)
            ims[id] = myfont.render(str(id), False, color)
        return ims

    def drawGoal(self):
        w,h = 40,40
        y = 50
        startx = self.length*w+3*y
        for i in range(self.length):
            x = startx
            for j in range(self.length):
                id = self.puzzle.goal[i][j]
                pygame.draw.rect(self.screen, Visual.BLACK, [x, y, w, h], 2)
                if id != 0:
                    self.screen.blit(self.pieceIms[id], (x+4,y+4))
                x += w
            y += h

    def drawBoard(self):
        w,h = 40,40
        y = 50
        for i in range(self.length):
            x = 50
            for j in range(self.length): 
                pygame.draw.rect(self.screen, self.col, [x, y, w, h], 2)
                x += w
            y += h

    def drawPieces(self):
        w,h = 40,40
        y = 50
        for i in range(self.length):
            x = 50
            for j in range(self.length):
                id = self.board.matrix[i][j]
                if id != 0:
                    self.screen.blit(self.pieceIms[id], (x+4,y+4))
                x += w
            y += h

    def drawState(self):
        self.screen.fill(Visual.WHITE)
        self.drawBoard()
        self.drawPieces()
        self.drawGoal()
        pygame.display.flip()

    def changeColor(self, color):
        self.col = color

def visualize(puzzle):
    vis = Visual(puzzle)
    GREEN = 0, 255, 0
    if messages:
        print("VISUAL")
        print("-----------------")

    start = pygame.time.get_ticks()
    i=0
    j=0
    done = False
    while not done:
        if i % 500000 == 0 and j<=puzzle.sol.solpos:
            move, vis.board, empty = SBP.domove(puzzle.sol.seq[j], vis.board)
            if messages:
                print(puzzle.sol.seq[j].describe)
            j+=1
            vis.drawState()
        elif j == puzzle.sol.solpos+1:
            vis.changeColor(GREEN)
            vis.drawState()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        i+=1
    pygame.quit()
    
    
if __name__ == "__main__":
    #test()
    tilelevelstuff()
    """
    pygame.init()
    with open("mutatedistcomp2.csv", 'a+') as f:
        f.write("dist, moves, time\n")
        for i in range(10, 100, 10):
            for j in range(3):
                compareDifficulty(i, f)
            print("\n")
"""
