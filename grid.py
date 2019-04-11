import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import genetic as gen
import evaluate as evl

from copy import deepcopy

import sys
from evaluate import readin

from  matplotlib.animation import FuncAnimation

final = [[0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0]]


boards = readin(sys.argv[1])
num = int(sys.argv[2])

grid = deepcopy(boards[num])

pieces = {}

def toBoard(grid):
    r = [0]*8
    padded=[]
    for i in range(8):
        padded.append(list(r))

    num = 3
    
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == 0 or grid[row][col] == 1:
                padded[row+1][col+1] = grid[row][col]+1
                pieces[grid[row][col]] = grid[row][col]+1
            elif grid[row][col] not in pieces:
                pieces[grid[row][col]] = num
                padded[row+1][col+1] = num
                num += 1
            else:
                padded[row+1][col+1] = pieces[grid[row][col]]
    padded[3][7]=1
    return padded

padded = toBoard(grid)

colors = ['#363737', #dark grey
          '#d8dcd6', #grey
          '#e50000', #red
          '#ff81c0',#salmon
          '#75bbfd',#sky blue
          '#aaff32', #lime
          '#6e750e', #olive
          '#80f9ad', #seafoam
          '#887191', #greyish purple
          '#3d0734', #aubergine
          '#a24857', #light maroon
          '#005249', #dark blue green
          '#ff7855', #melon
          '#fb7d07', #pumpkin orange
          '#1f0954', #dark indigo
          '#f5bf03', #golden
          '#8b3103', #rust brown
          '#1d5dec' #azul
]

cmap=ListedColormap(colors[:len(pieces)+1])

fig = plt.figure()
ax = plt.axes()
plot = ax.matshow(padded, cmap=cmap)
#plot.axes.get_xaxis().set_visible(False)
#plot.axes.get_yaxis().set_visible(False)
ax.set_axis_off()
plt.gca()

puzzle = gen.SBP(grid, final)
puzzle.solve(mutate=True)
moves = evl.confine(puzzle.sol)
n_frames = len(moves)+4

def getFromPadded(g, padded):
    for row in range(0, len(grid)):
        for col in range(0, len(grid)):
            g[row][col] = padded[row+1][col+1]-1
    return g

def init():
    plot.set_data(padded)
    return [plot]

def update(j):
    global grid
    n = j%(len(moves)+4)
    if n == 0:
        grid = deepcopy(boards[num])
        return init()
    elif n == len(moves)+1:
        pad = toBoard(grid)
        pad[3][5] = 1
        pad[3][7] = 2
        plot.set_data(pad)
    elif n == len(moves)+2:
        pad = toBoard(grid)
        pad[3][5] = 1
        pad[3][6] = 1
        pad[3][7] = 2
        plot.set_data(pad)
    elif n == len(moves)+3:
        pad = toBoard(grid)
        pad[3][5] = 1
        pad[3][6] = 1
        pad[3][7] = 1
        plot.set_data(pad)
    else:
        move, g, empty = gen.SBP.domove(moves[n-1], gen.Board(grid))
        grid = g.matrix
        plot.set_data(toBoard(grid))
    return [plot]

anim = FuncAnimation(fig, update, init_func = init, frames = n_frames, interval=300, blit=True, repeat=True)

plt.show()
