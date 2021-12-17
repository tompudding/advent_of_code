import sys
import re

with open(sys.argv[1], "r") as file:
    match = re.match("target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", file.read())
    x1, x2, y1, y2 = (int(n) for n in match.groups())

# with initial velocity K, after n steps the position is
# Step | Height
# -----+-------
#   0  |   0
#   1  |   K
#   2  |  2K-1
#   3  |  3K-3
#   4  |  4K-6
#   n  |  nK- (n*(n-1))/2 = (K+0.5)n - 0.5n**2

# The horizontal position is
# Step | Pos
# -----+-------
#   0  |   0
#   1  |   X
#   2  |   2X-1 #Actually it depends on the abs value of X, fuck it let's just try a bunch

in_area = {}
max_height = 0

for initial_v in range(-1000, 1000):
    v = initial_v
    pos = 0
    current_max_height = 0
    for step in range(0, 1000):
        pos += v
        if pos > current_max_height:
            current_max_height = pos
        v -= 1
        if y1 <= pos <= y2:
            print(f"{initial_v=}, {step=}, {pos=}, {max_height=}")
            if current_max_height > max_height:
                max_height = current_max_height
            try:
                in_area[step].append(initial_v)
            except KeyError:
                in_area[step] = [initial_v]
        if pos < y1:
            break

print(max_height)
count = 0
winners = set()

# next consider the x axis
for initial_v in range(0, 1000):
    v = initial_v
    pos = 0
    for step in range(1000):
        pos += v
        if v > 0:
            v -= 1

        if step in in_area and x1 <= pos <= x2:
            for y in in_area[step]:
                winners.add((initial_v, y))

print(len(winners))
