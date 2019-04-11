"""
Collects boards with interesting scores
"""

import sys

def _collect(board_file, threshold):
    with open(board_file + "_best", "w+") as w, open(board_file, "r+") as r:
        collect = False
        for line in r:
            elements = line.split()
            if len(elements) == 1:
                score = float(elements[0])
                if score>=threshold or score==0:
                    w.write(str(score) + "\n")
                    for i in range(6):
                        w.write(r.readline())
                    w.write("\n")
    

def collect_unadjusted(board_file):
    """
    threshold for interesting seems to be around 15
    """
    _collect(board_file, 15)                

def collect_adjusted(board_file):
    _collect(board_file, 15)

if __name__ == "__main__":
    collect_adjusted(sys.argv[1])
