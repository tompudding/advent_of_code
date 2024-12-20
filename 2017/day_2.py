import sys
import itertools

with open(sys.argv[1], "r") as file:
    lines = [[int(v) for v in line.strip().split()] for line in file]

print(sum(max(data) - min(data) for data in lines))

total = 0
for data in lines:
    for a, b in itertools.combinations(data, 2):
        if a < b:
            a, b = b, a
        if a % b == 0:
            break
    else:
        print(data)
        raise NoBlow()

    total += a // b

print(total)
