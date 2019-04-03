from pygame import time
import pygame
import genetic as gen

if __name__ == "__main__":
    length=4
    dist = 25
    pygame.init()

    with open("mutatedata3.csv", "w+") as f:
        f.write("Mutation chance(%), Time, Solution Length, Solution Found?\n")
        for i in range(0, 10):
            level = gen.Level(length, length*length-1, dist)
            for j in range(0, 50):
                print(j)
                puzzle = gen.SBP(level.start.matrix, level.end.matrix)
                start1 = time.get_ticks()
                puzzle.solve(mutate=True, chance = 0.01*j)
                end1 = time.get_ticks()
                sollen = puzzle.sol.solpos+1

                timetaken = end1-start1

                f.write(str(j) + ", " + str(timetaken) + ", " + str(sollen) + ", " + str(sollen!=0) + "\n")

        
    
