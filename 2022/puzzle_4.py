import sys


class Range:
    def __init__(self, range_str):
        self.start, self.end = (int(v) for v in range_str.split("-"))

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return not (self.start > other.end or self.end < other.start)


ranges = []
with open(sys.argv[1], "r") as file:
    for line in file:
        ranges.append([Range(v) for v in line.strip().split(",")])

contained = 0
overlaps = 0
for a, b in ranges:
    if a.contains(b) or b.contains(a):
        contained += 1
    if a.overlaps(b):
        overlaps += 1

print(contained)
print(overlaps)
