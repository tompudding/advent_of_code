import sys
import collections

a = []
b = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        x, y = (int(v) for v in line.strip().split())
        a.append(x)
        b.append(y)

a.sort()
b.sort()

print(sum(abs(x-y) for (x,y) in zip(a,b)))

counts = collections.Counter(b)
print(sum((item*counts[item] for item in a)))
