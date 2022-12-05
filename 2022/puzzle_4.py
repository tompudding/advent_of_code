import sys

class Range:
    def __init__(self, range_str):
        self.start, self.end = (int(v) for v in range_str.split('-'))
        #self.range = set(range(self.start, self.end+1))

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return not (self.start > other.end or self.end < other.start)

ranges = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        ranges.append([Range(v) for v in line.strip().split(',')])

contained = 0
overlaps = 0
for a, b in ranges:
    #combined = a.range | b.range
    #if len(combined) in [len(a.range), len(b.range)]:
    #    contained += 1
    if a.contains(b) or b.contains(a):
        contained += 1
    if a.overlaps(b):
        overlaps += 1

print(contained)
print(overlaps)
    
