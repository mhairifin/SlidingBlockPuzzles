import genetic as gen

import random

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
    for i in range(2, 13):
        available.append((i, 2))
    for j in range(13, 17):
        available.append((j, 3))

def genSlots():
    for i in range(0, size*(size-1)*2):
        twoslots.append(i)
    for i in range(0, size):
        for j in range(0, size-2):
            threeslots.append(((i,j),(i, j+1),(i, j+2)))
            threeslots.append(((j, i), (j+1, i), (j+2, i)))

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

class Maximize():
    def __init__(self, available):
        self.available = available
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
                break

        level = gen.SBP(board, board)
        level.generate()
        return board
        

class GeneticLevel():
    def __init__(self, available):
        self.available = available
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

        print(convertPosToSlot((2,x1), (2,x2)))
        print(twoslots)

        del twoslots[convertPosToSlot((2,x1), (2,x2))]

        # put on piece, generate level, check if solvable, repeat

        while(len(available)>0):
        
            count+=1

            print("ROUND: " + str(count))

            p = random.randrange(len(available))
            id, s = available[p]

            del available[p]

            r = 0
            potslot = 0
            if s == 2 and len(twoslots)>0:
                r = random.randrange(len(twoslots))
                potSlot = twoslots[r]

                pos1, pos2 = convertSlotToPos(potSlot)

                x1, y1 = pos1
                x2, y2 = pos2

                try:
                    if board[x1][y1] != 0 or board[x2][y2] != 0:
                        del twoslots[r]
                        continue
                    board[x1][y1] = id
                    board[x2][y2] = id

                    puzzle = gen.SBP(board, final)
                    puzzle.solve(mutate=True)

                    if not puzzle.solved:
                        available.append((id, s))
                        repeat += 1
                        if repeat >= 5:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            return board
                        else:
                            board[x1][y1] = 0
                            board[x2][y2] = 0
                            del twoslots[r]
                            continue
                    else:
                        gen.printboard(board)
                        del twoslots[r]
                except:
                    gen.printboard(board)
                    print(twoslots)
                    print("SOMETHING WENT WRONG IN TWOSLOT")

            
            elif s == 3 and len(threeslots)>0:
                r = random.randrange(len(threeslots))
                pos1, pos2, pos3 = threeslots[r]
                x1, y1 = pos1
                x2, y2 = pos2
                x3, y3 = pos3
                try:
                    if board[x1][y1] != 0 or board[x2][y2] != 0 or board[x3][y3] != 0:
                        del threeslots[r]
                        continue
                    board[x1][y1] = id
                    board[x2][y2] = id
                    board[x3][y3] = id

                    puzzle = gen.SBP(board, final)
                    puzzle.solve(mutate=True)

                    if not puzzle.solved:
                        available.append((id, s))
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
                            del threeslots[r]
                            continue
                    else:
                        del threeslots[r]
                        
                except:
                    gen.printboard(board)
                    print(threeslots)
                    print("SOMETHING WENT WRONG IN THREESLOT")
            else:
                break
        return board

if __name__ == "__main__":
    with open("boards3", "w+") as f:
        for i in range(1000):
            generateAvailable()
            genSlots()
            level = GeneticLevel(available)
            puzzle = gen.SBP(level.end, final)
            puzzle.solve(mutate=True)
            f.write(str(puzzle.solved) + "\n" + str(puzzle.sol.solpos+1) + "\n")
            f.write(gen.writeboard(level.end))
    """
    generateAvailable()
    genSlots()
    level = Maximize(available)
    gen.printboard(level.end)
    """
    
        
        

        
        
                     

        
        

        

        

         
        
        
        
