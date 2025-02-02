import sys
from collections import Counter


class Rectangle:
    def __init__(self, line):
        self.id, rest = line[1:].strip().split(" @ ")
        self.id = int(self.id)
        pos, size = rest.split(": ")
        self.pos = [int(part) for part in pos.split(",")]
        self.size = [int(part) for part in size.split("x")]

        self.points = {
            (self.pos[0] + x, self.pos[1] + y) for x in range(self.size[0]) for y in range(self.size[1])
        }


with open(sys.argv[1], "r") as file:
    rects = [Rectangle(line) for line in file]

counts = Counter(rects[0].points)

for rect in rects[1:]:
    counts.update(rect.points)

print(len([count for count in counts.values() if count > 1]))

for rect in rects:
    if all(counts[point] == 1 for point in rect.points):
        print(rect.id)
