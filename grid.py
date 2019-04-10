import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import genetic as gen

import sys
from evaluate import readin

boards = readin(sys.argv[1])
num = int(sys.argv[2])

grid = boards[num]
r = [0]*8
padded=[]
for i in range(8):
    padded.append(list(r))

print(grid)

num = 3

pieces = {}
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

print(pieces)

padded[3][7]=1

print(padded)

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

fig = plt.matshow(padded, cmap=cmap)
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
plt.gca()
plt.show()
