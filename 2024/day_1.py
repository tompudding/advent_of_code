import sys
import collections

lists = [[], []]
with open(sys.argv[1], "r") as file:
    for line in file:
        for i, num in enumerate(line.strip().split()):
            lists[i].append(int(num))

for l in list:
    l.sort()

print(sum(abs(x - y) for (x, y) in zip(*lists)))

counts = collections.Counter(lists[1])
print(sum((item * counts[item] for item in lists[0])))
