import sbp.genetic as gen
import copy
import sys

final = [[0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0]]


# returns a list of moves that solves the puzzle
# from a Sequence object
def confine(sequence):
    return sequence.seq[:sequence.solpos+1]

# Applies a sequence in reverse to a board
# counts how many moves are invalid
# these moves are dependent
def dependents(seq, board):
    count = 0
    for move in reversed(seq):
        if gen.SBP.legal(move, board):
            move, board, empty = gen.SBP.domove(move, board)
        else:
            count += 1
    if len(seq) != 0:
        return count/len(seq)*10
    else:
        return 10

# counts how many different pieces are used in a solution
# this is the variety of the moves
def variety(seq):
    pieces = set()
    for move in seq:
        if move.piece.id not in pieces:
            pieces.add(move.piece.id)
    if len(seq) != 0:
        return len(pieces)/len(seq)*10
    else:
        return 10

# need to define some ideal weighting
# possibly based on ranking of existing rush hour puzzles
def evaluate(sequence, board):
    solution = confine(sequence)
    deps = dependents(solution, gen.Board(board))
    var = variety(solution)
    length = len(solution)

    return (deps, var, length)

def readin(filename):
    boards = []
    with open(filename, "r+") as f:
        board = []
        for line in f:
            if len(board) == 6:
                boards.append(copy.deepcopy(board))
                board = []
            things = line.split()
            if len(things) > 1:
                row = []
                for p in things:
                    row.append(int(p))
                board.append(row)
    return boards

if __name__ == "__main__":
    name = sys.argv[1]
    boards = readin(name)
    max = 0
    top = []
    with open(name+"_limited_bands", "w+") as f, open(name+"_limited_scores", "w+") as scores:
        i = 1
        for board in boards:
            if i%5 == 0:
                break
            print("Board "+ str(i))
            puzzle = gen.SBP(board, final)
            puzzle.solve(mutate=True)
            print("Solved")
            deps, var, length = evaluate(puzzle.sol, board)
            score = 1*deps+1*var+0.3*length
            if score > max:
                max = score
                top = board
            f.write(str(deps)+", "+str(var)+", "+str(length)+"\n")
            scores.write(str(i)+", " +str(deps)+", "+str(var)+", "+str(length)+", "+str(score)+"\n")
            f.write(str(score)+"\n")
            f.write(gen.writeboard(board))
            i += 1

    print(top)
    print(max)
