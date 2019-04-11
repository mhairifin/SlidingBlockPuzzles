"""
Data collection on the difficulty of randomly generated 15-puzzles
and comparison of mutation values for randomly generated 15-puzzle levels
"""

from sbp.generate import Level

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
