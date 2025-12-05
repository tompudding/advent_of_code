import sys
import functools


@functools.total_ordering
class Range:
    def __init__(self, start, end):
        assert end >= start
        self.start = start
        self.end = end

    def __contains__(self, value):
        return self.start <= value <= self.end

    def __le__(self, other):
        return self.start <= other.start

    def __eq__(self, other):
        return (self.start, self.end) == (other.start, other.end)

    def __repr__(self):
        return f"{self.start}-{self.end}"


ranges = []
ids = []

with open(sys.argv[1]) as file:
    for line in file:
        line = line.strip()
        if not line:
            break
        start, end = (int(v) for v in line.split("-"))
        ranges.append(Range(start, end))

    count = 0
    for line in file:
        ids.append(int(line.strip()))

ranges.sort()

for value in ids:
    # We could bisect here for a speedup
    count += any(value in r for r in ranges)

print(count)

pos = 0
count = 0
for r in ranges:

    start = max(pos, r.start)
    if pos > r.end:
        continue
    end = r.end

    count += end - start + 1
    pos = end + 1

print(count)

# 330033121340659 is too low
