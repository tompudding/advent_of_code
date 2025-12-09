import sys
import itertools
from PIL import Image


def compact(points):
    sorted_x = sorted(p[0] for p in points)
    sorted_y = sorted(p[1] for p in points)

    return tuple((sorted_x.index(p[0]), sorted_y.index(p[1])) for p in points)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


neighbours = ((-1, 0), (1, 0), (0, 1), (0, -1))


with open(sys.argv[1]) as file:
    points = [tuple(int(v) for v in line.strip().split(",")) for line in file]

orig_points = points
points = compact(orig_points)

points_lookup = {points[i]: orig_points[i] for i in range(len(points))}


class Horizontal:
    def __init__(self, y, x_start, x_end):
        self.y = y
        self.x_min = min(x_start, x_end)
        self.x_max = max(x_start, x_end)
        self.start = (x_start, self.y)
        self.unit = (1 if x_start < x_end else -1, 0)

    def all_points(self):
        for x in range(self.x_min, self.x_max + 1):
            yield (x, self.y)


class Vertical:
    def __init__(self, x, y_start, y_end):
        self.x = x
        self.y_min = min(y_start, y_end)
        self.y_max = max(y_start, y_end)
        self.start = (self.x, self.y_min)
        self.unit = (0, 1 if y_start < y_end else -1, 0)

    def all_points(self):
        for y in range(self.y_min, self.y_max + 1):
            yield (self.x, y)


all_lines = []

for a, b in itertools.pairwise(points + points[:1]):
    if a[0] == b[0]:
        new_line = Vertical(a[0], a[1], b[1])
    elif a[1] == b[1]:
        new_line = Horizontal(a[1], a[0], b[0])

    all_lines.append(new_line)

inside_point = all_lines[0].start
inside_point = add(inside_point, all_lines[0].unit)
inside_point = add(inside_point, (-all_lines[-1].unit[0], -all_lines[-1].unit[1]))

point_pairs = {}
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        point_pairs[points[i], points[j]] = (abs(orig_points[i][0] - orig_points[j][0]) + 1) * abs(
            abs(orig_points[i][1] - orig_points[j][1]) + 1
        )

point_pairs = sorted(list(point_pairs.items()), key=lambda x: x[1], reverse=True)

# For part 1 we just take the first
print(point_pairs[0][1])

# For part 2 now we've compacted it's perhaps possible to do everything brute-force style
edges = {p for line in all_lines for p in line.all_points()}

# For debugging
# image = Image.new("RGB", (max(p[0] for p in tiles) + 10, max(p[1] for p in tiles) + 10))
# pixels = image.load()
# for p in tiles:
#    print(p)
#    pixels[p] = (255, 0, 0)

# pixels[inside_point] = (255, 255, 255)


# Now we can flood-fill the centre.
frontier = {inside_point}
interior = {inside_point}
while True:
    new_frontier = set()
    for point in frontier:
        for extra in neighbours:
            new_point = add(point, extra)
            if new_point in edges or new_point in interior or new_point in frontier:
                continue

            new_frontier.add(new_point)
    if not new_frontier:
        break
    interior |= new_frontier
    frontier = new_frontier

# Finally the tiles are the edges plus the interior
tiles = edges | interior


# For part 2 we take the first one where the whole square is interior
for (a, b), area in point_pairs:
    # top and bottom
    top_y = min(a[1], b[1])
    bottom_y = max(a[1], b[1])
    left_x = min(a[0], b[0])
    right_x = max(a[0], b[0])
    lines = [
        Horizontal(top_y, a[0], b[0]),
        Horizontal(bottom_y, a[0], b[0]),
        Vertical(left_x, a[1], b[1]),
        Vertical(right_x, a[1], b[1]),
    ]

    for line in lines:
        if any(point not in tiles for point in line.all_points()):
            break
    else:
        # We're done!
        print(area)
        break
