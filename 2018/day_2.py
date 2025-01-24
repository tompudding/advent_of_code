import sys
from collections import Counter

with open(sys.argv[1], "r") as file:
    data = [line.strip() for line in file]

counts = [Counter(d) for d in data]
twos = [c for c in counts if 2 in c.values()]
threes = [c for c in counts if 3 in c.values()]

print(len(twos) * len(threes))


def common(x, y):
    return "".join(p for p, q in zip(x, y) if p == q)


for a in data:
    for b in data:
        c = common(a, b)
        if len(c) == len(a) - 1:
            print(c, a, b)
