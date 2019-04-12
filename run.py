import genetic as gen
import generate as create
import evaluate as evl
from evaluate import readin

import subprocess
import argparse

desc = """ This is a command line tool for solving, generating, and evaluating sliding block puzzles. 
The order of evaluation scores is: Board Number, Dependency, Variety, Length, Total Score 
"""

def runGenetic(src, anim, final, nomut):
    boards = readin(src)
    if final == None:
        final = [[0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,1,1],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0]]
    else:
        final = readin(final)[0]
    if not anim:
        for i in range(len(boards)):
            puzzle = gen.SBP(boards[i], final)
            puzzle.solve(mutate = (not nomut))
            print(f"Board {i+1}")
            if puzzle.solved:
                for move in evl.confine(puzzle.sol):
                    move.prin()
                else:
                    print("Could not solve")
            print("\n")
    else:
        subprocess.run(['python','grid.py', src, '0'])
        

def runGenerate(dest, generator, number):
    mapToFuncs = {"Random": create.Random, "Incremental": create.Incremental, "ImprovedIncremental": create.ImprovedIncremental, "Genetic": create.Maximize}
    with open(dest, "a+") as f:
        for i in range(number):
            print(f"Generating Board {i+1}")
            level = mapToFuncs[generator]()
            f.write(gen.writeboard(level.end))

def runEvaluate(src, dest, final):
    if final == None:
        final = [[0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,1,1],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0]]
    else:
        final = readin(final)[0]
    boards = readin(src)
    with open(dest, "a+") as scores:
        i = 1
        for board in boards:
            print("Analyzing board "+ str(i))
            puzzle = gen.SBP(board, final)
            puzzle.solve(mutate=True)
            deps, var, length = evl.evaluate(puzzle.sol, board)
            score = 1*deps+1*var+0.3*length
            scores.write(str(i)+", "
                         +str(deps)+", "
                         +str(var)+", "
                         +str(length)+", "
                         +str(score)+"\n")
            i += 1



parser = argparse.ArgumentParser(description="working")
parser.add_argument('action', help="solve, generate, or evaluate (s, g, or e)")
parser.add_argument("-a", "--animate", action='store_true', help="Animate solution found with solver")
parser.add_argument("-s", "--sourcefile", type=str, help="Source file for board to solve, or boards to evaluate")
parser.add_argument("-d", "--destfile", type=str, help="Destination file for generated boards or generated evaluation scores - appends to destination file if it already exists")
parser.add_argument("-f", "--final", type=str, help="File containing the final board for the solver to use. Otherwise, will use Rush Hour final board")
parser.add_argument("-n", "--nomutate", action='store_true', help="Turns OFF mutation for the solver")
parser.add_argument ("-g", "--generator", help="Type of generator: Random, Incremental, ImprovedIncremental, Genetic", default="ImprovedIncremental")
parser.add_argument("-i", "--number", type=int, help="Number of puzzles to generate", default=1)

args=parser.parse_args()

if args.action == 's' or args.action=='solve':
    runGenetic(args.sourcefile, args.animate, args.final, args.nomutate)
elif args.action == 'g' or args.action=='generate':
    runGenerate(args.destfile, args.generator, args.number)
elif args.action == 'e' or args.action == 'evaluate':
    runEvaluate(args.sourcefile, args.destfile, args.final)
