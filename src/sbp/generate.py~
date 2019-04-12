import genetic as gen

import random

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame import time

import sys

size = 6

available = []

twoslots = []
threeslots = []

totpieces = 16

empty = []

final = [[0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0]]

def generateAvailable():
    available = []
    for i in range(2, 13):
        available.append((i, 2))
    for j in range(13, 17):
        available.append((j, 3))
    return available

def genSlots():
    twoslots = []
    threeslots = []
    for i in range(0, size*(size-1)*2):
        twoslots.append(i)
    for i in range(0, size):
        for j in range(0, size-2):
            threeslots.append(((i,j),(i, j+1),(i, j+2)))
            threeslots.append(((j, i), (j+1, i), (j+2, i)))
    return (twoslots, threeslots)

def convertPosToSlot(pos1,pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    if x1 == x2:
        return x1*(size-1)+y1
    else:
        return 30+x1*size+y1

def convertSlotToPos(num):
    if num >= 30:
        num -= 30
        row2 = int(num/size)
        col = num%size
        return ((row2, col), (row2+1, col))
    else:
        row = int(num/(size-1))
        col1 = num%(size-1)
        return((row, col1), (row, col1+1))

class Random():
    EMPTY = 0
    def __init__(self):
        self.available = generateAvailable()
        self.twoslots, self.threeslots = genSlots()
        self.end = self.constructBoard()

    def constructBoard(self, shuffle=1000):
        self.start = startRandom(self.available, self.twoslots, self.threeslots)
        return Random.shuffleBoard(self.start)
        
    def shuffleBoard(matrix, shuffle = 100):
        board = gen.Board(matrix, gen.SBP.piecesFromMatrix(matrix))
        moves = []
        for num in range(shuffle):
            move=gen.SBP.getvalidmove(board)
            move, board, empty = gen.SBP.domove(move, board)
            moves.append(move)
        return board.matrix
        
        
    def create15Board(self, size, numPieces):
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

def startRandom(available, twoslots, threeslots):
    board = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        board.append(row)

    # solveable board
    board[2][4] = 1
    board[2][5] = 1

    while len(available)>0:
        p = random.randrange(len(available))
        id, s = available[p]

        del available[p]

        if s==2 and len(twoslots)>0:
            r = random.randrange(len(twoslots))
            potSlot = twoslots[r]

            pos1, pos2 = convertSlotToPos(potSlot)

            x1, y1 = pos1
            x2, y2 = pos2        
            if board[x1][y1] != 0 or board[x2][y2] != 0:
                del twoslots[r]
                continue
            board[x1][y1] = id
            board[x2][y2] = id
        elif s==3 and len(threeslots)>0:
            r = random.randrange(len(threeslots))
            pos1, pos2, pos3 = threeslots[r]
            x1, y1 = pos1
            x2, y2 = pos2
            x3, y3 = pos3
            if board[x1][y1] != 0 or board[x2][y2] != 0 or board[x3][y3] != 0:
                del threeslots[r]
                continue
            board[x1][y1] = id
            board[x2][y2] = id
            board[x3][y3] = id
        else:
            return board
    return board
    

class Maximize():
    def __init__(self):
        self.available = generateAvailable()
        self.twoslots, self.threeslots = genSlots()
        self.end = self.constructBoard()

    def constructBoard(self):
        board = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(0)
            board.append(row)

        # solveable board
        board[2][4] = 1
        board[2][5] = 1

        while len(self.available)>0:
            p = random.randrange(len(self.available))
            id, s = self.available[p]

            del self.available[p]

            if s==2 and len(self.twoslots)>0:
                r = random.randrange(len(self.twoslots))
                potSlot = self.twoslots[r]

                pos1, pos2 = convertSlotToPos(potSlot)

                x1, y1 = pos1
                x2, y2 = pos2
                
                if board[x1][y1] != 0 or board[x2][y2] != 0:
                    del self.twoslots[r]
                    continue
                board[x1][y1] = id
                board[x2][y2] = id
            elif s==3 and len(self.threeslots)>0:
                r = random.randrange(len(self.threeslots))
                pos1, pos2, pos3 = self.threeslots[r]
                x1, y1 = pos1
                x2, y2 = pos2
                x3, y3 = pos3
                if board[x1][y1] != 0 or board[x2][y2] != 0 or board[x3][y3] != 0:
                    del self.threeslots[r]
                    continue
                board[x1][y1] = id
                board[x2][y2] = id
                board[x3][y3] = id
            else:
                break

        level = gen.SBP(board, board)
        level.generate()

        permute = level.sol.seq[:level.sol.solpos+1]
        final = []
        for move in permute:
            move, b, empty = gen.SBP.domove(move, gen.Board(board))
            final = b.matrix
        return final

class ImprovedIncremental():
    def __init__(self):
        self.available = generateAvailable()
        self.twoslots, self.threeslots = genSlots()
        self.end = self.constructBoard()

    def constructBoard(self):
        repeat = 0
        count = 1

        hor = 0
        ver = 0
        
        board = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(0)
            board.append(row)

        # make sure it is not trivially solvable, and is in the right row
        poss = [(0,1), (2,3), (2,3), (3,4)]
        rand = random.randint(0,3)
        r1, r2 = poss[rand]
        board[2][r1] = 1
        board[2][r2] = 1

        del self.twoslots[convertPosToSlot((2,r1), (2,r2))]

        # put on piece, generate level, check if solvable, repeat

        while(len(self.available)>0):
        
            count+=1

            print("ROUND: " + str(count))

            p = random.randrange(len(self.available))
            id, s = self.available[p]

            del self.available[p]

            r = 0
            potslot = 0
            if s == 2 and len(self.twoslots)>0:
                poss = []
                for i in range(5):
                    r = random.randrange(len(self.twoslots))
                    poss.append(r)

                bucket = []
                for item in poss:
                    potSlot = self.twoslots[item]

                    pos1, pos2 = convertSlotToPos(potSlot)

                    x1, y1 = pos1
                    x2, y2 = pos2

                    bucket.append((pos1, pos2, item))

                    if self.checkadjacent([pos1, pos2], board):
                        bucket.append((pos1, pos2, item))
                        
                    if self.inway([pos1, pos2], r1, r2):
                        bucket.append((pos1, pos2, item))
                        
                select = random.randrange(len(bucket))
                pos1, pos2, r = bucket[select]
                x1, y1 = pos1
                x2, y2 = pos2
                        

                try:
                    if board[x1][y1] != 0 or board[x2][y2] != 0:
                        del self.twoslots[r]
                        continue
                    board[x1][y1] = id
                    board[x2][y2] = id

                    puzzle = gen.SBP(board, final)
                    puzzle.solve(mutate=True)

                    if not puzzle.solved:
                        self.available.append((id, s))
                        repeat += 1
                        if repeat >= 5:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            #print("stopped here")
                            return board
                        else:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            del self.twoslots[r]
                            continue
                    else:
                        #gen.printboard(board)
                        del self.twoslots[r]
                except:
                    gen.printboard(board)
                    sys.exit(0)

            
            elif s == 3 and len(self.threeslots)>0:
                poss = []
                for i in range(5):
                    r = random.randrange(len(self.threeslots))
                    poss.append(r)

                bucket = []
                for item in poss:
                    pos1, pos2, pos3 = self.threeslots[item]
                    bucket.append((pos1, pos2, pos3, item))
                    
                    if self.checkadjacent([pos1, pos2, pos3], board):
                        bucket.append((pos1, pos2, pos3, item))

                    if self.inway([pos1, pos2, pos3], r1, r2):
                        bucket.append((pos1, pos2, pos3, item))

                select = random.randrange(len(bucket))
                pos1, pos2, pos3, r = bucket[select]
                x1, y1 = pos1
                x2, y2 = pos2
                x3, y3 = pos3
                    
                try:
                    if board[x1][y1] != 0 or board[x2][y2] != 0 or board[x3][y3] != 0:
                        del self.threeslots[r]
                        continue
                    board[x1][y1] = id
                    board[x2][y2] = id
                    board[x3][y3] = id

                    puzzle = gen.SBP(board, final)
                    puzzle.solve(mutate=True)

                    if not puzzle.solved:
                        self.available.append((id, s))
                        repeat += 1
                        if repeat >= 5:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            board[x3][y3] = 0
                            #print("ended here")
                            return board
                        else:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            board[x3][y3] = 0
                            del self.threeslots[r]
                            continue
                    else:
                        del self.threeslots[r]
                        
                except:
                    gen.printboard(board)
                    sys.exit(0)
                    print(self.threeslots)
                    print("SOMETHING WENT WRONG IN THREESLOT")
            else:
                break
        print("finished naturally")
        return board

    def checkadjacent(self, positions, board):
        for pos in positions:
            x, y = pos
            surrounds = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for r, c in surrounds:
                if self.inbounds(r,c,len(board)) and board[r][c] != 0:
                    return True
        return False

    def inbounds(self, x, y, size):
        return x>= 0 and x<size and y>=0 and y<size

    def inway(self, positions, r1, r2):
        for pos in positions:
            r,c = pos
            if r == 2 and c > r2:
                return True
        return False

    
        

class Incremental():
    def __init__(self):
        self.available = generateAvailable()
        self.twoslots, self.threeslots = genSlots()
        self.randomize = shuffle
        self.end = self.constructBoard()

    def constructBoard(self):
        repeat = 0
        count = 1

        hor = 0
        ver = 0
        
        board = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(0)
            board.append(row)

        # make sure it is not trivially solvable, and is in the right row
        poss = [(0,1), (2,3), (2,3), (3,4)]
        rand = random.randint(0,3)
        x1, x2 = poss[rand]
        board[2][x1] = 1
        board[2][x2] = 1

        del self.twoslots[convertPosToSlot((2,x1), (2,x2))]

        # put on piece, generate level, check if solvable, repeat

        while(len(self.available)>0):
        
            count+=1

            print("ROUND: " + str(count))

            p = random.randrange(len(self.available))
            id, s = self.available[p]

            del self.available[p]

            r = 0
            potslot = 0
            if s == 2 and len(self.twoslots)>0:
                r = random.randrange(len(self.twoslots))
                potSlot = self.twoslots[r]

                pos1, pos2 = convertSlotToPos(potSlot)

                x1, y1 = pos1
                x2, y2 = pos2

                try:
                    if board[x1][y1] != 0 or board[x2][y2] != 0:
                        del self.twoslots[r]
                        continue
                    board[x1][y1] = id
                    board[x2][y2] = id

                    puzzle = gen.SBP(board, final)
                    puzzle.solve(mutate=True)

                    if not puzzle.solved:
                        self.available.append((id, s))
                        repeat += 1
                        if repeat >= 5:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            return board
                        else:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            del self.twoslots[r]
                            continue
                    else:
                        gen.printboard(board)
                        del self.twoslots[r]
                except:
                    gen.printboard(board)
                    print(self.twoslots)
                    print("SOMETHING WENT WRONG IN TWOSLOT")

            
            elif s == 3 and len(self.threeslots)>0:
                r = random.randrange(len(self.threeslots))
                pos1, pos2, pos3 = self.threeslots[r]
                x1, y1 = pos1
                x2, y2 = pos2
                x3, y3 = pos3
                try:
                    if board[x1][y1] != 0 or board[x2][y2] != 0 or board[x3][y3] != 0:
                        del self.threeslots[r]
                        continue
                    board[x1][y1] = id
                    board[x2][y2] = id
                    board[x3][y3] = id

                    puzzle = gen.SBP(board, final)
                    puzzle.solve(mutate=True)

                    if not puzzle.solved:
                        self.available.append((id, s))
                        repeat += 1
                        if repeat >= 5:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            board[x3][y3] = 0
                            return board
                        else:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            board[x3][y3] = 0
                            del self.threeslots[r]
                            continue
                    else:
                        del self.threeslots[r]
                        
                except:
                    gen.printboard(board)
                    print(self.threeslots)
                    print("SOMETHING WENT WRONG IN THREESLOT")
            else:
                break

        if self.randomize:
            return Random.shuffleBoard(board)
        return board

if __name__ == "__main__":
    generator = sys.argv[1]
    number = int(sys.argv[2])
    place = sys.argv[3]

    pygame.init()
    
    with open(place, "w+") as f:
        for i in range(number):
            print(f"Generating Board {i+1}")
            start = time.get_ticks()
            level = globals()[generator]()
            end = time.get_ticks()
            puzzle = gen.SBP(level.end, final)
            timetaken = end-start
            print(timetaken)
            f.write(str(timetaken) + "\n")
            f.write(gen.writeboard(level.end))
    """
    with open("100boardsGenetic", "w+") as f:
        for i in range(100):
            generateAvailable()
            genSlots()
            level = Maximize(available)
            gen.printboard(level.end)
            puzzle = gen.SBP(level.end, final)
            puzzle.solve(mutate=True)
            f.write(str(puzzle.solved) + "\n" + str(puzzle.sol.solpos+1) + "\n")
            f.write(gen.writeboard(level.end))
    """
    """
    generateAvailable()
    genSlots()
    level=Maximize(available)
    puzzle = gen.SBP(level.end, final)
    gen.basicVisualise(puzzle)
    """
    """
    pygame.init()
    
    with open("40ImprovedIncremental", "w+") as f:
        for i in range(40):
            print(i)
            start = time.get_ticks()
            level = globals()[generator]()
            end = time.get_ticks()
            puzzle = gen.SBP(level.end, final)
            timetaken = end-start
            print(timetaken)
            f.write(str(timetaken) + "\n")
            f.write(gen.writeboard(level.end))        
      """

        
        
                     

        
        

        

        

         
        
        
        
