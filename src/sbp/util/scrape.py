from requests import get
from contextlib import closing

import re
import sbp.genetic as gen

def simple_get(url):
    with closing(get(url, stream=True)) as resp:
        return str(resp.content)

if __name__ == "__main__":
    boards = []
    for i in range(1, 41):
        board = []
        for c in range(6):
            row = []
            for r in range(6):
                row.append(0)
            board.append(row)
        content = simple_get(f"http://www.puzzles.com/products/rushhour/rhfrommarkriedel/jam{i}.js")
        cars = re.findall(r'([red]*)car(EW|NS).gif\",\(fTop\+(\d+)\*72\),\(fLeft\+(\d+)\*72\)', content)
        lorries = re.findall(r'lorry(EW|NS).gif",\(fTop\+(\d+)\*72\),\(fLeft\+(\d+)\*72\)', content)
        count = 2
        for car in cars:
            red, dir, r, c = car
            id = count
            if red == 'red':
                count -= 1
                id = 1
            board[int(r)][int(c)] = id
            if dir == 'NS':
                board[int(r)+1][int(c)] = id
            else:
                board[int(r)][int(c)+1] = id
            count+=1
        for lorry in lorries:
            dir, r, c = lorry
            id = count
            board[int(r)][int(c)] = id
            if dir == 'NS':
                board[int(r)+1][int(c)] = id
                board[int(r)+2][int(c)] = id
            else:
                board[int(r)][int(c)+1] = id
                board[int(r)][int(c)+2] = id
            count+=1
            
        gen.printboard(board)
    
