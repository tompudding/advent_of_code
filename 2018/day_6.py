import sys
from utils import Point2D as Point, manhattan


class Bounds:
    class DimBound:
        def __init__(self):
            self.min = 2 ** 20
            self.max = 0

        def update(self, val):
            if val < self.min:
                self.min = val
            if val > self.max:
                self.max = val

    def __init__(self):
        self.x = self.DimBound()
        self.y = self.DimBound()

    def get_edge(self):
        top = [(x, 0) for x in range(self.x.min, self.x.max + 1)]
        right = [(self.x.max, y) for y in range(self.y.min, self.y.max + 1)]
        bottom = [(x, self.y.max) for x in range(self.x.min, self.x.max + 1)]
        left = [(0, y) for y in range(self.y.min, self.y.max + 1)]
        return top + right + bottom + left

    def __iter__(self):
        for x in range(self.x.min, self.x.max + 1):
            for y in range(self.y.min, self.y.max + 1):
                yield (x, y)


points = []
bounds = Bounds()

with open(sys.argv[1], "r") as file:
    for line in file:
        x, y = [int(v.strip()) for v in line.strip().split(",")]
        points.append((x, y))
        bounds.x.update(x)
        bounds.y.update(y)


def get_closest(point):
    scores = [(candidate, manhattan(point, candidate)) for candidate in points]
    scores.sort(key=lambda x: x[1])
    if scores[0][1] == scores[1][1]:
        return None

    return scores[0][0]


infinites = set()

for point in bounds.get_edge():
    infinites.add(get_closest(point))

candidates = [point for point in points if point not in infinites]

closest = {}

for point in points:
    closest[point] = set()

for point in bounds:

    winner = get_closest(point)
    if not winner:
        continue

    closest[winner].add(point)

print(max(len(closest[point]) for point in candidates))

target = 32 if len(points) < 10 else 10000

region = set()
for point in bounds:
    total = 0
    for p in points:
        total += manhattan(p, point)
        if total >= target:
            break
    if total < target:
        region.add(point)

print(len(region))
