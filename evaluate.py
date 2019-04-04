import genetic as gen
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
    print(deps)
    var = variety(solution)
    print(var)
    length = len(solution)
    print(length)

    return deps+var+.3*length

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
    with open(name+"_scores", "w+") as f:
        for board in boards:
            print("Next Board")
            puzzle = gen.SBP(board, final)
            puzzle.solve(mutate=True)
            score = evaluate(puzzle.sol, board)
            if score > max:
                max = score
                top = board
            f.write(str(score)+"\n")
            f.write(gen.writeboard(board))

    print(top)
    print(max)    

