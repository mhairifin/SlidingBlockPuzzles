import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import sbp.genetic as gen
import sbp.evaluate as evl
"""
Contains class for animating sequences of moves on a board
"""


from copy import deepcopy

import sys
from sbp.evaluate import readin

from  matplotlib.animation import FuncAnimation

def toBoard(grid):
    r = [0]*8
    padded=[]
    pieces = {}
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
    return padded, pieces

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

class Animate():
    def __init__(self, board, moves):
        self.original = board
        self.grid = deepcopy(board)

        n_frames = len(moves)+4

        self.moves = moves

        self.padded, self.pieces = toBoard(self.grid)

        cmap=ListedColormap(colors[:len(self.pieces)+1])

        fig=plt.figure()
        ax = plt.axes()
        self.plot=ax.matshow(self.padded, cmap=cmap)
        ax.set_axis_off()
        plt.gca()

        anim = FuncAnimation(fig, self.update, init_func = self.start, frames = n_frames, interval=300, blit=True, repeat=True)

        plt.show()


    def start(self):
        self.plot.set_data(self.padded)
        return [self.plot]

    def update(self, j):
        n = j%(len(self.moves)+4)
        if n == 0:
            self.grid = deepcopy(self.original)
            return self.start()
        elif n == len(self.moves)+1: # these animate the piece leaving the board
            pad, p = toBoard(self.grid)
            pad[3][5] = 1
            pad[3][7] = 2
            self.plot.set_data(pad)
        elif n == len(self.moves)+2:
            pad, p = toBoard(self.grid)
            pad[3][5] = 1
            pad[3][6] = 1
            pad[3][7] = 2
            self.plot.set_data(pad)
        elif n == len(self.moves)+3:
            pad, p = toBoard(self.grid)
            pad[3][5] = 1
            pad[3][6] = 1
            pad[3][7] = 1
            self.plot.set_data(pad)
        else:
            move, g, empty = gen.SBP.domove(self.moves[n-1], gen.Board(self.grid))
            self.grid = g.matrix
            self.plot.set_data(toBoard(self.grid)[0])
        return [self.plot]
        
