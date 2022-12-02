import sys
import itertools

rotations = set()

for v in itertools.permutations([0, 1, 2]):
    # This gives 48 rotations which is not correct, but ends up working anyway /shrug
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                rotations.add(((v[0], x), (v[1], y), (v[2], z)))


def vector_equal(a, b):
    return all(((x == y) for x, y in zip(a, b)))


def vector_diff(a, b):
    return [y - x for x, y in zip(a, b)]


def vector_add(a, b):
    return [x + y for x, y in zip(a, b)]


def rotate(vector, rotation):
    out = []

    for index, coeff in rotation:
        out.append(vector[index] * coeff)

    return out


class Distance:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.diff = vector_diff(end, start)
        self.length = sum((diff ** 2 for diff in self.diff))

    def __hash__(self):
        return hash(self.length)

    def __eq__(self, other):
        return other.length == self.length


class Scanner:
    def __init__(self, points, need_distance=True):
        self.points = points
        self.distance_to_point = {}
        if need_distance:
            self.build_distances()
        self.pos = (0, 0, 0)

    def build_distances(self):
        self.matrix = []
        for i, point in enumerate(self.points):
            distances = set()
            for other in self.points:
                if point is other:
                    continue
                distances.add(Distance(point, other))
            self.matrix.append(distances)

    def points_in_common(self, other):
        point_map = {}
        for i, point in enumerate(self.points):
            for j, point in enumerate(other.points):
                matches = self.matrix[i] & other.matrix[j]
                # Why 11?
                if len(matches) >= 11:
                    point_map[i] = j

        return point_map

    def transform(self, rot, trans):
        # We rotate all of the points, then add the translation, returning a new scanner
        points = []

        for point in self.points:
            new_point = tuple(vector_add(rotate(point, rot), trans))
            points.append(new_point)

        out = Scanner(points, need_distance=False)
        out.pos = tuple(vector_add(rotate(self.pos, rot), trans))
        return out


scanners = []

with open(sys.argv[1], "r") as file:
    current = []
    for line in file:
        line = line.strip()
        if not line:
            continue

        if "---" in line:
            if not current:
                continue
            scanners.append(Scanner(current))
            current = []

        else:
            current.append(tuple([int(n) for n in line.split(",")]))

scanners.append(Scanner(current))

transforms = {}
transform_map = {}

for i in range(len(scanners)):
    for j in range(len(scanners)):
        if i == j:
            continue
        common = scanners[i].points_in_common(scanners[j])

        if len(common) == 0:
            continue

        # This allows us to work out the relative position and rotation of the two scanners.  Pick 2 points
        # the same, then look at their difference. Rotate the second until it's the same as the first
        ((point_one_i, point_one_j), (point_two_i, point_two_j)) = [a for a in common.items()][:2]

        point_one_i = scanners[i].points[point_one_i]
        point_one_j = scanners[j].points[point_one_j]
        point_two_i = scanners[i].points[point_two_i]
        point_two_j = scanners[j].points[point_two_j]

        vector_j = [point_two_j[n] - point_one_j[n] for n in (0, 1, 2)]
        vector_i = [point_two_i[n] - point_one_i[n] for n in (0, 1, 2)]

        for rot in rotations:
            rotated = rotate(vector_j, rot)
            if vector_equal(rotated, vector_i):
                break

        else:
            raise SystemExit("No rotation")

        # That's given us the rotation, now we need the absolute difference
        point_two_j_rotated = rotate(point_two_j, rot)

        trans = vector_diff(point_two_j_rotated, point_two_i)

        try:
            transforms[j].add(i)
        except:
            transforms[j] = set([i])

        transform_map[j, i] = (rot, tuple(trans))


# Now for each scanner that isn't scanner[0], we want to find a map of transforms that end in scanner[0], so
# we can get everything in the same frame

points = set(scanners[0].points)
scanner_positions = []

for j in range(1, len(scanners)):
    chain = []

    def explore_chain(chain, pos):
        for neighbour in transforms[pos]:
            if neighbour in chain:
                continue

            if neighbour == 0:
                # This is the end
                yield chain + [neighbour]
                return
            for chain in explore_chain(chain + [neighbour], neighbour):
                yield chain

    scanner = scanners[j]
    total_trans = (0, 0, 0)
    for chain in explore_chain([j], j):
        for pos in range(len(chain) - 1):
            frm, to = chain[pos : pos + 2]
            rot, trans = transform_map[frm, to]
            total_trans = vector_add(trans, total_trans)
            scanner = scanner.transform(rot, trans)

        points |= set(scanner.points)
        break
    scanner_positions.append(scanner.pos)

print(len(points))

maxhatten = 0

for a in scanner_positions:
    for b in scanner_positions:
        if a is b:
            continue

        manhatten = sum((abs(i) for i in vector_diff(b, a)))
        if manhatten > maxhatten:
            maxhatten = manhatten

print(maxhatten)
