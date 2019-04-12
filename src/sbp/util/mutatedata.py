from pygame import time
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import sbp.genetic as gen

if __name__ == "__main__":
    length=4
    dist = 25
    pygame.init()

    with open("mutatedatamore.csv", "w+") as f:
        f.write("Mutation chance(%), Time, Solution Length, Solution Found?\n")
        for i in range(0, 20):
            level = gen.Level(length, length*length-1, dist)
            for j in range(4, 20):
                puzzle = gen.SBP(level.start.matrix, level.end.matrix)
                start1 = time.get_ticks()
                puzzle.solve(mutate=True, chance = 0.01*j)
                end1 = time.get_ticks()
                sollen = puzzle.sol.solpos+1

                timetaken = end1-start1

                f.write(str(j) + ", " + str(timetaken) + ", " + str(sollen) + ", " + str(sollen!=0) + "\n")

        
    
