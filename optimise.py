data = []
with open("originalBoards_limited_scores") as read:
    for line in read:
        els = line.split(", ")
        data.append((int(els[0]), float(els[1]), float(els[2]), int(els[3].strip())))

def getscore(item):
    return item[1]

def evaluate(l, print=False):
    l.sort(key=getscore)

    diff = 0
    for num in range(len(l)):
        diff += abs(l[num][0] - (num+1))
    return diff, l

lowest = float("inf")
li = 0
lj = 0
lk = 0
thing = None
for i in range(0, 100, 1):
    for j in range(0, 100, 1):
        for k in range(0, 100, 1):
            intermed = []
            for item in data:
                id, deps, var, length = item
                if deps == 10 and var == 10 and length == 0:
                    continue
                score = i*deps+j*var+k*length
                intermed.append((id, score))
            diff, order = evaluate(intermed)
            if diff<lowest and not (i == 0 and j == 0 and k == 0):
                lowest = diff
                li = i
                lj = j
                lk = k
                thing = order
print(str(li) + ", " + str(lj) + ", " + str(lk))
print(lowest)
print(thing)
