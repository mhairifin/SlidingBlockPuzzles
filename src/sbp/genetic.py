"""
Contains a genetic algorithm for solving sliding block puzzles
"""

import random
import heapq
import copy
import statistics as stats
from enum import Enum
import sys, pygame
from pygame import time
import numpy as np
import math

debug = False
messages = False

def getavg(select):
    tot = 0
    for i in select:
        tot+=i.score
    return tot/len(select)

"""
Directions for pieces
"""
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

"""
Representation of a board
"""
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

"""
Representation of a sliding block puzzle to be solved
"""
class SBP():

    EMPTY = 0
    
    dirs = {'u': Compass.UP, 'd': Compass.DOWN, 'r': Compass.RIGHT, 'l': Compass.LEFT}
    
    def __init__(self, problem, goal):
        self.length = 7
        self.popsize = 49
        self.sol = None
        self.zero = SBP.findzeros(problem)
        self.board = Board(problem, SBP.getPieces(problem))
        self.goal = goal
        self.gb = SBP.getgoal(goal)
        self.max = False

    """
    Function for use by genetic generator
    """
    def generate(self, mutate=True, chance = 0.07):
        self.max = True
        self.solve(mutate=mutate, chance=chance, maximize = True)
                
    def solve(self, mutate=False, chance=0.07, maximize = False):
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

        self.gen = 0

        # number of generations is limited to 100
        while self.keepgoing() and self.gen<100:
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
            if self.max and self.inc == 3:
                self.found = True
                break;
            self.gen+=1
        comp = float("inf")
        if self.max:
            comp = 0
        self.sol = Sequence("bad", comp, "bad", "bad")
        c = 0
        for el in self.sel:
            if self.favours(el.score,self.sol.score):
                self.sol = el
            elif el.score == self.sol.score and self.favours(el.solpos,self.sol.solpos):
                self.sol = el
            c += 1

        self.solved = (self.sol.solpos + 1) != 0

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

    """
    Decides whether the alogirthm should continue based on 
    whether the average is staying consistent
    Also extends the sequence when necessary
    """
    def keepgoing(self):
        if not self.found:
            if self.lastavg != None and self.curravg != None and self.favours(self.lastavg,self.curravg):
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
            elif self.inc == 30:
                print("Halting without solution")
                return False
            return True
        else:
            self.inc += 1
            return self.inc <= 8

    def favours(self, num1, num2):
        if self.max:
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
            return heapq.nlargest(int(self.selectSize()), self.pop, key=SBP.genscore)
        best = heapq.nsmallest(int(self.selectSize()), self.pop, key=SBP.getscore)
        return best

    """
    Gets the number to select from a population to keep a consistent population size
    """
    def selectSize(self):
        return math.sqrt(self.popsize)
        
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

    """
    Crosses two sequences to obtain a third, child sequence
    """
    def getchild(self, mum, dad):
        child = []
        ibalter = self.board.copy()
        zeros = self.zero
        score = float("inf")
        if self.max:
            score = 0
        solpos = -1
        
        for i in range(len(mum.seq)):
            rand = random.random()
            if rand >= self.chance or not self.mutate: # small chance of mutation
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

                    # 80% probability of selecting the most favourable move
                    if (self.favours(totm,totd) and chance<0.8) or (not self.favours(totm,totd) and chance >= 0.8):
                        child.append(mum.seq[i])
                        ibalter = ibmum
                        if self.favours(totm,score):
                            if self.max:
                                solpos = i
                            score=totm
                    else:
                        child.append(dad.seq[i])
                        ibalter = ibdad
                        if self.favours(totd,score):
                            if self.max:
                                solpos = i
                            score=totd

                elif mumlegal:
                    adjm, ibmum, mumempty = self.applymove(mum.seq[i], ibmum)
                    totm = self.manhattan(ibmum)
                    child.append(mum.seq[i])
                    ibalter = ibmum
                    if self.favours(totm,score):
                        if self.max:
                            solpos = i
                        score=totm

                elif dadlegal:
                    adjd, ibdad, dadempty = self.applymove(dad.seq[i], ibdad)
                    totd = self.manhattan(ibdad)
                    child.append(dad.seq[i])
                    ibalter = ibdad
                    if self.favours(totd,score):
                        if self.max:
                            solpos = i
                        score=totd

                else:
                    move = SBP.getvalidmove(ibalter)        
                    adjd, ibalter, newempty = self.applymove(move, ibalter)
                    tot = self.manhattan(ibalter)
                    child.append(move)
                    if self.favours(tot,score):
                        if self.max:
                            solpos = i
                        score=tot
            else:
                move = SBP.getvalidmove(ibalter)
                adjd, ibalter, newempty = self.applymove(move, ibalter)
                tot = self.manhattan(ibalter)
                child.append(move)
                if self.favours(tot,score):
                    if self.max:
                        solpos = i
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

    """
    Gets a valid move from a board
    """
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

    """ 
    Gets all possible moves on the board from one empty spot
    """
    def getMoves(z, board):
        moves = []
        rz, cz = z
        for k in SBP.dirs:
            r,c = SBP.add(z, SBP.dirs[k])
            if SBP.check(r,c,board) and SBP.moveable(r,c, board, SBP.dirs[k]): # check there is something in that space and it can move
                moves.append(Move(z, Compass.opp(SBP.dirs[k]), board.getpiece(loc=(r,c))))
        return moves
            
    def add(t1, t2):
        x,y = t1
        s,p = t2
        return (x+s, y+p)

    """
    Checks that a placement is within bounds, and there is a piece there
    """
    def check(r, c, board):
        return SBP.within(r, c, board) and board.matrix[r][c] != SBP.EMPTY

    """
    Checks if a piece can move in a given direction
    """
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

    """
    Gets a random sequence of moves
    """
    def getsequence(self, length, board, ongoingscore = None, zeros = None):
        if zeros == None:
            zeros = SBP.findzeros(board.matrix) 
        ibalter = board.copy()
        seq = []
        score = float("inf") #arbitrarily high number
        if self.max:
            score = 0
        if ongoingscore == None:
            ongoingscore = self.manhattan(board) 
        solpos = -1;
        for i in range(length):
            move = SBP.getvalidmove(ibalter)
            adjscore, ibalter, newempty = self.applymove(move, ibalter)
            #zeros = SBP.replace(zeros, move.empty, newempty)
            #zeros = SBP.findzeros(ibalter.matrix)
            ongoingscore = adjscore
            if self.favours(ongoingscore,score):
                score = ongoingscore
            seq.append(move)
            if ongoingscore == 0 and solpos == -1:
                solpos = i
        return Sequence(seq, score, ibalter, solpos)

    """
    Gets the manhattan score of a board
    """
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

    
    
if __name__ == "__main__":
    # readin board and then print out solution
    pass
