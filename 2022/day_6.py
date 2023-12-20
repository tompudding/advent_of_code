import sys

with open(sys.argv[1], 'r') as file:
    data = file.read().strip()

def add(counts, data, c, length):
    try:
        counts[c] += 1
    except KeyError:
        counts[c] = 1
    return len(counts) == length

def calc(data, length):
    counts = {}
    for pos in range(length):
        c = data[pos]
        if add(counts, data, c, length):
            return pos+1

    for pos in range(length,len(data)):
        old = data[pos-length]
        counts[old]-=1
        if counts[old] == 0:
            del counts[old]
        new = data[pos]
        if add(counts, data, new, length):
            return pos+1

    raise Jawn()

print(calc(data, 4))
print(calc(data, 14))

