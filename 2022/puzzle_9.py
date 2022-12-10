import sys

head = [0,0]
tail = [0,0]

vectors = {'R' : (1,0),
           'U' : (0,1),
           'L' : (-1,0),
           'D' : (0,-1)}

def step_tail(head, tail):
    diff = (head[0] - tail[0], head[1] - tail[1])
    if abs(diff[0]) <= 1 and abs(diff[1]) <= 1:
        return tail
    diff = [x/abs(x) if x else 0 for x in diff]
    tail[0] += diff[0]
    tail[1] += diff[1]
    return tail

tails = set()

with open(sys.argv[1],'r') as file:
    for line in file:
        cmd, num = line.strip().split()
        vector = vectors[cmd]
        num = int(num)
        for i in range(num):
            head[0] += vector[0]
            head[1] += vector[1]
            tail = step_tail(head, tail)
            tails.add(tuple(tail))
            print(head, tail)

print(len(tails))
