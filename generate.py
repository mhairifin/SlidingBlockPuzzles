import genetic as gen

import random

size = 6

available = []

twoslots = []

totpieces = 16

empty = []

final = [[0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0]]

def generateAvailable():
    for i in range(1, 13):
        available.append((i, 2))
    for j in range(13, 17):
        available.append((j, 3))

def genSlots():
    for i in range(0, size*(size-1)*2):
        twoslots.append(i)

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

        del twoslots[convertPosToSlot((2,x1), (2,x2))]

        # put on piece, generate level, check if solvable, repeat

        while(len(twoslots)>0):
        
            count+=1

            print("ADDING PIECE: " + str(count))

            r = random.randint(0,len(twoslots)-1)
        
            potSlot = twoslots[r]

            pos1, pos2 = convertSlotToPos(potSlot)

            x1, y1 = pos1
            x2, y2 = pos2

                    
            try:

                if board[x1][y1] != 0 or board[x2][y2] != 0:
                    #print("ADD FAILED")
                    count -= 1
                    del twoslots[r]
                    continue
            

                if potSlot < 30:
                    hor += 1
                else:
                    ver += 1
                board[x1][y1] = count
                board[x2][y2] = count

                puzzle = gen.SBP(board, final)
                puzzle.solve(mutate=True)

                if not puzzle.solved:
                    repeat += 1
                    if repeat >= 5:
                        board[x1][y1] = 0
                        board[x2][y2] = 0
                        return board
                    else:
                        board[x1][y1] = 0
                        board[x2][y2] = 0
                        print("H: " + str(hor))
                        print("V: " + str(ver))
                        del twoslots[r]
                        print(repeat)
                        continue
                else:
                    repeat = 0
                    gen.printboard(board)
                    del twoslots[r]
            except:
                print(twoslots)
                print(potSlot)
                print("x: " + str(x1) + " y: " + str(y1))
                print("x: " + str(x2) + " y: " + str(y2))
                return board
        return board

if __name__ == "__main__":
    with open("boards2", "w+") as f:
        for i in range(50):
            generateAvailable()
            genSlots()
            level = GeneticLevel(available)
            puzzle = gen.SBP(level.end, final)
            puzzle.solve(mutate=True)
            f.write(str(puzzle.solved) + "\n" + str(puzzle.sol.solpos+1) + "\n")
            f.write(gen.writeboard(level.end))
            
    
        
        

        
        
                     

        
        

        

        

         
        
        
        
