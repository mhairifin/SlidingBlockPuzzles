from genetic import *

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
