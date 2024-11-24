import sys

directions = {"R": (1, 0), "U": (0, -1), "D": (0, 1), "L": (-1, 0)}


def manhattan(point):
    return abs(point[0]) + abs(point[1])


def get_points(line):
    points = {}

    point = (0, 0)
    t = 0

    for segment in line:
        vector = directions[segment[0]]
        length = int(segment[1:])
        for i in range(length):
            point = (point[0] + vector[0], point[1] + vector[1])
            t += 1
            if point not in points:
                points[point] = t

    return points


with open(sys.argv[1], "r") as file:
    points = [get_points(line.strip().split(",")) for line in file.readlines()]

crosses = points[0].keys() & points[1].keys()
print(min(manhattan(p) for p in crosses))
print(min(points[0][p] + points[1][p] for p in crosses))
