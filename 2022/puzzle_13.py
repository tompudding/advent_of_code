import sys

def cmp(a, b):
    if isinstance(a, list) and isinstance(b, list):
        for x,y in zip(a, b):
            r = cmp(x,y)
            if r:
                return r
        #If we get here they were the same
        if len(a) < len(b):
            return -1
        elif len(a) > len(b):
            return 1
        #This means they were identical?
        return 0

    elif isinstance(a, list):
        #This means b is not a list
        return cmp(a, [b])
    elif isinstance(b, list):
        #This means a is not a list
        return cmp([a], b)
    else:
        #Both are integers
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
import functools
    

pairs = []
current = []

with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            pairs.append(current)
            current = []
            continue
        current.append(eval(line))

if current:
    pairs.append(current)

part_one = 0

for i,pair in enumerate(pairs):
    if len(pair) != 2:
        raise ValueError('Bad pair len')

    if cmp(pair[0],pair[1]) < 0:
        #print(f'{i+1} correct')
        part_one += i+1

print(part_one)

dividers = [[[2]], [[6]]]

all_items = dividers[::]
for pair in pairs:
    all_items.extend(pair)

all_items.sort(key=functools.cmp_to_key(cmp))

print((all_items.index(dividers[0])+1)*(all_items.index(dividers[1])+1))
